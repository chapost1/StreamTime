from uuid import UUID
from data_access.rds.abstract import VideosDB
from typing import Union
from models import WatchVideoRecord, Video
from common.app_errors import NotFoundError, AccessDeniedError
from data_access.storage.abstract import Storage
from use_cases.validation_utils import is_same_user

# returns the video meta data along with watchable url
def make_get_watch_video_record(videos: VideosDB, storage: Storage):
    async def get_watch_video_record(authenticated_user_id: Union[UUID, str], user_id: UUID, hash_id: UUID) -> WatchVideoRecord:        
        if is_same_user(authenticated_user_id, user_id):
            hide_private = False
            hide_unlisted = False
        else:
            hide_private = True
            hide_unlisted = True

        video: Video = await videos.get_video(user_id=user_id, hash_id=hash_id)
        if video is None or \
           not video.is_listed() and hide_unlisted:
            raise NotFoundError()
        
        if video.is_private and hide_private:
            raise AccessDeniedError()

        eighteen_hours_in_seconds = 18 * 3600
        
        watchable_url = await storage.get_file_signed_url(
            item_relative_path=video._storage_object_key,
            signature_duration_seconds=min(eighteen_hours_in_seconds, video.duration_seconds * 3)
        )

        return WatchVideoRecord(
            video=video,
            watchable_url=watchable_url
        )

    return get_watch_video_record
