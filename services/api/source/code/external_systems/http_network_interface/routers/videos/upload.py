from entities.storage import (
    FileUploadSignedInstructions,
    VideoUploadConfigRecord
)
from functools import partial
from fastapi import APIRouter, Depends, status
from uuid import UUID
from external_systems.data_access.rds.pg.videos import videos_db_client
from external_systems.data_access.storage.s3.videos import videos_s3_client
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import authenticated_user
from use_cases.videos.get_upload_file_signed_instructions import get_upload_video_signed_instructions_use_case
from use_cases.videos.get_video_upload_config import get_video_upload_config_use_case

router = APIRouter()


# get upload a video signatures
get_upload_video_signed_instructions_uc = partial(
    get_upload_video_signed_instructions_use_case,
    database=videos_db_client,
    storage=videos_s3_client
)
#
@router.get('/', response_model=FileUploadSignedInstructions, responses={
    status.HTTP_401_UNAUTHORIZED: {},
    status.HTTP_400_BAD_REQUEST: {}
})
async def get_upload_video_signed_instructions(
    file_content_type: str,
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> FileUploadSignedInstructions:
    return await get_upload_video_signed_instructions_uc(
        authenticated_user_id=authenticated_user_id,
        file_content_type=file_content_type
    )


# get supported config to upload a video
get_video_upload_config_uc = get_video_upload_config_use_case
#
@router.get('/config', response_model=VideoUploadConfigRecord, responses={
    status.HTTP_401_UNAUTHORIZED: {}
})
async def get_video_upload_config(
    _: UUID = Depends(authenticated_user)
) -> VideoUploadConfigRecord:
    return await get_video_upload_config_uc()
