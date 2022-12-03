from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.abstract import VideosDB
from typing import List, Dict
from entities.videos import Video, UnprocessedVideo, VideoStages
from external_systems.data_access.rds.pg.videos import tables
from common.utils import nl
from uuid import UUID


class Videos:
    f"""
    Videos database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {VideosDB.__doc__}
    """

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

    async def get_listed_videos(
        self,
        allow_privates_of_user_id: UUID,
        exclude_user_id: UUID,
        pagination_index_is_smaller_than: int,
        limit: int
    ) -> List[Video]:
        base_conditions = []
        visibility_conditions = []
        params = []

        # pagination index should be first as it should truncate the query window lookup
        if pagination_index_is_smaller_than is not None:
            if pagination_index_is_smaller_than < 1:
                # pagination index range is [1, INT_MAX]
                # therefore, smaller than 1 means return nothing
                return []
            base_conditions.append('pagination_index < %s')
            params.append(pagination_index_is_smaller_than)
        
        # assert query will return listed videos only
        base_conditions.append('listing_time is not null')

        if allow_privates_of_user_id is not None:
            # authenticated user
            # allow private visibility:
            # if this is not the allowed user, show only public (not private)
            # else, show for the auth user, anything
            visibility_conditions.append('((user_id != %s AND is_private is not true) OR (user_id = %s))')
            params.append(allow_privates_of_user_id)
            params.append(allow_privates_of_user_id)
        else:
            # anonymous user, do not allow privates at all
            visibility_conditions.append('is_private is not true')
        
        if exclude_user_id is not None:
            # hide anything which is related to the excluded user_id
            visibility_conditions.append('user_id != %s')
            params.append(exclude_user_id)
        

        # keep limit as the last param, as it is the last sql expression
        params.append(limit)

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
                        storage_object_key,
                        storage_thumbnail_key,
                        upload_time,
                        is_private,
                        listing_time,
                        pagination_index
                FROM {tables.VIDEOS_TABLE}
                WHERE {f'{nl()}AND '.join(base_conditions)}
                AND ({f'{nl()}AND '.join(visibility_conditions)})
                ORDER BY pagination_index DESC
                LIMIT %s""",
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
            _storage_object_key=video[8],
            _storage_thumbnail_key=video[9],
            upload_time=video[10],
            is_private=video[11],
            listing_time=video[12],
            pagination_index=video[13]
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


    async def get_user_videos(
        self,
        user_id: UUID,
        hide_private: bool,
        hide_unlisted: bool,
        pagination_index_is_smaller_than: int,
        limit: int
    ) -> List[UnprocessedVideo]:
        conditions = ['user_id = %s']
        params = [user_id]

        # pagination index can appear also after user_id as it is an maintained index on pg side (user_id)
        if pagination_index_is_smaller_than is not None:
            if pagination_index_is_smaller_than < 1:
                # pagination index range is [1, INT_MAX]
                # therefore, smaller than 1 means return nothing
                return []
            conditions.append('pagination_index < %s')
            params.append(pagination_index_is_smaller_than)

        if hide_private:
            conditions.append('is_private is not true')

        if hide_unlisted:
            conditions.append('listing_time is not null')

        # keep limit as the last param, as it is the last sql expression
        params.append(limit)

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
                        storage_object_key,
                        storage_thumbnail_key,
                        upload_time,
                        is_private,
                        listing_time,
                        pagination_index
                FROM {tables.VIDEOS_TABLE}
                WHERE {f'{nl()}AND '.join(conditions)}
                ORDER BY pagination_index DESC
                LIMIT %s""",
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
            _storage_object_key=video[8],
            _storage_thumbnail_key=video[9],
            upload_time=video[10],
            is_private=video[11],
            listing_time=video[12],
            pagination_index=video[13]
        ), videos))


    async def get_unprocessed_video(self, user_id: UUID, hash_id: UUID) -> UnprocessedVideo:
        videos = await Connection().query([
            (
                f"""SELECT 
                        hash_id,
                        user_id,
                        upload_time,
                        failure_reason
                FROM {tables.UNPROCESSED_VIDEOS_TABLE}
                WHERE user_id = %s
                AND hash_id = %s""",
                tuple([user_id, hash_id])
            )
        ])

        if len(videos) < 1:
            return None

        video = videos[0]
        return UnprocessedVideo(
            hash_id=video[0],
            user_id=video[1],
            upload_time=video[2],
            failure_reason=video[3]
        )


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
                        storage_object_key,
                        storage_thumbnail_key,
                        upload_time,
                        is_private,
                        listing_time,
                        pagination_index
                FROM {tables.VIDEOS_TABLE}
                WHERE user_id = %s
                AND hash_id = %s""",
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
            _storage_object_key=video[8],
            _storage_thumbnail_key=video[9],
            upload_time=video[10],
            is_private=video[11],
            listing_time=video[12],
            pagination_index=video[13]
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
    

    async def delete_video_by_stage(self, user_id: UUID, hash_id: UUID, stage: VideoStages) -> None:
        table = tables.video_stages_to_table(stage)
        
        if table is None:
            raise Exception(f'invalid video stage found. {user_id}/{hash_id} in stage [{stage}]')

        await Connection().execute([
            (
                f"""DELETE FROM {table}
                    WHERE user_id = %s
                    AND hash_id = %s;""",
                tuple([user_id, hash_id])
            )
        ])
