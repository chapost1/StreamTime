from environment import constants
from typing import List, Optional
from fastapi import APIRouter, Depends
from rds import videos
from models import Video
from ..auth_guards import any_user

router = APIRouter()

# explore all videos which are already listed
@router.get("/", response_model=List[Video], response_model_exclude_none=True)
async def explore_listed_videos(include_my: Optional[bool] = False, authenticated_user_id: str = Depends(any_user)) -> List[Video]:
    is_authenticated_user = not authenticated_user_id.__eq__(constants.ANONYMOUS_USER)
        
    if is_authenticated_user:
        # let the authenticated user to view it's own private videos if he will
        # it won't appear unless user wants to see it's own videos anyway
        allow_privates_of_user_id = authenticated_user_id

        if include_my:# user wants to see its own videos while exploring
            exclude_user_id = None
        else:# user wants to excldue its videos
            exclude_user_id = authenticated_user_id

    return await videos.get_listed_videos(allow_privates_of_user_id=allow_privates_of_user_id, exclude_user_id=exclude_user_id)
