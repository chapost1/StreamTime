from models.storage import (
    FileUploadSignedInstructions,
    VideoUploadConfigRecord
)
from fastapi import APIRouter, Depends
from uuid import UUID
from ..auth_guards import authenticated_user
from use_cases.videos import (
    get_upload_video_signed_instructions_uc,
    get_video_upload_config_uc
)

router = APIRouter()

# get upload a video signatures
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
@router.get('/config', response_model=VideoUploadConfigRecord)
async def get_video_upload_config() -> VideoUploadConfigRecord:
    return await get_video_upload_config_uc()
