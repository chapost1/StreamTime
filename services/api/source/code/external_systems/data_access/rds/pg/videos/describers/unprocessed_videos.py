from __future__ import annotations
from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.abstract.videos import UnprocessedVideosDescriber
from external_systems.data_access.rds.pg.videos.describers.uploaded_videos import UploadedVideosDescriberPG
from typing import List, Tuple
from entities.videos import UnprocessedVideo
from entities.videos import VideoStages
from external_systems.data_access.rds.pg.videos import tables
from common.utils import nl


class UnprocessedVideosDescriberPG(UploadedVideosDescriberPG):
    f"""
    DescribedUnprocessedVideos database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {UnprocessedVideosDescriber.__doc__}
    """

    async def search(self) -> List[UnprocessedVideo]:
        conditions, params = super().build_query_conditions_params()

        videos = await Connection().query([
            (
                f"""SELECT
                        hash_id,
                        user_id,
                        upload_time,
                        failure_reason
                FROM {tables.UNPROCESSED_VIDEOS_TABLE}
                WHERE {f'{nl()}AND '.join(conditions)}
                ORDER BY upload_time DESC""",
                tuple(params)
            )
        ])

        return list(map(self.__prase_db_records_into_classes, videos))
    

    async def delete(self) -> None:
        await super().delete(stage=VideoStages.UNPROCESSED.value)


    def __prase_db_records_into_classes(self, unprocessed_video: Tuple) -> UnprocessedVideo:
        return UnprocessedVideo(
            hash_id=unprocessed_video[0],
            user_id=unprocessed_video[1],
            upload_time=unprocessed_video[2],
            failure_reason=unprocessed_video[3]
        )
