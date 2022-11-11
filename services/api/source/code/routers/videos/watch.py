from fastapi import APIRouter, Depends
from typing import Union
from uuid import UUID
from models import WatchVideoRecord
from ..auth_guards import any_user
from use_cases.videos import get_watch_video_record_uc

router = APIRouter()

# watch a video
@router.get('/', response_model=WatchVideoRecord, response_model_exclude_none=True)
async def get_watch_video_record(
    user_id: UUID,
    hash_id: UUID,
    authenticated_user_id: Union[UUID, str] = Depends(any_user)
) -> WatchVideoRecord:
    return await get_watch_video_record_uc(
        authenticated_user_id=authenticated_user_id,
        user_id=user_id,
        hash_id=hash_id
    )
