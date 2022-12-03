from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.videos import VideosDescriber
from external_systems.data_access.rds.abstract.videos import UnprocessedVideosDescriber
from external_systems.data_access.rds.pg.videos.describers import VideosDescriberPG
from external_systems.data_access.rds.pg.videos.describers import UnprocessedVideosDescriberPG
from entities.videos import VideoStages
from external_systems.data_access.rds.pg.videos import tables
from uuid import UUID


class VideosDatabasePG:
    f"""
    VideosDatabase database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {VideosDatabase.__doc__}
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


    def describe_videos(self) -> VideosDescriber:
        return VideosDescriberPG()
    

    def describe_unprocessd_videos(self) -> UnprocessedVideosDescriber:
        return UnprocessedVideosDescriberPG()
