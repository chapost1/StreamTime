from fastapi import APIRouter, status, Depends
from uuid import UUID
from models import Video, UserVideosList
from ..auth_guards import authenticated_user
from use_cases.videos import (
    get_authenticated_user_videos_uc,
    update_video_uc,
    delete_video_uc
)

router = APIRouter()

# get auth user videos
@router.get("/", response_model=UserVideosList, response_model_exclude_none=True)
async def get_authenticated_user_videos(
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> UserVideosList:
    return await get_authenticated_user_videos_uc(
        authenticated_user_id=authenticated_user_id
    )

# put video
@router.put("/{hash_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_video(
    video: Video,
    hash_id: UUID,
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> None:
    await update_video_uc(
        authenticated_user_id=authenticated_user_id,
        video=video,
        hash_id=hash_id
    )

# delete a video
@router.delete('/{hash_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(
    hash_id: UUID,
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> None:
    await delete_video_uc(
        authenticated_user_id=authenticated_user_id,
        hash_id=hash_id
    )
