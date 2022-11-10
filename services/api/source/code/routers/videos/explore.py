from environment import constants
from typing import List, Optional
from fastapi import APIRouter, Request
from rds import videos
from models import Video

router = APIRouter()

# explore all videos which are already listed
@router.get("/", response_model=List[Video], response_model_exclude_none=True)
async def explore_listed_videos(request: Request, include_my: Optional[bool] = False) -> List[Video]:
    authenticated_user_id: str = request.state.auth_user_id

    # hide authenticated user listed videos by default
    allow_privates_of_user_id = None
    
    if include_my and not authenticated_user_id.__eq__(constants.ANONYMOUS_USER):
        allow_privates_of_user_id = authenticated_user_id

    return await videos.get_listed_videos(allow_privates_of_user_id=allow_privates_of_user_id)
