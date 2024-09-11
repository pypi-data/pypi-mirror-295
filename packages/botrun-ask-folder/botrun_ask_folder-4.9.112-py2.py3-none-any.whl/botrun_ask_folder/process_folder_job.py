import asyncio
import logging
import os
from botrun_ask_folder.drive_download import (
    drive_download_with_service,
    file_download_with_service,
)
from botrun_ask_folder.drive_download_metadata import (
    get_drive_files_need_update,
    init_drive_folder,
    set_drive_files,
)
from botrun_ask_folder.drive_list_files import drive_list_files_with_service
from botrun_ask_folder.google_drive_service import get_google_drive_service
from botrun_ask_folder.embeddings_to_qdrant import init_qdrant_collection
from botrun_ask_folder.models.drive_file import DriveFile, DriveFileStatus
from botrun_ask_folder.models.drive_folder import DriveFolderStatus
from botrun_ask_folder.models.splitted_file import SplittedFileStatus
from botrun_ask_folder.run_split_txts import run_split_txts_for_distributed
from botrun_ask_folder.embeddings_to_qdrant import embeddings_to_qdrant_distributed
from botrun_ask_folder.services.drive.drive_factory import drive_client_factory
from dotenv import load_dotenv
from botrun_ask_folder.constants import MAX_CONCURRENT_PROCESS_FILES
from google.cloud import run_v2
from google.oauth2 import service_account

load_dotenv()
# Add this near the top of the file, after the imports
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def process_folder_job(
    folder_id: str,
    force: bool,
    embed: bool,
    qdrant_host: str,
    qdrant_port: int,
    qdrant_api_key: str,
):
    logger.info(
        f"Cloud run job Processing folder {folder_id} with force={force} and embed={embed}"
    )
    logger.info(f"Qdrant settings: host={qdrant_host}, port={qdrant_port}")
    logger.info(f"fast_api: {os.getenv('BOTRUN_ASK_FOLDER_FAST_API_URL')}")
    drive_client = drive_client_factory()
    if force:
        logger.info(f"Deleting folder {folder_id} because force is true")
        await drive_client.delete_drive_folder(folder_id)
    drive_folder = await drive_client.get_drive_folder(folder_id)
    if drive_folder is not None:
        drive_folder.status = DriveFolderStatus.PROCESSING
        await drive_client.set_drive_folder(drive_folder)

    service = get_google_drive_service()

    try:
        if embed:
            logger.info(f"Initializing qdrant collection for folder {folder_id}")
            await init_qdrant_collection(
                folder_id,
                force=force,
                qdrant_host=qdrant_host,
                qdrant_port=qdrant_port,
                qdrant_api_key=qdrant_api_key,
            )
    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.error(
            f"init_qdrant_collection folder_id {folder_id} 失敗，錯誤訊息：{e}"
        )
        raise e

    dic_result = drive_list_files_with_service(service, folder_id, max_files=9999999)
    logger.info(f"Listed from {folder_id}, result: {dic_result}")

    drive_files = [
        DriveFile(
            id=item["id"],
            name=item["name"],
            modifiedTime=item["modifiedTime"],
            mimeType=item["mimeType"],
            size=item.get("size", ""),
            parent=item.get("parent", ""),
            path=item.get("path", ""),
            folder_id=folder_id,
        )
        for item in dic_result["items"]
    ]
    drive_files_need_update = drive_files
    if drive_folder is None:
        await init_drive_folder(folder_id, dic_result)
        await set_drive_files(drive_files)
        # 确保 init_drive_folder 完成后再继续
        logger.info(
            f"Initialized drive folder {folder_id}, prepare to download all files from folder"
        )
    else:
        drive_files_need_update = await get_drive_files_need_update(drive_files)
        logger.info(
            f"Folder {folder_id} drive_files_need_update: {drive_files_need_update}"
        )
        await set_drive_files(drive_files_need_update)

    # items = dic_result["items"]

    # 将文件 ID 分组
    file_id_groups = [
        drive_files_need_update[i : i + MAX_CONCURRENT_PROCESS_FILES]
        for i in range(0, len(drive_files_need_update), MAX_CONCURRENT_PROCESS_FILES)
    ]
    if len(file_id_groups) == 0 and drive_folder is not None:
        drive_folder.status = DriveFolderStatus.DONE
        logger.info(
            f"Folder {folder_id} status set to done because no files need to update"
        )
        await drive_client.set_drive_folder(drive_folder)

    # 为每组文件触发一个 Cloud Run Job
    for group in file_id_groups:
        file_ids = ",".join([drive_file.id for drive_file in group])
        trigger_cloud_run_job(
            folder_id, force, embed, file_ids, qdrant_host, qdrant_port, qdrant_api_key
        )


