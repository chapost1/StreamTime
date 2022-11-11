from typing import List, Union
from fastapi import APIRouter, Depends
from uuid import UUID
from models import Video
from ..auth_guards import any_user
from use_cases.videos import get_specific_user_videos_uc

router = APIRouter()

# get specific user videos
@router.get('/{user_id}', response_model=List[Video], response_model_exclude_none=True)
async def get_specific_user_videos(
    user_id: UUID,
    authenticated_user_id: Union[UUID, str] = Depends(any_user)
) -> List[Video]:
    return await get_specific_user_videos_uc(
        authenticated_user_id=authenticated_user_id,
        user_id=user_id
    )
