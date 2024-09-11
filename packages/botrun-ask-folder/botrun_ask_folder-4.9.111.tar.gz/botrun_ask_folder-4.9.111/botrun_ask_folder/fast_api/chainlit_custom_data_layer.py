import os
from datetime import datetime
from typing import Optional, Dict, List, Union
from google.cloud import firestore, storage
from google.oauth2 import service_account
from chainlit.step import StepDict
from chainlit.element import Element, ElementDict
from chainlit.types import (
    ThreadDict,
    Feedback,
    ThreadFilter,
    Pagination,
    PaginatedResponse,
    PageInfo,
)
from chainlit.data import BaseDataLayer, queue_until_user_message
from chainlit.user import PersistedUser, User
import asyncio


class FirestoreGCSDataLayer(BaseDataLayer):
    # 定義集合名稱
    USERS_COLLECTION = "chainlit_users"
    FEEDBACK_COLLECTION = "chainlit_feedback"
    ELEMENTS_COLLECTION = "chainlit_elements"
    STEPS_COLLECTION = "chainlit_steps"
    THREADS_COLLECTION = "chainlit_threads"
    USER_SESSIONS_COLLECTION = "chainlit_user_sessions"

    def __init__(self):
        google_service_account_key_path = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
            "/app/keys/scoop-386004-d22d99a7afd9.json",
        )
        credentials = service_account.Credentials.from_service_account_file(
            google_service_account_key_path,
            scopes=[
                "https://www.googleapis.com/auth/datastore",
                "https://www.googleapis.com/auth/devstorage.read_write",
            ],
        )

        self.db = firestore.Client(credentials=credentials)
        self.storage_client = storage.Client(credentials=credentials)
        self.bucket = self.storage_client.bucket("botrun_ask_folder")

    def _get_current_timestamp(self) -> str:
        return datetime.now().isoformat() + "Z"

    async def get_user(self, identifier: str) -> Optional[PersistedUser]:
        print(f"[chaintlit_custom_data_layer][get_user] identifier: {identifier}")
        doc = self.db.collection(self.USERS_COLLECTION).document(identifier).get()
        if doc.exists:
            user_data = doc.to_dict()
            return PersistedUser(**user_data)
        return None

    async def create_user(self, user: User) -> Optional[PersistedUser]:
        print(f"[chaintlit_custom_data_layer][create_user] user: {user}")
        ts = self._get_current_timestamp()
        user_dict = {
            "id": user.identifier,
            "identifier": user.identifier,
            "metadata": user.metadata,
            "createdAt": ts,
        }
        self.db.collection(self.USERS_COLLECTION).document(user.identifier).set(
            user_dict
        )
        return PersistedUser(**user_dict)

    async def upsert_feedback(self, feedback: Feedback) -> str:
        print(f"[chaintlit_custom_data_layer][upsert_feedback] feedback: {feedback}")
        feedback_id = f"{feedback.threadId}_{feedback.forId}"
        doc_ref = self.db.collection(self.FEEDBACK_COLLECTION).document(feedback_id)
        doc_ref.set(feedback.dict())
        return feedback_id

    async def delete_feedback(self, feedback_id: str) -> bool:
        print(
            f"[chaintlit_custom_data_layer][delete_feedback] feedback_id: {feedback_id}"
        )
        self.db.collection(self.FEEDBACK_COLLECTION).document(feedback_id).delete()
        return True

    @queue_until_user_message()
    async def create_element(self, element: Element):
        print(f"[chaintlit_custom_data_layer][create_element] element: {element}")
        element_dict = element.to_dict()
        if element.type == "file":
            blob = self.bucket.blob(f"chainlit/elements/{element.id}")
            if element.path:
                blob.upload_from_filename(element.path)
            elif element.content:
                blob.upload_from_string(element.content)
            element_dict["content"] = f"gs://{self.bucket.name}/{blob.name}"

        self.db.collection(self.ELEMENTS_COLLECTION).document(element.id).set(
            element_dict
        )

    async def get_element(
        self, thread_id: str, element_id: str
    ) -> Optional[ElementDict]:
        print(
            f"[chaintlit_custom_data_layer][get_element] thread_id: {thread_id}, element_id: {element_id}"
        )
        doc = self.db.collection(self.ELEMENTS_COLLECTION).document(element_id).get()
        if doc.exists:
            element = doc.to_dict()
            if element.get("type") == "file":
                blob = self.bucket.blob(element["content"].split("/", 3)[-1])
                element["content"] = blob.download_as_bytes()
            return element
        return None

    @queue_until_user_message()
    async def delete_element(self, element_id: str, thread_id: Optional[str] = None):
        print(f"[chaintlit_custom_data_layer][delete_element] element_id: {element_id}")
        self.db.collection(self.ELEMENTS_COLLECTION).document(element_id).delete()
        blob = self.bucket.blob(f"chainlit/elements/{element_id}")
        if blob.exists():
            blob.delete()

    @queue_until_user_message()
    async def create_step(self, step_dict: StepDict):
        print(f"[chaintlit_custom_data_layer][create_step] step_dict: {step_dict}")
        self.db.collection(self.STEPS_COLLECTION).document(step_dict["id"]).set(
            step_dict
        )

    @queue_until_user_message()
    async def update_step(self, step_dict: StepDict):
        print(f"[chaintlit_custom_data_layer][update_step] step_dict: {step_dict}")
        self.db.collection(self.STEPS_COLLECTION).document(step_dict["id"]).update(
            step_dict
        )

    @queue_until_user_message()
    async def delete_step(self, step_id: str):
        print(f"[chaintlit_custom_data_layer][delete_step] step_id: {step_id}")
        self.db.collection(self.STEPS_COLLECTION).document(step_id).delete()

    async def get_thread_author(self, thread_id: str) -> str:
        print(
            f"[chaintlit_custom_data_layer][get_thread_author] thread_id: {thread_id}"
        )
        doc = self.db.collection(self.THREADS_COLLECTION).document(thread_id).get()
        if doc.exists:
            return doc.to_dict().get("userId")
        raise ValueError(f"Author not found for thread_id {thread_id}")

    async def delete_thread(self, thread_id: str):
        print(f"[chaintlit_custom_data_layer][delete_thread] thread_id: {thread_id}")
        # 獲取線程文檔
        thread_doc = (
            self.db.collection(self.THREADS_COLLECTION).document(thread_id).get()
        )
        if not thread_doc.exists:
            return

        # 刪除相關的步驟和元素
        batch = self.db.batch()
        batch.delete(thread_doc.reference)

        steps = (
            self.db.collection(self.STEPS_COLLECTION)
            .where("threadId", "==", thread_id)
            .stream()
        )
        elements = (
            self.db.collection(self.ELEMENTS_COLLECTION)
            .where("threadId", "==", thread_id)
            .stream()
        )

        for step in steps:
            batch.delete(step.reference)

        for element in elements:
            batch.delete(element.reference)
            if element.to_dict().get("type") == "file":
                blob = self.bucket.blob(f"chainlit/elements/{element.id}")
                if blob.exists():
                    blob.delete()

        # 執行批量刪除
        batch.commit()

    async def list_threads(
        self, pagination: Pagination, filters: ThreadFilter
    ) -> PaginatedResponse[ThreadDict]:
        print(f"[chainlit_custom_data_layer][list_threads] pagination: {pagination}")
        print(f"[chainlit_custom_data_layer][list_threads] filters: {filters}")
        query = self.db.collection(self.THREADS_COLLECTION)

        try:
            if filters.userId:
                print(
                    f"[chainlit_custom_data_layer][list_threads] Filtering by userId: {filters.userId}"
                )
                query = query.where("userId", "==", filters.userId)

            query = query.order_by("createdAt", direction=firestore.Query.DESCENDING)
            query = query.limit(pagination.first)
            if pagination.cursor:
                last_doc = (
                    self.db.collection(self.THREADS_COLLECTION)
                    .document(pagination.cursor)
                    .get()
                )
                if last_doc.exists:
                    query = query.start_after(last_doc)

            print("[chainlit_custom_data_layer][list_threads] Executing query")

            # 使用 stream() 而不是 get()
            docs_stream = query.stream()

            threads: List[ThreadDict] = []
            async for doc in self._async_stream(docs_stream):
                print(
                    f"[chainlit_custom_data_layer][list_threads] Processing document: {doc.id}"
                )
                thread_data = doc.to_dict()
                thread_data["id"] = doc.id
                threads.append(ThreadDict(**thread_data))

            print(
                f"[chainlit_custom_data_layer][list_threads] Processed {len(threads)} threads"
            )

            has_next_page = len(threads) == pagination.first
            next_cursor = threads[-1].id if has_next_page else None

            return PaginatedResponse(
                data=threads,
                pageInfo=PageInfo(
                    hasNextPage=has_next_page,
                    startCursor=pagination.cursor,
                    endCursor=next_cursor,
                ),
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"[chainlit_custom_data_layer][list_threads] error: {e}")
            raise e

    async def _async_stream(self, stream):
        for doc in stream:
            yield doc
            await asyncio.sleep(0)  # 允許其他協程運行

    async def get_thread(self, thread_id: str) -> Optional[ThreadDict]:
        print(f"[chaintlit_custom_data_layer][get_thread] thread_id: {thread_id}")
        try:
            doc = self.db.collection(self.THREADS_COLLECTION).document(thread_id).get()
            if doc.exists:
                thread = doc.to_dict()
                thread["id"] = doc.id

                # 獲取相關的步驟和元素
                steps = (
                    self.db.collection(self.STEPS_COLLECTION)
                    .where("threadId", "==", thread_id)
                    .order_by("createdAt")
                    .stream()
                )
                elements = (
                    self.db.collection(self.ELEMENTS_COLLECTION)
                    .where("threadId", "==", thread_id)
                    .stream()
                )

                thread["steps"] = [step.to_dict() for step in steps]
                thread["elements"] = [element.to_dict() for element in elements]
                return ThreadDict(**thread)
            return None
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"[chainlit_custom_data_layer][get_thread] error: {e}")
            raise e

    async def update_thread(
        self,
        thread_id: str,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
    ):
        print(f"[chaintlit_custom_data_layer][update_thread] thread_id: {thread_id}")
        ts = self._get_current_timestamp()
        thread_ref = self.db.collection(self.THREADS_COLLECTION).document(thread_id)

        update_data = {
            "createdAt": ts,
        }
        if name is not None:
            update_data["name"] = name
        if user_id is not None:
            update_data["userId"] = user_id
        if metadata is not None:
            update_data["metadata"] = metadata
        if tags is not None:
            update_data["tags"] = tags

        # 使用 set 方法，並設置 merge=True，這樣如果文檔不存在，它會被創建
        thread_ref.set(update_data, merge=True)
        return thread_id

    async def delete_user_session(self, id: str) -> bool:
        self.db.collection(self.USER_SESSIONS_COLLECTION).document(id).delete()
        return True
