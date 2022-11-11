from typing import Dict
from fastapi import APIRouter, Depends
from uuid import UUID
from ..auth_guards import authenticated_user
from use_cases.videos import get_upload_video_url_uc

router = APIRouter()

# upload a video, cosider, maybe return a dataclass...
@router.get('/', response_model=Dict)
async def get_upload_video_url(
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> Dict:
    return await get_upload_video_url_uc(authenticated_user_id=authenticated_user_id)
