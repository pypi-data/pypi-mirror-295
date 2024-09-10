from abc import ABC, abstractmethod
from botrun_ask_folder.models.job_event import JobEvent

QUEUE_STORE_NAME = "job-queue-store"


class QueueStore(ABC):
    @abstractmethod
    async def enqueue(self, job: JobEvent) -> str:
        pass

    @abstractmethod
    async def dequeue(self, all: bool = False) -> JobEvent:
        pass

    @abstractmethod
    async def complete_job(self, job_id: str):
        pass

    @abstractmethod
    async def fail_job(self, job_id: str, error: str):
        pass

    @abstractmethod
    async def reset_job(self, job_id: str):
        pass

    @staticmethod
    def get_queue_store_key(job_id: str) -> str:
        return f"{QUEUE_STORE_NAME}:{job_id}"
