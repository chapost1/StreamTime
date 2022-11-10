from fastapi import APIRouter, Request, HTTPException, status, Depends
from rds import videos
from uuid import UUID
from models import Video, UserVideosList, SortKeys
from common.utils import calc_server_time
from ..validation_utils import required_fields_validator
from ..auth_guards import authenticated_user

router = APIRouter()

# get auth user videos
@router.get("/", response_model=UserVideosList, response_model_exclude_none=True)
async def get_authenticated_user_videos(authenticated_user_id: str = Depends(authenticated_user)) -> UserVideosList:
    return UserVideosList(
        unprocessed_videos=await videos.get_user_unprocessed_videos(user_id=authenticated_user_id),
        videos=await videos.get_user_videos(
            user_id=authenticated_user_id,
            hide_private=False,
            listed_only=False,
            sort_key=SortKeys.upload_time
        )
    )

# put video (using the hash_id of one which is not listed (check it out) && user_id(is already known))
@router.put("/{hash_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_video(video: Video, hash_id: UUID, authenticated_user_id: str = Depends(authenticated_user)) -> None:
    # todo: support new thumbnail selection

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


# delete a video
@router.delete("/{hash_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(request: Request, hash_id: UUID, authenticated_user_id: str = Depends(authenticated_user)) -> None:

    """todo: implement""" # consider the case of hash_id in unprocessed / videos
