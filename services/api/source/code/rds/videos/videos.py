from rds.connection.connection import Connection
from typing import List
from models.video import Video
from rds.videos.tables import VIDEOS_TABLE

async def get_listed_videos() -> List[Video]:
    videos = await Connection().query([
        (
            f"""SELECT 
                    hash_id,
                    user_id,
                    title,
                    description,
                    size_in_bytes,
                    duration_seconds,
                    video_type,
                    thumbnail_url,
                    upload_time
               FROM {VIDEOS_TABLE}
               WHERE is_listed is true""",
            None
        )
    ])

    return list(map(lambda video: Video(
        hash_id=video[0],
        user_id=video[1],
        title=video[2],
        description=video[3],
        size_in_bytes=video[4],
        duration_seconds=video[5],
        video_type=video[6],
        thumbnail_url=video[7],
        upload_time=video[8]
    ), videos))