def trigger_cloud_run_job(
    folder_id: str,
    force: bool,
    embed: bool,
    file_ids: str,
    qdrant_host: str,
    qdrant_port: int,
    qdrant_api_key: str,
):
    google_service_account_key_path = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
        "/app/keys/scoop-386004-d22d99a7afd9.json",
    )
    credentials = service_account.Credentials.from_service_account_file(
        google_service_account_key_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = run_v2.JobsClient(credentials=credentials)
    project = credentials.project_id
    job_name = f"projects/{project}/locations/{os.getenv('CLOUD_RUN_REGION', 'asia-east1')}/jobs/process-folder-job"

    args = [
        "--folder_id",
        folder_id,
        "--qdrant_host",
        qdrant_host,
        "--qdrant_port",
        str(qdrant_port),
        "--qdrant_api_key",
        qdrant_api_key,
    ]
    if force:
        args.append("--force")
    if not embed:
        args.append("--no-embed")
    if file_ids:
        args.append("--file_ids")
        args.append(file_ids)
    container_override = run_v2.RunJobRequest.Overrides.ContainerOverride(
        name="gcr.io/scoop-386004/botrun-ask-folder-job",
        args=args,
    )

    job_overrides = run_v2.RunJobRequest.Overrides(
        container_overrides=[container_override]
    )
    request = run_v2.RunJobRequest(name=job_name, overrides=job_overrides)

    operation = client.run_job(request=request)
    logger.info(
        f"Triggered Cloud Run Job {operation.metadata.name} for folder {folder_id} with file_ids: {file_ids}"
    )


async def process_file_ids(
    folder_id: str,
    file_ids: str,
    force: bool,
    embed: bool,
    qdrant_host: str,
    qdrant_port: int,
    qdrant_api_key: str,
):
    service = get_google_drive_service()
    for file_id in file_ids.split(","):
        drive_client = drive_client_factory()
        drive_file = await drive_client.get_drive_file(file_id)
        await download_single_file_and_embed(
            drive_file, service, force, embed, qdrant_host, qdrant_port, qdrant_api_key
        )


async def download_single_file_and_embed(
    drive_file: DriveFile,
    service,
    force: bool,
    embed: bool,
    qdrant_host: str,
    qdrant_port: int,
    qdrant_api_key: str,
):
    folder_path = "./data"
    logger.info(f"Downloading file: {drive_file.id}")
    drive_file = file_download_with_service(
        service, drive_file, folder_path, force=force
    )

    if force:
        drive_file.splitted_files = []

    drive_client = drive_client_factory()
    await drive_client.set_drive_file(drive_file)
    await drive_client.update_drive_file_status_in_folder(
        drive_file.folder_id, drive_file.id, drive_file.status
    )
    await run_split_txts_for_distributed(drive_file, force=force)
    logger.info(f"File: {drive_file.id} splitted")

    if embed:
        await embed_file(drive_file, qdrant_host, qdrant_port, qdrant_api_key)
    else:
        await mark_file_as_embedded(drive_file)


async def embed_file(
    drive_file: DriveFile, qdrant_host: str, qdrant_port: int, qdrant_api_key: str
):
    embed_success = False
    try:
        print(f"_handle_download_and_embed Embedding file: {drive_file.id}")
        embed_success = await embeddings_to_qdrant_distributed(
            drive_file,
            qdrant_host=qdrant_host,
            qdrant_port=qdrant_port,
            qdrant_api_key=qdrant_api_key,
        )
        print(
            f"_handle_download_and_embed Embedding file: {drive_file.id} done, check success: {embed_success}"
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.error(f"Embedding 失敗，錯誤訊息：{e} for file {drive_file.id}")

    if embed_success:
        drive_file.status = DriveFileStatus.EMBEDDED
        drive_client = drive_client_factory()
        await drive_client.set_drive_file(drive_file)
        logger.info(
            f"Folder {drive_file.folder_id} Embedding file: {drive_file.id} set status to embedded"
        )
        await drive_client.update_drive_file_status_in_folder(
            drive_file.folder_id, drive_file.id, drive_file.status
        )
        await finalize_embed(drive_file)


async def mark_file_as_embedded(drive_file: DriveFile):
    drive_client = drive_client_factory()
    for split_id in drive_file.splitted_files:
        split_file = await drive_client.get_splitted_file(split_id)
        split_file.status = SplittedFileStatus.EMBEDDED
        await drive_client.set_splitted_file(split_file)
    drive_file.status = DriveFileStatus.EMBEDDED
    await drive_client.set_drive_file(drive_file)
    await drive_client.update_drive_file_status_in_folder(
        drive_file.folder_id, drive_file.id, drive_file.status
    )
    await finalize_embed(drive_file)


async def finalize_embed(drive_file: DriveFile):
    logger.info(f"_finalize_embed called from {drive_file.id}")
    drive_client = drive_client_factory()
    for item in drive_file.splitted_files:
        split_file = await drive_client.get_splitted_file(item)
        split_file.status = SplittedFileStatus.EMBEDDED
        await drive_client.set_splitted_file(split_file)
        if split_file.save_path:
            try:
                logger.info(
                    f"Removing split file {split_file.id} save path, from file {drive_file.id}"
                )
                os.remove(split_file.save_path)
            except Exception as e:
                logger.error(
                    f"Error removing split file {split_file.id} save path: {e}"
                )
    drive_folder = await drive_client.get_drive_folder(drive_file.folder_id)
    all_files_embedded = True
    logger.info(
        f"called from {drive_file.id}, checking drive_folder.items {drive_folder.items}"
    )
    if len(drive_folder.items) == 0:
        logger.info(
            f"called from {drive_file.id}, Folder {drive_folder.id} items is empty"
        )
    for file_id in drive_folder.items:
        tmp_drive_file = await drive_client_factory().get_drive_file(file_id)
        if tmp_drive_file.status != DriveFileStatus.EMBEDDED:
            logger.info(
                f"called from {drive_file.id}, Folder {drive_folder.id} checking File {tmp_drive_file.id} status is not embedded"
            )
            all_files_embedded = False
            break
    if all_files_embedded:
        drive_folder.status = DriveFolderStatus.DONE
        for id, file_status in drive_folder.file_statuses.items():
            drive_folder.file_statuses[id] = DriveFileStatus.EMBEDDED
        logger.info(
            f"called from {drive_file.id}, All files embedded, updating folder {drive_folder.id} status to done"
        )
        await drive_client.set_drive_folder(drive_folder)
    if drive_file.save_path:
        try:
            logger.info(
                f"called from {drive_file.id}, Removing drive file {drive_file.id} save path"
            )
            os.remove(drive_file.save_path)
        except Exception as e:
            logger.info(
                f"called from {drive_file.id}, Error removing drive file {drive_file.id} save path: {e}"
            )
    logger.info(
        f"called from {drive_file.id},Finalize embed for drive file {drive_file.id}"
    )
