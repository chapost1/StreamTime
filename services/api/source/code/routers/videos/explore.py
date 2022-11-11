from typing import List, Optional, Union
from fastapi import APIRouter, Depends
from models import Video
from uuid import UUID
from ..auth_guards import any_user
from use_cases.videos import explore_listed_videos_uc

router = APIRouter()

# explore all videos which are already listed
@router.get('/', response_model=List[Video], response_model_exclude_none=True)
async def explore_listed_videos(
    include_my: Optional[bool] = False,
    authenticated_user_id: Union[UUID, str] = Depends(any_user)
) -> List[Video]:
    return await explore_listed_videos_uc(
        authenticated_user_id=authenticated_user_id,
        include_my=include_my
    )
