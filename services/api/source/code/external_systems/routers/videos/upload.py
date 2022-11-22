from entities.storage import (
    FileUploadSignedInstructions,
    VideoUploadConfigRecord
)
from fastapi import APIRouter, Depends
from uuid import UUID
from external_systems.routers.videos.data_accessors import videos_db_client, videos_s3_client
from ..auth_guards import authenticated_user
from use_cases.videos.get_upload_file_signed_instructions import make_get_upload_video_signed_instructions
from use_cases.videos.get_video_upload_config import make_get_video_upload_config

router = APIRouter()


# get upload a video signatures
get_upload_video_signed_instructions_uc = make_get_upload_video_signed_instructions(videos=videos_db_client, storage=videos_s3_client)
@router.get('/', response_model=FileUploadSignedInstructions)
async def get_upload_video_signed_instructions(
    file_content_type: str,
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> FileUploadSignedInstructions:
    return await get_upload_video_signed_instructions_uc(
        authenticated_user_id=authenticated_user_id,
        file_content_type=file_content_type
    )


# get supported config to upload a video
get_video_upload_config_uc = make_get_video_upload_config()
@router.get('/config', response_model=VideoUploadConfigRecord)
async def get_video_upload_config() -> VideoUploadConfigRecord:
    return await get_video_upload_config_uc()
