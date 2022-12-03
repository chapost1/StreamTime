from entities.videos import Video
from uuid import UUID
from typing import Callable, List
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from use_cases.validation_utils import required_fields_validator
from common.utils import calc_server_time
from common.app_errors import (InputError, NotFoundError)


def make_update_video(database: VideosDatabase) -> Callable[[UUID, Video, UUID], None]:
    """Creates Upade a Video use case"""

    async def update_video(authenticated_user_id: UUID, video: Video, hash_id: UUID) -> None:
        """Updates an existing video"""

        # TODO: support new thumbnail selection

        videos: List[Video] = await (
            database.videos()
            .with_hash(id=hash_id)
            .owned_by(user_id=authenticated_user_id)
            .include_privates_of(user_id=authenticated_user_id)
            .search()
        )
        if len(videos) < 1:
            raise NotFoundError()

        existing_video: Video = videos[0]

        if not existing_video.is_listed():
            # assert requried fields for new listing are not missing
            video.listing_time = calc_server_time()
            errors = required_fields_validator(video.dict(exclude_none=True), Video.REQUIRED_FIELDS_ON_LISTING)
            if errors is not None:
                raise InputError(details={
                    'errors': errors
                })

        # filter-in allowed update fields, to avoid update of forbidden fields
        to_update = video.dict(include=Video.ALLOWED_UPDATE_FIELDS, exclude_none=True)

        await (
            database.videos()
            .with_hash(id=hash_id)
            .owned_by(user_id=authenticated_user_id)
            .update(to_update=to_update)
        )

    return update_video
