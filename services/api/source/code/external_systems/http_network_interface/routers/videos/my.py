from fastapi import APIRouter, status, Depends
from uuid import UUID
from entities.videos import Video, UserVideosList
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import authenticated_user
from external_systems.data_access.rds.pg.videos import videos_db_client
from external_systems.data_access.storage.s3.videos import videos_s3_client
from use_cases.videos.get_authenticated_user_videos import make_get_authenticated_user_videos
from use_cases.videos.update_video import make_update_video
from use_cases.videos.delete_video import make_delete_video

router = APIRouter()


# get authenticated user videos
get_authenticated_user_videos_uc = make_get_authenticated_user_videos(database=videos_db_client)
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
update_video_uc = make_update_video(database=videos_db_client)
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
delete_video_uc = make_delete_video(database=videos_db_client, storage=videos_s3_client)
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
