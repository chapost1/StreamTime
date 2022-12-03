from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from typing import Union, Callable, List
from entities.videos import WatchVideoRecord, Video
from common.app_errors import NotFoundError, AccessDeniedError
from external_systems.data_access.storage.abstract import Storage
from use_cases.videos.utils import get_cross_users_visibility_settings


def make_get_watch_video_record(database: VideosDatabase, storage: Storage) -> Callable[[Union[UUID, str], UUID, UUID], WatchVideoRecord]:
    """Creates Get Watch Video Record use case"""

    async def get_watch_video_record(authenticated_user_id: Union[UUID, str], user_id: UUID, hash_id: UUID) -> WatchVideoRecord:  
        """
        Gets Watch Video record

        It holds a presigned watchable url.
        It is needed to grant premission to access (watch) to the video assets storage
        """

        visibility_settings = get_cross_users_visibility_settings(
            authenticated_user_id=authenticated_user_id,
            user_id=user_id
        )

        videos: List[Video] = await (
            database.describe_videos()
            .with_hash(id=hash_id)
            .owned_by(user_id=user_id)
            .include_privates_of(user_id=authenticated_user_id)
            .search()
        )
        if len(videos) < 1:
            raise NotFoundError()

        video: Video = videos[0]

        if not video.is_listed() and visibility_settings.hide_unlisted:
            raise AccessDeniedError()
        
        if video.is_private and visibility_settings.hide_private:
            raise AccessDeniedError()

        eighteen_hours_in_seconds = 18 * 3600
        # videos assets are private by default.
        # therefore, we need to create a signed link to let the user watch the asset
        watchable_url = await storage.get_file_signed_url(
            item_relative_path=video._storage_object_key,
            signature_duration_seconds=min(eighteen_hours_in_seconds, video.duration_seconds * 3)
        )

        return WatchVideoRecord(
            video=video,
            watchable_url=watchable_url
        )

    return get_watch_video_record
