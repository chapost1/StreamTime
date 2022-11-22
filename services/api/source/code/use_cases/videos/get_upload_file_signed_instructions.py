from environment.environment import SUPPORTED_VIDEO_TYPES
from uuid import UUID
from typing import Callable
from external_systems.data_access.rds.abstract import VideosDB
from external_systems.data_access.storage.abstract import Storage
from entities.storage import FileUploadSignedInstructions
from use_cases.videos.utils import generate_new_video_hash_id_for_user
from common.app_errors import InputError


# gets signed isntructions for uploading a new video file
def make_get_upload_video_signed_instructions(videos: VideosDB, storage: Storage) -> Callable[[UUID], FileUploadSignedInstructions]:
    async def get_upload_video_signed_instructions(authenticated_user_id: UUID, file_content_type: str) -> FileUploadSignedInstructions:
        if file_content_type not in SUPPORTED_VIDEO_TYPES:
            raise InputError(f'unsupported video file type::{file_content_type}, try one of these: {SUPPORTED_VIDEO_TYPES}')

        hash_id = await generate_new_video_hash_id_for_user(videos=videos, user_id=authenticated_user_id)

        object_key = f'{authenticated_user_id}/{hash_id}'

        return await storage.get_upload_file_signed_instructions(
            item_relative_path=object_key,
            file_content_type=file_content_type
        )

    return get_upload_video_signed_instructions
