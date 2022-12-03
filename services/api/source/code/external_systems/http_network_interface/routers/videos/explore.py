from typing import List, Optional, Union
from fastapi import APIRouter, Depends
from entities.videos import Video
from uuid import UUID
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import any_user
from external_systems.data_access.rds.pg.videos import videos_db_client
from use_cases.videos.explore_listed_videos import make_explore_listed_videos

router = APIRouter()


# explore listed videos
explore_listed_videos_uc = make_explore_listed_videos(database=videos_db_client)
#
@router.get('/', response_model=List[Video], response_model_exclude_none=True)
async def explore_listed_videos(
    pagination_index_is_smaller_than: Optional[int] = None,
    include_my: Optional[bool] = False,
    authenticated_user_id: Union[UUID, str] = Depends(any_user)
) -> List[Video]:
    return await explore_listed_videos_uc(
        authenticated_user_id=authenticated_user_id,
        pagination_index_is_smaller_than=pagination_index_is_smaller_than,
        include_my=include_my
    )
