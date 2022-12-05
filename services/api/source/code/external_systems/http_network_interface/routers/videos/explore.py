from typing import Optional, Union
from fastapi import APIRouter, Depends
from entities.videos import VideosPage
from functools import partial
from uuid import UUID
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import any_user
from external_systems.data_access.rds.pg.videos import videos_db_client
from use_cases.videos.explore_listed_videos import explore_listed_videos

router = APIRouter()


# explore listed videos
explore_listed_videos_uc = partial(explore_listed_videos, database=videos_db_client)
#
@router.get('/', response_model=VideosPage, response_model_exclude_none=True)
async def explore_listed_videos(
    next: Optional[str] = None,
    include_my: Optional[bool] = False,
    authenticated_user_id: Union[UUID, str] = Depends(any_user)
) -> VideosPage:
    return await explore_listed_videos_uc(
        authenticated_user_id=authenticated_user_id,
        next=next,
        include_my=include_my
    )
