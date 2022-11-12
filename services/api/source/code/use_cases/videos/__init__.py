from environment import environment
from data_access.rds.pg import Videos
from data_access.storage.s3.client import S3
from data_access.storage.s3.context import Context

videos_s3_client = S3(Context(
    bucket=environment.VIDEOS_BUCKET,
    upload_prefix=environment.UPLOADDED_VIDEOS_PREFIX
))
videos = Videos()

# explore
from use_cases.videos.explore_listed_videos import make_explore_listed_videos
explore_listed_videos_uc = make_explore_listed_videos(videos=videos)

# my
from use_cases.videos.get_authenticated_user_videos import make_get_authenticated_user_videos
get_authenticated_user_videos_uc = make_get_authenticated_user_videos(videos=videos)

from use_cases.videos.update_video import make_update_video
update_video_uc = make_update_video(videos=videos)

from use_cases.videos.delete_video import make_delete_video
delete_video_uc = make_delete_video(videos=videos)

# upload
from use_cases.videos.get_upload_url import make_get_upload_video_signed_instructions
get_upload_video_signed_instructions_uc = make_get_upload_video_signed_instructions(videos=videos, storage=videos_s3_client)

# user
from use_cases.videos.get_specific_user_videos import make_get_specific_user_videos
get_specific_user_videos_uc = make_get_specific_user_videos(videos=videos)

# watch
from use_cases.videos.get_watch_video_record import make_get_watch_video_record
get_watch_video_record_uc = make_get_watch_video_record(videos=videos)
