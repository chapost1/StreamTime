from data_access.rds.connection.connection import Connection
from typing import List, Dict
from models import Video, UnprocessedVideo, SortKeys, VideoStages
from data_access.rds.videos import tables
from common.utils import nl
from uuid import UUID

class Videos:
    async def find_video_stage(self, user_id: UUID, hash_id: UUID) -> VideoStages:
        stages = await Connection().query([
            (
                f"""
                SELECT stage FROM (
                    SELECT '{VideoStages.UNPROCESSED.value}' as stage FROM {tables.UNPROCESSED_VIDEOS_TABLE}
                    WHERE user_id = %s
                    AND hash_id = %s
                ) as unprocessed
                UNION ALL
                SELECT stage FROM (
                    SELECT '{VideoStages.READY.value}' as stage FROM {tables.VIDEOS_TABLE}
                    WHERE user_id = %s
                    AND hash_id = %s
                ) as ready;
                """,
                tuple([user_id, hash_id, user_id, hash_id])
            )
        ])

        if len(stages) < 1:
            return None

        return list(map(lambda tup: tup[0], stages))

    async def get_listed_videos(self, allow_privates_of_user_id: UUID, exclude_user_id: UUID) -> List[Video]:
        conditions = []
        params = []
        if allow_privates_of_user_id is not None:
            # allow private visibility:
            # if this is not the allowed user, show only public (not private)
            # else, show for the auth user, anything
            conditions.append('((user_id != %s AND is_private is not true) OR (user_id = %s))')
            params.append(allow_privates_of_user_id)
            params.append(allow_privates_of_user_id)
        
        if exclude_user_id is not None:
            # hide anything which is related to the excluded user_id
            conditions.append('user_id != %s')
            params.append(exclude_user_id)

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
                AND ({f'{nl()}AND '.join(conditions)})
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


    async def get_user_unprocessed_videos(self, user_id: UUID) -> List[UnprocessedVideo]:
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


    async def get_user_videos(self, user_id: UUID, hide_private: bool, listed_only: bool, sort_key: SortKeys) -> List[UnprocessedVideo]:
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


    async def get_video(self, user_id: UUID, hash_id: UUID) -> Video:
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


    async def update_video(self, user_id: UUID, hash_id: UUID, to_update: Dict) -> None:
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
