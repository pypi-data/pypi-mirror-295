from fastapi import FastAPI, HTTPException, Query, APIRouter, Depends
from fastapi.responses import StreamingResponse, Response, JSONResponse, FileResponse
from urllib.parse import quote
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import io
import os
import json
import asyncio
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from botrun_ask_folder.constants import TOPIC_USER_INPUT_FOLDER
from botrun_ask_folder.embeddings_to_qdrant import embeddings_to_qdrant_distributed

from botrun_ask_folder.fast_api.util.pdf_util import pdf_page_to_image, DEFAULT_DPI
from botrun_ask_folder.google_drive_service import get_google_drive_service
from botrun_ask_folder.models.drive_file import DriveFile, DriveFileStatus
from botrun_ask_folder.models.drive_folder import DriveFolder, DriveFolderStatus
from botrun_ask_folder.models.splitted_file import SplittedFile, SplittedFileStatus
from botrun_ask_folder.process_folder_job import (
    finalize_embed,
    download_single_file_and_embed,
)
from botrun_ask_folder.run_split_txts import run_split_txts_for_distributed

from botrun_ask_folder.drive_download import (
    file_download_with_service,
)
from botrun_ask_folder.services.drive.drive_factory import (
    drive_client_factory,
)
from botrun_ask_folder.services.queue.queue_factory import (
    queue_client_factory,
)
from botrun_ask_folder.models.job_event import JobEvent
from botrun_ask_folder.split_txts import process_single_file
from botrun_ask_folder.workers.worker_pool import worker_pool
from google.cloud import run_v2
from google.cloud.run_v2.types import RunJobRequest
from dotenv import load_dotenv

from botrun_ask_folder.fast_api.jwt_util import verify_token

load_dotenv()

router = APIRouter(prefix="/botrun_ask_folder", tags=["botrun_ask_folder"])


current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
router.mount("/static", StaticFiles(directory=static_dir), name="static")


@router.get("/stress", response_class=FileResponse)
async def stress_page():
    return FileResponse(os.path.join(static_dir, "stress.html"))


@router.get("/chainlit.css", response_class=FileResponse)
async def chainlit_css():
    return FileResponse(os.path.join(static_dir, "chainlit.css"))


