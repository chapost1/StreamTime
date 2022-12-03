from typing import List, Union, Optional
from fastapi import APIRouter, Depends, status
from uuid import UUID
from entities.videos import Video
from external_systems.data_access.rds.pg.videos import videos_db_client
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import any_user
from use_cases.videos.get_specific_user_listed_videos import make_get_specific_user_listed_videos

router = APIRouter()


# get specific user videos
get_specific_user_listed_videos_uc = make_get_specific_user_listed_videos(database=videos_db_client)
#
@router.get('/{user_id}', response_model=List[Video], response_model_exclude_none=True, responses={
    status.HTTP_404_NOT_FOUND: {}
})
async def get_specific_user_videos(
    user_id: UUID,
    pagination_index_is_smaller_than: Optional[int] = None,
    authenticated_user_id: Union[UUID, str] = Depends(any_user)
) -> List[Video]:
    return await get_specific_user_listed_videos_uc(
        authenticated_user_id=authenticated_user_id,
        pagination_index_is_smaller_than=pagination_index_is_smaller_than,
        user_id=user_id
    )
