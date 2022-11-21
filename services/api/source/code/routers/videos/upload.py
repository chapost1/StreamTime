from models.storage import FileUploadSignedInstructions
from fastapi import APIRouter, Depends
from uuid import UUID
from ..auth_guards import authenticated_user
from use_cases.videos import get_upload_video_signed_instructions_uc

router = APIRouter()

# upload a video, cosider, maybe return a dataclass...
@router.get('/', response_model=FileUploadSignedInstructions)
async def get_upload_video_signed_instructions(
    file_content_type: str,
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> FileUploadSignedInstructions:
    return await get_upload_video_signed_instructions_uc(
        authenticated_user_id=authenticated_user_id,
        file_content_type=file_content_type
    )