@router.get("/download_file/{file_id}")
def download_file(file_id: str):
    service_account_file = "keys/google_service_account_key.json"
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=["https://www.googleapis.com/auth/drive"]
    )
    drive_service = build("drive", "v3", credentials=credentials)

    try:
        file = (
            drive_service.files().get(fileId=file_id, fields="name, mimeType").execute()
        )
        file_name = file.get("name")
        file_mime_type = file.get("mimeType")

        request = drive_service.files().get_media(fileId=file_id)

        def file_stream():
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                yield fh.getvalue()
                fh.seek(0)
                fh.truncate(0)

        # Encode the filename for Content-Disposition
        encoded_filename = quote(file_name)

        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
            "Content-Type": file_mime_type,
        }

        return StreamingResponse(
            file_stream(), headers=headers, media_type=file_mime_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_pdf_page/{file_id}")
def get_pdf_page(
    file_id: str,
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    dpi: int = Query(DEFAULT_DPI, ge=72, le=600, description="DPI for rendering"),
    scale: float = Query(1.0, ge=0.1, le=2.0, description="Scaling factor"),
    color: bool = Query(True, description="Render in color if True, else grayscale"),
):
    try:
        img_byte_arr = pdf_page_to_image(
            file_id=file_id, page=page, dpi=dpi, scale=scale, color=color
        )

        return Response(content=img_byte_arr, media_type="image/png")
    except ValueError as e:
        return Response(content=str(e), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class FolderRequest(BaseModel):
    folder_id: str
    force: bool = False
    embed: bool = True
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    qdrant_api_key: str = ""


@router.post("/pub-process-folder", dependencies=[Depends(verify_token)])
async def pub_process_folder(request: FolderRequest):
    print(f"Processing folder {request.folder_id} with force={request.force}")

    if request.force:
        client = drive_client_factory()
        await client.delete_drive_folder(request.folder_id)

    queue_client = queue_client_factory()
    await queue_client.enqueue(
        JobEvent(
            topic=TOPIC_USER_INPUT_FOLDER,
            data=json.dumps(
                {
                    "folder_id": request.folder_id,
                    "force": request.force,
                    "embed": request.embed,
                }
            ),
        )
    )
    asyncio.create_task(worker_pool.start())
    return {
        "message": f"Drive folder {request.folder_id} processing initiated",
        "status": "success",
    }


@router.post("/process-folder-job", dependencies=[Depends(verify_token)])
async def process_folder_job(request: FolderRequest):
    print(
        f"Processing folder {request.folder_id} with force={request.force} using Cloud Run Job"
    )

    # Get the credentials from the key file
    google_service_account_key_path = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
        "/app/keys/scoop-386004-d22d99a7afd9.json",
    )
    credentials = service_account.Credentials.from_service_account_file(
        google_service_account_key_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Create a Cloud Run Jobs client
    client = run_v2.JobsClient(credentials=credentials)

    # Get the project ID from the credentials
    project = credentials.project_id

    # Prepare the job request
    job_name = f"projects/{project}/locations/{os.getenv('CLOUD_RUN_REGION', 'asia-east1')}/jobs/process-folder-job"

    args = [
        "--folder_id",
        request.folder_id,
        "--qdrant_host",
        request.qdrant_host,
        "--qdrant_port",
        str(request.qdrant_port),
        "--qdrant_api_key",
        request.qdrant_api_key,
    ]
    if request.force:
        args.append("--force")
    if not request.embed:
        args.append("--no-embed")
    container_override = RunJobRequest.Overrides.ContainerOverride(
        name="gcr.io/scoop-386004/botrun-ask-folder-job",
        args=args,
    )

    job_overrides = RunJobRequest.Overrides(container_overrides=[container_override])

    job_request = RunJobRequest(name=job_name, overrides=job_overrides)

    print(
        "start invoke Cloud Run Job process_folder_job with folder_id: ",
        request.folder_id,
    )
    # 触发 Job
    operation = client.run_job(request=job_request)

    # 返回成功响应
    return {
        "message": "Job triggered successfully",
        "job_id": operation.metadata.name,
        "status": "success",
    }


@router.get("/heartbeat", dependencies=[Depends(verify_token)])
async def heartbeat():
    print("Triggering Cloud Run Job heartbeat check")

    # Get the credentials from the key file
    google_service_account_key_path = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
        "/app/keys/scoop-386004-d22d99a7afd9.json",
    )
    credentials = service_account.Credentials.from_service_account_file(
        google_service_account_key_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Create a Cloud Run Jobs client
    client = run_v2.JobsClient(credentials=credentials)

    # Get the project ID from the credentials
    project = credentials.project_id

    # Prepare the job request
    job_name = f"projects/{project}/locations/{os.getenv('CLOUD_RUN_REGION', 'asia-east1')}/jobs/process-folder-job"

    args = ["--folder_id", "heartbeat_check", "--heartbeat"]
    container_override = RunJobRequest.Overrides.ContainerOverride(
        name="gcr.io/scoop-386004/botrun-ask-folder-job",
        args=args,
    )

    job_overrides = RunJobRequest.Overrides(container_overrides=[container_override])

    job_request = RunJobRequest(name=job_name, overrides=job_overrides)

    print("start invoke Cloud Run Job heartbeat check")
    # 触发 Job
    operation = client.run_job(request=job_request)

    # 返回成功响应
    return {
        "message": "Heartbeat job triggered successfully",
        "job_id": operation.metadata.name,
        "status": "success",
    }


class FolderStatusRequest(BaseModel):
    folder_id: str
    # 因為 cloud run job 沒有立即執行，所以加入這個參數，如果偵測到 folder updated_at 比 action_started_at 舊，就回等待中
    action_started_at: str = ""


@router.post("/folder-status", dependencies=[Depends(verify_token)])
async def folder_status(request: FolderStatusRequest):
    folder_id = request.folder_id
    client = drive_client_factory()

    try:
        folder = await client.get_drive_folder(folder_id)
        if request.action_started_at and folder.updated_at < request.action_started_at:
            return {
                "status": "WAITING",
                "message": "Folder is waiting to be processed",
            }

        total_files = len(folder.items)
        embedded_files = sum(
            1
            for status in folder.file_statuses.values()
            if status == DriveFileStatus.EMBEDDED
        )

        response = {
            "status": folder.status.value,
            "message": f"Folder {folder_id} status: {folder.status.value}",
            "updated_at": folder.updated_at,
            "total_files": total_files,
            "embedded_files": embedded_files,
            "processing_files": total_files - embedded_files,
        }

        if folder.status == DriveFolderStatus.DONE:
            response["message"] = f"Folder {folder_id} processing completed"
        elif folder.status == DriveFolderStatus.INTIATED:
            response["message"] = f"Folder {folder_id} processing not started yet"
        elif folder.status == DriveFolderStatus.PROCESSING:
            response["message"] = f"Folder {folder_id} is being processed"

        print(f"[Folder {folder_id}] Response: {response}")
        return response

    except Exception as e:
        print(f"[Folder {folder_id}] Error in folder_status: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error processing folder status: {str(e)}"
        )


@router.post("/start-worker")
async def start_worker(request: FolderRequest):
    print(f"Starting workers for folder {request.folder_id}")

    # Start worker pool (if not already started)
    asyncio.create_task(worker_pool.start())

    return {
        "message": f"Workers started for folder {request.folder_id}",
        "status": "success",
    }


@router.post("/complete-all-jobs", dependencies=[Depends(verify_token)])
async def complete_all_jobs():
    """
    清空所有 job queue 裡的 job，開發用
    """
    queue_client = queue_client_factory()
    completed_count = 0

    try:
        while True:
            job = await queue_client.dequeue(all=True)
            if job is None:
                break

            if hasattr(job, "id"):
                await queue_client.complete_job(job.id)
                completed_count += 1

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error completing jobs: {str(e)}")

    return {
        "message": "All jobs completed",
        "status": "success",
        "jobs_completed": completed_count,
    }


class DriveFileRequest(BaseModel):
    file_id: str
    force: bool = False
    # 是否要 embed，這個是做壓測試的時候，可設成 false ，來節省 embed 的金額
    embed: bool = True


@router.post("/process-file", dependencies=[Depends(verify_token)])
async def process_file(request: DriveFileRequest):
    # drive_file = DriveFile.from_json(request.drive_file)
    force = request.force
    embed = request.embed

    try:
        drive_client = drive_client_factory()
        drive_file = await drive_client.get_drive_file(request.file_id)
        download_single_file_and_embed(
            drive_file, get_google_drive_service(), force, embed
        )
        return {
            "status": "success",
            "message": f"File {drive_file.id} processed successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
