from uuid import UUID
from common.constants import MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
from common.utils import find_one
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from typing import Union
from entities.videos import WatchVideoRecord, Video
from common.app_errors import AccessDeniedError
from external_systems.data_access.storage.abstract import Storage
from use_cases.videos.get_watch_video_record.helpers.abstract import (
    IsAccessAllowedFunction
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    storage: Storage,
    is_access_allowed_fn: IsAccessAllowedFunction,
    # usage scope
    authenticated_user_id: Union[UUID, str],
    user_id: UUID,
    hash_id: UUID
) -> WatchVideoRecord:
    """
    Gets Watch Video record

    It holds a presigned watchable url.
    It is needed to grant premission to access (watch) to the video assets storage
    """

    videos, _ = await database.get_videos(
        include_user_id=user_id,
        include_hash_id=hash_id,
        filter_unlisted=True,
        include_privates_of_user_id=authenticated_user_id
    )

    video: Video = find_one(
        items=videos
    )

    is_access_denied = not is_access_allowed_fn(
        authenticated_user_id=authenticated_user_id,
        owner_user_id=user_id,
        is_private=video.is_private
    )
    if is_access_denied:
        raise AccessDeniedError()

    # videos assets are private by default.
    # we want to let users to see any videos which day have permissions to
    # therefore, we need to create a signed link to let the user watch the asset
    watchable_url = await storage.get_file_signed_url(
        item_relative_path=video.storage_object_key,
        signature_duration_seconds=MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
    )

    return WatchVideoRecord(
        video=video,
        watchable_url=watchable_url
    )
