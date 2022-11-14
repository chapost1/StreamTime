from uuid import UUID
from typing import Callable
from data_access.rds.abstract import VideosDB
from data_access.storage.abstract import Storage
from models.storage import FileUploadSignedInstructions
from use_cases.videos.utils import generate_new_video_hash_id_for_user


# gets signed isntructions for uploading a new video file
def make_get_upload_video_signed_instructions(videos: VideosDB, storage: Storage) -> Callable[[UUID], FileUploadSignedInstructions]:
    async def get_upload_video_signed_instructions(authenticated_user_id: UUID) -> FileUploadSignedInstructions:
        hash_id = await generate_new_video_hash_id_for_user(videos=videos, user_id=authenticated_user_id)

        object_key = f'{authenticated_user_id}/{hash_id}'

        return await storage.get_upload_file_signed_instructions(
            item_relative_path=object_key
        )

    return get_upload_video_signed_instructions
