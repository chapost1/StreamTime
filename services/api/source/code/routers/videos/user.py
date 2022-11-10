from typing import List
from fastapi import APIRouter, Depends
from rds import videos
from uuid import UUID
from models import Video, SortKeys
from ..auth_guards import any_user

router = APIRouter()

# get specific user videos
@router.get("/{user_id}", response_model=List[Video], response_model_exclude_none=True)
async def get_specific_user_videos(user_id: UUID, authenticated_user_id: str = Depends(any_user)) -> List[Video]:
    # build visibility settings by matching selected user id to the viewer
    if authenticated_user_id.__eq__(user_id):
        hide_private = False
        listed_only = False
        sort_key = SortKeys.upload_time
    else:
        hide_private = True
        listed_only = True
        sort_key = SortKeys.listing_time

    return await videos.get_user_videos(
        user_id=user_id,
        hide_private=hide_private,
        listed_only=listed_only,
        sort_key=sort_key
    )
