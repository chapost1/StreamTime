from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.abstract.videos import VideosDB
from external_systems.data_access.rds.abstract.videos import VideosExplorer
from external_systems.data_access.rds.pg.videos.videos_explorer import VideosExplorerPG
from typing import List, Dict, Tuple
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


    def get_videos_explorer(self) -> VideosExplorer:
        return VideosExplorerPG(self.__db_video_record_to_class)


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

        return list(map(self.__db_unprocessed_video_record_to_class, videos))


    async def get_unprocessed_video(self, user_id: UUID, hash_id: UUID) -> UnprocessedVideo:
        unprocessed_videos = await Connection().query([
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

        if len(unprocessed_videos) < 1:
            return None

        return self.__db_unprocessed_video_record_to_class(unprocessed_videos[0])


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


    def __db_video_record_to_class(self, video: Tuple) -> Video:
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


    def __db_unprocessed_video_record_to_class(self, unprocessed_video: Tuple) -> UnprocessedVideo:
        return UnprocessedVideo(
            hash_id=unprocessed_video[0],
            user_id=unprocessed_video[1],
            upload_time=unprocessed_video[2],
            failure_reason=unprocessed_video[3]
        )
