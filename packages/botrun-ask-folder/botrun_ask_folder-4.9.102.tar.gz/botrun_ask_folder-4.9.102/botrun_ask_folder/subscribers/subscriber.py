from fastapi import FastAPI, Request
import json
import uvicorn
import os
from dapr.clients import DaprClient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
from botrun_ask_folder.drive_list_files import drive_list_files
from botrun_ask_folder.constants import (
    PUBSUB_NAME_EMBEDDING,
    SECRET_STORE_NAME,
    TOPIC_USER_INPUT_FOLDER,
    STATE_STORE_NAME,
    TOPIC_DOWNLOAD_AND_EMBED,
    STORAGE_NAME,
)
from botrun_ask_folder.models.drive_folder import DriveFolder, DriveFolderStatus
from botrun_ask_folder.services.drive.drive_store import DriveFolderStore
from botrun_ask_folder.drive_download import (
    convert_google_apps_mime_to_office_mime,
    append_export_extension_to_path,
)
import base64

app = FastAPI()


@app.post("/process_user_input_folder")
async def process_user_input_folder(request: Request):
    data = await request.json()
    # print(f"process_user_input_folder Received data: {data}", flush=True)
    data = data.get("data")
    if not data:
        print("Missing data", flush=True)
        return {"success": False, "error": "Missing data"}

    folder_id = data.get("folder_id")
    force = data.get("force", False)
    print(f"folder_id: {folder_id}, force: {force}", flush=True)
    if not folder_id:
        print("Missing folder_id", flush=True)
        return {"success": False, "error": "Missing folder_id"}

    with DaprClient() as client:

        # 從狀態存儲中獲取文件夾狀態
        state_key = DriveFolderStore.get_drive_folder_store_key(folder_id)
        state = client.get_state(store_name=STATE_STORE_NAME, key=state_key).data

        if state:
            folder_state = DriveFolder.model_validate_json(state)
            if folder_state.status == DriveFolderStatus.PROCESSING and not force:
                print(f"Folder {folder_id} already processed. Skipping.")
                return {"success": True, "message": "Folder already processed"}

        # 更新狀態為 PROCESSED
        new_state = DriveFolder(id=folder_id, status=DriveFolderStatus.PROCESSING)
        response = client.save_state(
            store_name=STATE_STORE_NAME,
            key=state_key,
            value=new_state.model_dump_json(),
        )
        secret_response = client.get_secret(
            store_name=SECRET_STORE_NAME, key="GOOGLE_APPLICATION_CREDENTIALS"
        )
        service_account_file = secret_response.secret["GOOGLE_APPLICATION_CREDENTIALS"]
        dic_result = drive_list_files(service_account_file, folder_id, 9999999)
        # print(dic_result)
        # print(f"items: {dic_result.get('items', [])}")

        for item in dic_result.get("items", []):
            # print(f"publish event: {item.get('id')}")
            client.publish_event(
                pubsub_name=PUBSUB_NAME_EMBEDDING,
                topic_name=TOPIC_DOWNLOAD_AND_EMBED,
                data=json.dumps(
                    {
                        "folder_id": folder_id,
                        "file_id": item.get("id"),
                        "file_name": item.get("name"),
                        "mime_type": item.get("mimeType"),
                        "path": item.get("path"),
                    }
                ),
                data_content_type="application/json",
            )

        print(
            f"Folder {folder_id} processed successfully and DOWNLOAD_and_EMBED event published"
        )
        return {
            "success": True,
            "message": "Folder processed and DOWNLOAD_and_EMBED event published",
        }


def download_file_from_drive(service, file_id: str, mime_type: str) -> BytesIO:
    """從 Google Drive 下載文件"""
    export_mime = convert_google_apps_mime_to_office_mime(mime_type)
    if export_mime:
        request = service.files().export_media(fileId=file_id, mimeType=export_mime)
    else:
        request = service.files().get_media(fileId=file_id)

    file_content = BytesIO()
    downloader = MediaIoBaseDownload(file_content, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    file_content.seek(0)
    return file_content


def upload_file_to_gcs(
    client: DaprClient, file_path: str, file_content: BytesIO, mime_type: str
):
    """上傳文件到 Google Cloud Storage"""
    # 將文件內容轉換為 base64 編碼
    file_content_base64 = base64.b64encode(file_content.getvalue()).decode("utf-8")

    metadata = {"key": file_path, "contentType": mime_type}

    try:
        print(f"Uploading file {file_path} to GCS")
        response = client.invoke_binding(
            binding_name=STORAGE_NAME,
            operation="create",
            data=file_content_base64,
            binding_metadata=metadata,
        )
        print(f"File {file_path} uploaded to GCS")
        return response
    except Exception as e:
        print(f"Error uploading file {file_path} to GCS: {str(e)}")
        raise


@app.post("/download_and_embed")
async def download_and_embed(request: Request):
    data = await request.json()
    print(f"download_and_embed Received data: {data}", flush=True)
    data = data.get("data")
    folder_id = data.get("folder_id")
    file_id = data.get("file_id")
    file_name = data.get("file_name")
    mime_type = data.get("mime_type")
    path = data.get("path")
    return {"success": True, "message": "File downloaded and uploaded to GCS"}
    print(f"Downloading and embedding file {file_id} for folder {folder_id}")
    if not folder_id or not file_id:
        print("Missing folder_id or file_id", flush=True)
        return {"success": False, "error": "Missing folder_id or file_id"}

    with DaprClient() as client:
        # 獲取 Google 服務帳戶憑證文件路徑
        secret_response = client.get_secret(
            store_name=SECRET_STORE_NAME, key="GOOGLE_APPLICATION_CREDENTIALS"
        )
        service_account_file = secret_response.secret["GOOGLE_APPLICATION_CREDENTIALS"]

        # 創建 Google Drive 服務
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file
        )
        service = build("drive", "v3", credentials=credentials)

        # 獲取文件信息
        # file_metadata = (
        #     service.files().get(fileId=file_id, fields="name,path,mimeType").execute()
        # )
        # print(f"File metadata: {file_metadata}")
        # file_name = file_metadata["name"]
        # path = file_metadata["path"]
        # mime_type = file_metadata["mimeType"]

        # 下載文件
        file_content = download_file_from_drive(service, file_id, mime_type)

        # 準備文件路徑
        file_path = f"{folder_id}/{path}"
        file_path = append_export_extension_to_path(file_path, mime_type)

        # 上傳到 GCS
        response = upload_file_to_gcs(client, file_path, file_content, mime_type)
        print(f"Response from GCS: {response}")

    # TODO: 實現嵌入邏輯

    return {
        "success": True,
        "message": f"File {file_path} downloaded and uploaded to GCS",
    }


@app.get("/dapr/subscribe")
def subscribe():
    subscriptions = [
        {
            "pubsubname": PUBSUB_NAME_EMBEDDING,
            "topic": TOPIC_USER_INPUT_FOLDER,
            "route": "/process_user_input_folder",
        },
        {
            "pubsubname": PUBSUB_NAME_EMBEDDING,
            "topic": TOPIC_DOWNLOAD_AND_EMBED,
            "route": "/download_and_embed",
        },
    ]
    return subscriptions


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
