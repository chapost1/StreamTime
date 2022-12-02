from fastapi import APIRouter, Depends, status
from typing import Union
from uuid import UUID
from entities.videos import WatchVideoRecord
from external_systems.data_access.rds.pg.videos import videos_db_client
from external_systems.data_access.storage.s3.videos import videos_s3_client
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import any_user
from use_cases.videos.get_watch_video_record import make_get_watch_video_record

router = APIRouter()


# watch a video
get_watch_video_record_uc = make_get_watch_video_record(database=videos_db_client, storage=videos_s3_client)
#
@router.get('/', response_model=WatchVideoRecord, response_model_exclude_none=True, responses={
    status.HTTP_404_NOT_FOUND: {},
    status.HTTP_403_FORBIDDEN: {}
})
async def get_watch_video_record(
    user_id: UUID,
    hash_id: UUID,
    authenticated_user_id: Union[UUID, str] = Depends(any_user)
) -> WatchVideoRecord:
    return await get_watch_video_record_uc(
        authenticated_user_id=authenticated_user_id,
        user_id=user_id,
        hash_id=hash_id
    )
