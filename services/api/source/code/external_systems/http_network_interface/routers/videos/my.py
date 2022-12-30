from fastapi import APIRouter, status, Depends
from functools import partial
from uuid import UUID
from entities.videos import Video, UserVideosList
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import authenticated_user
from external_systems.data_access.rds.pg.videos import videos_db_client
from external_systems.data_access.storage.s3.videos import videos_s3_client
from use_cases.videos.get_authenticated_user_videos import get_authenticated_user_videos_use_case
from use_cases.videos.update_video import update_video_use_case
from use_cases.videos.delete_video import delete_video_use_case

router = APIRouter()


# get authenticated user videos
get_authenticated_user_videos_uc = partial(get_authenticated_user_videos_use_case, database=videos_db_client)
#
@router.get("/", response_model=UserVideosList, response_model_exclude_none=True, responses={
    status.HTTP_401_UNAUTHORIZED: {}
})
async def get_authenticated_user_videos(
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> UserVideosList:
    return await get_authenticated_user_videos_uc(
        authenticated_user_id=authenticated_user_id
    )


# update a video
update_video_uc = partial(update_video_use_case, database=videos_db_client)
#
@router.put("/{hash_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_401_UNAUTHORIZED: {},
    status.HTTP_404_NOT_FOUND: {},
    status.HTTP_400_BAD_REQUEST: {}
})
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
delete_video_uc = partial(delete_video_use_case, database=videos_db_client)
#
@router.delete('/{hash_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_401_UNAUTHORIZED: {},
    status.HTTP_404_NOT_FOUND: {},
    status.HTTP_425_TOO_EARLY: {}
})
async def delete_video(
    hash_id: UUID,
    authenticated_user_id: UUID = Depends(authenticated_user)
) -> None:
    await delete_video_uc(
        authenticated_user_id=authenticated_user_id,
        hash_id=hash_id
    )
