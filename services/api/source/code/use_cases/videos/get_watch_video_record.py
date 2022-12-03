from uuid import UUID
from common.constants import MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
from external_systems.data_access.rds.abstract.videos import VideosDescriber
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from typing import Union, Callable
from entities.videos import WatchVideoRecord, Video
from common.app_errors import AccessDeniedError
from external_systems.data_access.storage.abstract import Storage
from common.utils import find_one
from use_cases.validation_utils import is_same_user


def make_get_watch_video_record(database: VideosDatabase, storage: Storage) -> Callable[[Union[UUID, str], UUID, UUID], WatchVideoRecord]:
    """Creates Get Watch Video Record use case"""

    async def get_watch_video_record(authenticated_user_id: Union[UUID, str], user_id: UUID, hash_id: UUID) -> WatchVideoRecord:  
        """
        Gets Watch Video record

        It holds a presigned watchable url.
        It is needed to grant premission to access (watch) to the video assets storage
        """

        videos_describer: VideosDescriber = (
            database.describe_videos()
            .with_hash(id=hash_id)
            .owned_by(user_id=user_id)
            .filter_unlisted(flag=True)
            .include_privates_of(user_id=authenticated_user_id)
        )

        video: Video = find_one(
            items=await videos_describer.search()
        )

        if video.is_private and not is_same_user(id_a=authenticated_user_id, id_b=user_id):
            raise AccessDeniedError()

        # videos assets are private by default.
        # we want to let users to see any videos which day have permissions to
        # therefore, we need to create a signed link to let the user watch the asset
        watchable_url = await storage.get_file_signed_url(
            item_relative_path=video._storage_object_key,
            signature_duration_seconds=MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
        )

        return WatchVideoRecord(
            video=video,
            watchable_url=watchable_url
        )

    return get_watch_video_record
