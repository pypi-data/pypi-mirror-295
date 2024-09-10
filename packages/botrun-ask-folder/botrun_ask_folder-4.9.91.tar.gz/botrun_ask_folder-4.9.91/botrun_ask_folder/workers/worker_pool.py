import asyncio
import random
import json
import time
import httpx
import threading
from botrun_ask_folder.drive_download_metadata import init_drive_folder
from botrun_ask_folder.drive_list_files import (
    drive_list_files_with_service,
)
from botrun_ask_folder.embeddings_to_qdrant import (
    init_qdrant_collection,
)
from botrun_ask_folder.google_drive_service import get_google_drive_service
from botrun_ask_folder.models.drive_file import DriveFile
from botrun_ask_folder.models.job_event import JobEvent
from botrun_ask_folder.services.drive.drive_factory import (
    drive_client_factory,
)
from botrun_ask_folder.services.queue.queue_factory import (
    queue_client_factory,
)
from botrun_ask_folder.constants import (
    MAX_EMPTY_CHECKS,
    MAX_WORKERS,
    TOPIC_DOWNLOAD_AND_EMBED,
    TOPIC_USER_INPUT_FOLDER,
)
import os
from botrun_ask_folder.fast_api.util.http_request_retry_decorator import async_retry


class WorkerPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkerPool, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        self.queue_client = queue_client_factory()
        self.workers = []
        self.is_running = False
        self.initialized = True
        self.active_workers = 0

    async def process_batch(self):
        self.active_workers = MAX_WORKERS
        self.workers = [asyncio.create_task(self.worker(i)) for i in range(MAX_WORKERS)]
        print(f"Worker pool started processing batch with {MAX_WORKERS} workers")
        await asyncio.gather(*self.workers)
        print("Worker pool finished processing batch")

    async def worker(self, worker_id: int):
        consecutive_empty_checks = 0
        max_empty_checks = MAX_EMPTY_CHECKS

        print(f"Worker {worker_id} started")

        while self.is_running and self.active_workers > 0:
            try:
                time1 = time.time()
                job = await self.queue_client.dequeue()
                time2 = time.time()
                print(f"Worker {worker_id} dequeue job time: {time2 - time1}")
                if job is None:
                    consecutive_empty_checks += 1
                    if consecutive_empty_checks >= max_empty_checks:
                        self.active_workers -= 1
                        break  # Exit the loop if this worker is no longer needed
                    wait_time = random.uniform(5, 10)
                    await asyncio.sleep(wait_time)
                    continue

                consecutive_empty_checks = 0
                await self.handle_job(worker_id, job)

                # Check if we need to add more workers
                if self.active_workers < MAX_WORKERS:
                    self.active_workers += 1
                    asyncio.create_task(self.worker(len(self.workers)))
                    self.workers.append(asyncio.current_task())

            except Exception as e:
                import traceback

                traceback.print_exc()
                print(f"Worker {worker_id}: Error processing job: {str(e)}")

        print(f"Worker {worker_id} terminated.")

    async def handle_job(self, worker_id: int, job: JobEvent):
        print(f"Worker {worker_id}: Processing job {job.topic} {job.id}")
        try:
            data = json.loads(job.data)
            if job.topic == TOPIC_USER_INPUT_FOLDER:
                await self._handle_user_input_folder(
                    worker_id, data["folder_id"], data["force"], data["embed"]
                )
            elif job.topic == TOPIC_DOWNLOAD_AND_EMBED:
                await self._handle_download_and_embed(
                    worker_id,
                    DriveFile.from_json(data["drive_file"]),
                    data["force"],
                    data["embed"],
                )
            await self.queue_client.complete_job(job.id)
            print(f"Worker {worker_id}: complete job {job.id}")
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"Error handling job {job.id}: {str(e)}")
            try:
                await self.queue_client.reset_job(job.id)
                print(f"worker {worker_id} reset job {job.id} done")
            except Exception as e:
                print(f"worker {worker_id} Error resetting job {job.id}: {str(e)}")

    async def _handle_user_input_folder(
        self, worker_id: int, folder_id: str, force: bool, embed: bool
    ):
        print(f"Processing folder: {folder_id}, force: {force}")
        if force:
            client = drive_client_factory()
            await client.delete_drive_folder(folder_id)
        try:
            if embed:
                await init_qdrant_collection(folder_id, force=force)
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(
                f"worker {worker_id} init_qdrant_collection folder_id {folder_id} 失敗，錯誤訊息：{e}"
            )
            # 有問題要丟出去，才會重置狀態
            raise e
        dic_result = drive_list_files_with_service(
            get_google_drive_service(), folder_id, 9999999
        )
        await init_drive_folder(folder_id, dic_result)
        items = dic_result["items"]

        for item in items:
            drive_file = DriveFile(
                id=item["id"],
                name=item["name"],
                modifiedTime=item["modifiedTime"],
                mimeType=item["mimeType"],
                size=item.get("size", ""),
                parent=item.get("parent", ""),
                path=item.get("path", ""),
                folder_id=folder_id,
            )
            await self.queue_client.enqueue(
                JobEvent(
                    topic=TOPIC_DOWNLOAD_AND_EMBED,
                    data=json.dumps(
                        {
                            "drive_file": drive_file.to_json(),
                            "force": force,
                            "embed": embed,
                        }
                    ),
                )
            )
        asyncio.create_task(self.start())

    async def _handle_download_and_embed(
        self, worker_id: int, drive_file: DriveFile, force: bool, embed: bool
    ):
        print(f"Worker {worker_id}: start _handle_download_and_embed {drive_file.id}")
        thread = threading.Thread(
            target=self._run_async_send_process_file_request,
            args=(drive_file, force, embed),
        )
        thread.start()

    def _run_async_send_process_file_request(self, drive_file, force, embed):
        asyncio.run(self._send_process_file_request(drive_file, force, embed))

    @async_retry(attempts=3, delay=1)
    async def _send_process_file_request(self, drive_file, force, embed):
        api_url = os.getenv("BOTRUN_ASK_FOLDER_FAST_API_URL")
        try:
            async with httpx.AsyncClient(timeout=3600) as client:
                response = await client.post(
                    f"{api_url}/api/botrun/botrun_ask_folder/process-file",
                    json={
                        "file_id": drive_file.id,
                        "force": force,
                        "embed": embed,
                    },
                )
            if response.status_code != 200:
                print(f"Error processing file: {response.text}")
            else:
                print(
                    f"_send_process_file_request File {drive_file.id} processed successfully"
                )
        except Exception as e:
            print(f"Error sending request for file {drive_file.id}: {str(e)}")
            raise  # Re-raise the exception to trigger the retry mechanism

    async def start(self):
        if not self.is_running:
            self.is_running = True
            await self.process_batch()
            self.is_running = False

    async def stop(self):
        if self.is_running:
            self.active_workers = 0
            for worker in self.workers:
                worker.cancel()
            await asyncio.gather(*self.workers, return_exceptions=True)
            self.workers = []
            self.is_running = False
            print("Worker pool stopped")


worker_pool = WorkerPool()
