from models.storage import FileUploadUrlRecord
from fastapi import APIRouter, Depends
from uuid import UUID
from ..auth_guards import authenticated_user
from use_cases.videos import get_upload_video_url_uc

router = APIRouter()

# upload a video, cosider, maybe return a dataclass...
@router.get('/', response_model=FileUploadUrlRecord)
async def get_upload_video_url(
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> FileUploadUrlRecord:
    return await get_upload_video_url_uc(authenticated_user_id=authenticated_user_id)
