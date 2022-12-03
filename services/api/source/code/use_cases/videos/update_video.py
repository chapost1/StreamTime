from entities.videos import Video
from uuid import UUID
from typing import Callable
from external_systems.data_access.rds.abstract.videos import VideosDescriber
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from use_cases.validation_utils import assert_required_fields
from common.utils import (
    calc_server_time,
    find_one
)


def make_update_video(database: VideosDatabase) -> Callable[[UUID, Video, UUID], None]:
    """Creates Upade a Video use case"""

    async def update_video(authenticated_user_id: UUID, video: Video, hash_id: UUID) -> None:
        """Updates an existing video"""

        # TODO: support new thumbnail selection

        videos_describer: VideosDescriber = (
            database.describe_videos()
            .with_hash(id=hash_id)
            .owned_by(user_id=authenticated_user_id)
            .include_privates_of(user_id=authenticated_user_id)
        )

        existing_video: Video = find_one(
            items=await videos_describer.search()
        )

        if not existing_video.is_listed():
            # assert new listing has required fields
            assert_required_fields(video.dict(exclude_none=True), Video.REQUIRED_FIELDS_ON_LISTING)
            video.listing_time = calc_server_time()

        # filter-in allowed update fields, to avoid update of forbidden fields
        new_desired_state = video.dict(include=Video.ALLOWED_UPDATE_FIELDS, exclude_none=True)

        await videos_describer.update(new_desired_state=new_desired_state)

    return update_video
