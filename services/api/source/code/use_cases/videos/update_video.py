from models import Video
from uuid import UUID
from data_access.rds.abstract import VideosDB
from use_cases.validation_utils import required_fields_validator
from common.utils import calc_server_time
from common.app_errors import (InputError, NotFoundError)


def make_update_video(videos: VideosDB):
    async def update_video(authenticated_user_id: UUID, video: Video, hash_id: UUID) -> None:
        # todo: support new thumbnail selection
        existing_video: Video = await videos.get_video(user_id=authenticated_user_id, hash_id=hash_id)
        if existing_video is None:
            raise NotFoundError()

        if not existing_video.is_listed():
            # requried fields for new listing
            video.listing_time = calc_server_time()
            errors = required_fields_validator(video.dict(exclude_none=True), ['title', 'description'])
            if errors is not None:
                 raise InputError(details={
                    'errors': errors
                })

        # allowed update fields
        to_update = video.dict(include={'title', 'description', 'listing_time', 'is_private'}, exclude_none=True)

        await videos.update_video(user_id=authenticated_user_id, hash_id=hash_id, to_update=to_update)
    return update_video
