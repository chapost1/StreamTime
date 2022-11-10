from environment import constants
from typing import List
from fastapi import APIRouter, Request, HTTPException, status
from rds import videos
from uuid import UUID
from models import Video, UserVideosList, SortKeys
from common.utils import calc_server_time
from .validation_utils import required_fields_validator

router = APIRouter(tags=["Video"])


# explore all videos which are already listed
@router.get("/", response_model=List[Video], response_model_exclude_none=True)
async def explore_listed_videos(request: Request) -> List[Video]:
    authenticated_user_id: str = request.state.auth_user_id
    if authenticated_user_id.__eq__(constants.ANONYMOUS_USER):
        # if not anonymous allow user see it's litings
        authenticated_user_id = None

    return await videos.explore_listed_videos(allow_privates_of_user_id=authenticated_user_id)


# get auth user videos
@router.get("/my", response_model=UserVideosList, response_model_exclude_none=True)
async def get_authenticated_user_videos(request: Request) -> UserVideosList:
    authenticated_user_id: str = request.state.auth_user_id
    if authenticated_user_id.__eq__(constants.ANONYMOUS_USER):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    
    return UserVideosList(
        unprocessed_videos=await videos.get_user_unprocessed_videos(user_id=authenticated_user_id),
        videos=await videos.get_user_videos(
            user_id=authenticated_user_id,
            hide_private=False,
            listed_only=False,
            sort_key=SortKeys.upload_time
        )
    )


# get specific user videos
@router.get("/{user_id}", response_model=List[Video], response_model_exclude_none=True)
async def get_specific_user_videos(request: Request, user_id: UUID) -> List[Video]:
    authenticated_user_id: str = request.state.auth_user_id

    if authenticated_user_id.__eq__(user_id):
        hide_private = False
        listed_only = False
        sort_key = SortKeys.upload_time
    else:
        print(authenticated_user_id)
        print(user_id)
        hide_private = True
        listed_only = True
        sort_key = SortKeys.listing_time

    return await videos.get_user_videos(
        user_id=user_id,
        hide_private=hide_private,
        listed_only=listed_only,
        sort_key=sort_key
    )


# put video (using the hash_id of one which is not listed (check it out) && user_id(is already known))
@router.put("/{hash_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_video(request: Request, video: Video, hash_id: UUID) -> None:# 204
    # todo: support new thumbnail selection

    authenticated_user_id: str = request.state.auth_user_id
    if authenticated_user_id == constants.ANONYMOUS_USER:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    existing_video: Video = await videos.get_video(user_id=authenticated_user_id, hash_id=hash_id)
    if existing_video is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if not existing_video.is_listed():
        # requried fields for new listing
        video.listing_time = calc_server_time()
        errors = required_fields_validator(video.dict(exclude_none=True), ['title', 'description'])
        if errors is not None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {
                'errors': errors
            })

    # allowed update fields
    to_update = video.dict(include={'title', 'description', 'listing_time', 'is_private'}, exclude_none=True)

    await videos.update_video(user_id=authenticated_user_id, hash_id=hash_id, to_update=to_update)


# todo implement:

# request upload video premission (will return presigned url) (will require nothing)

# delete video / unprocessed video (will be known because of user_id/hash_id combo)

# /watch video (return meta and watch presigned url, check if not private or actual user.)
