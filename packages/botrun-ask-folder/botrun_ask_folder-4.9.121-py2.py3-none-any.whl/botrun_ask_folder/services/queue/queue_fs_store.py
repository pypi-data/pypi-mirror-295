import asyncio
from google.cloud import firestore
from google.cloud.firestore import FieldFilter
from google.oauth2 import service_account
import os
from botrun_ask_folder.models.job_event import JobEvent
from botrun_ask_folder.services.queue.queue_store import (
    QueueStore,
    QUEUE_STORE_NAME,
)
from botrun_ask_folder.constants import MAX_WORKERS
import json
import random
from google.cloud.firestore_v1.transaction import Transaction


STATUS_PENDING = "pending"
STATUS_PROCESSING = "processing"
STATUS_FAILED = "failed"


class QueueFsStore(QueueStore):
    def __init__(self):
        google_service_account_key_path = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
            "/app/keys/scoop-386004-d22d99a7afd9.json",
        )
        credentials = service_account.Credentials.from_service_account_file(
            google_service_account_key_path,
            scopes=["https://www.googleapis.com/auth/datastore"],
        )

        self.db = firestore.Client(credentials=credentials)
        self.collection = self.db.collection(QUEUE_STORE_NAME)
        self.max_workers = MAX_WORKERS

    async def enqueue(self, job: JobEvent) -> str:
        doc_ref = self.collection.document(job.id)
        doc_ref.set(
            {
                "id": job.id,
                "status": STATUS_PENDING,
                "updated_at": firestore.SERVER_TIMESTAMP,
                "job_data": job.model_dump(),
            }
        )
        return job.id

    async def dequeue(self, all: bool = False) -> JobEvent:
        # 使用事务来确保原子性操作
        @firestore.transactional
        def dequeue_transaction(transaction, all: bool = False):
            if all:
                query = self.collection.order_by("updated_at").limit(1)
            else:
                # 查找第一个状态为 "pending" 的任务
                query = (
                    self.collection.where(
                        filter=FieldFilter("status", "==", STATUS_PENDING)
                    )
                    .order_by("updated_at")
                    .limit(1)
                )
            docs = list(query.stream(transaction=transaction))

            if not docs:
                return None

            doc = docs[0]
            doc_ref = doc.reference

            # 更新任务状态为 "processing"
            transaction.update(
                doc_ref,
                {
                    "status": STATUS_PROCESSING,
                    "updated_at": firestore.SERVER_TIMESTAMP,
                },
            )

            # 返回任务数据
            job_data = doc.to_dict()["job_data"]
            return JobEvent(**job_data)

        transaction = self.db.transaction()
        return dequeue_transaction(transaction, all)

    async def complete_job(self, job_id, transaction=None):
        doc_ref = self.collection.document(job_id)
        doc_ref.delete()

    async def fail_job(self, job_id: str, error: str):
        doc_ref = self.collection.document(job_id)
        await doc_ref.update(
            {
                "status": STATUS_FAILED,
                "updated_at": firestore.SERVER_TIMESTAMP,
                "error": error,
            }
        )

    async def reset_job(self, job_id: str):
        doc_ref = self.collection.document(job_id)
        await doc_ref.update(
            {
                "status": STATUS_PENDING,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }
        )
