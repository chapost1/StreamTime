from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.abstract.videos import VideosDB
from external_systems.data_access.rds.abstract.videos import VideosExplorer
from external_systems.data_access.rds.abstract.videos import UnprocessedVideosExplorer
from external_systems.data_access.rds.pg.videos.videos_explorer import VideosExplorerPG
from external_systems.data_access.rds.pg.videos.unprocessed_videos_explorer import UnprocessedVideosExplorerPG
from typing import Dict
from entities.videos import VideoStages
from external_systems.data_access.rds.pg.videos import tables
from common.utils import nl
from uuid import UUID


class VideosPG:
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


    def videos(self) -> VideosExplorer:
        return VideosExplorerPG()
    

    def unprocessd_videos(self) -> UnprocessedVideosExplorer:
        return UnprocessedVideosExplorerPG()


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
