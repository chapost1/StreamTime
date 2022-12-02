from common.environment import SUPPORTED_VIDEO_TYPES
from uuid import UUID
from typing import Callable
from external_systems.data_access.rds.abstract import VideosDB
from external_systems.data_access.storage.abstract import Storage
from entities.storage import FileUploadSignedInstructions
from use_cases.videos.utils import generate_new_video_hash_id_for_user
from common.app_errors import InputError


def make_get_upload_video_signed_instructions(database: VideosDB, storage: Storage) -> Callable[[UUID], FileUploadSignedInstructions]:
    """Creates Get Upload Video Signed Instructions use case"""

    async def get_upload_video_signed_instructions(authenticated_user_id: UUID, file_content_type: str) -> FileUploadSignedInstructions:
        """
        Gets Signed Instructions to upload a Video

        A struct which holds a single use signed instructions to upload a Video
        It is needed to avoid free-access to the videos assets storage
        And yet to allow the users to upload a file using a single use signed instructions
        """

        if file_content_type not in SUPPORTED_VIDEO_TYPES:
            raise InputError(f'unsupported video file type::{file_content_type}, try one of these: {SUPPORTED_VIDEO_TYPES}')

        # assets the uniqueness of the new hash id
        hash_id = await generate_new_video_hash_id_for_user(database=database, user_id=authenticated_user_id)

        object_key = f'{authenticated_user_id}/{hash_id}'

        return await storage.get_upload_file_signed_instructions(
            item_relative_path=object_key,
            file_content_type=file_content_type
        )

    return get_upload_video_signed_instructions
