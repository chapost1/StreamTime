from rds.connection.connection import Connection
from typing import List, Dict
from models import Video, UnprocessedVideo, SortKeys
from rds.videos import tables
from common.utils import nl


async def explore_listed_videos(allow_privates_of_user_id: str) -> List[Video]:
    private_visibility_conditions = ['is_private is not true']
    params = []
    if allow_privates_of_user_id is not None:
        # allow authenticated user to see his private videos
        private_visibility_conditions.append('user_id = %s')
        params.append(allow_privates_of_user_id)

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
                    upload_time,
                    is_private,
                    listing_time
               FROM {tables.VIDEOS_TABLE}
               WHERE listing_time is not null
               AND ({' OR '.join(private_visibility_conditions)})
               ORDER BY listing_time DESC""",
            tuple(params)
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
        upload_time=video[8],
        is_private=video[9],
        listing_time=video[10]
    ), videos))


async def get_user_unprocessed_videos(user_id: str) -> List[UnprocessedVideo]:
    videos = await Connection().query([
        (
            f"""SELECT 
                    hash_id,
                    user_id,
                    upload_time,
                    failure_reason
               FROM {tables.UNPROCESSED_VIDEOS_TABLE}
               WHERE user_id = %s
               ORDER BY upload_time DESC""",
            tuple([user_id])
        )
    ])

    return list(map(lambda video: UnprocessedVideo(
        hash_id=video[0],
        user_id=video[1],
        upload_time=video[2],
        failure_reason=video[3]
    ), videos))


async def get_user_videos(user_id: str, hide_private: bool, listed_only: bool, sort_key: SortKeys) -> List[UnprocessedVideo]:
    conditions = ['user_id = %s']
    params = [user_id]
    if hide_private:
        conditions.append('is_private is not true')
    if listed_only:
        conditions.append('listing_time is not null')

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
                    upload_time,
                    is_private,
                    listing_time
               FROM {tables.VIDEOS_TABLE}
               WHERE {f'{nl()}AND '.join(conditions)}
               ORDER BY {sort_key.value} DESC""",
            tuple(params)
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
        upload_time=video[8],
        is_private=video[9],
        listing_time=video[10]
    ), videos))


async def get_video(user_id: str, hash_id: str) -> Video:
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
                    upload_time,
                    is_private,
                    listing_time
               FROM {tables.VIDEOS_TABLE}
               WHERE user_id = %s
               AND hash_id = %s
               ORDER BY listing_time DESC""",
            tuple([user_id, hash_id])
        )
    ])

    if len(videos) < 1:
        return None

    video = videos[0]
    return Video(
        hash_id=video[0],
        user_id=video[1],
        title=video[2],
        description=video[3],
        size_in_bytes=video[4],
        duration_seconds=video[5],
        video_type=video[6],
        thumbnail_url=video[7],
        upload_time=video[8],
        is_private=video[9],
        listing_time=video[10]
    )


async def update_video(user_id: str, hash_id: str, to_update: Dict) -> None:
    to_update_statement = []
    params = []
    for field, value in to_update.items():
        to_update_statement.append(f'{field} = %s')
        params.append(value)
    
    if len(to_update_statement) < 1:
        # skip
        return None
    
    where_condition = []

    where_condition.append('user_id = %s')
    params.append(user_id)

    where_condition.append('hash_id = %s')
    params.append(hash_id)

    await Connection().execute([
        (
            f"""UPDATE {tables.VIDEOS_TABLE}
                SET {', '.join(to_update_statement)}
                WHERE {f'{nl()}AND '.join(where_condition)};""",
            tuple(params)
        )
    ])

    return None
