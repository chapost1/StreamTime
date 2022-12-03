from __future__ import annotations
from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.abstract.videos import UnprocessedVideosExplorer
from typing import List, Tuple
from entities.videos import UnprocessedVideo
from external_systems.data_access.rds.pg.videos import tables
from common.utils import nl
from uuid import UUID


class UnprocessedVideosExplorerPG:
    f"""
    UnprocessedVideosExplorer database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {UnprocessedVideosExplorer.__doc__}
    """

    hash_id: UUID = None
    user_id: UUID = None


    async def search(self) -> List[UnprocessedVideo]:
        conditions = []
        params = []

        if self.user_id is not None:
            # user_id is an index and therefore it is a good first filter condition
            conditions.append('user_id::text = %s::text')
            params.append(self.user_id)
        
        if self.hash_id is not None:
            conditions.append('hash_id::text = %s::text')
            params.append(self.hash_id)

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


    def id(self, id: UUID) -> UnprocessedVideosExplorer:
        self.hash_id = id
        return self


    def of_user(self, user_id: UUID) -> UnprocessedVideosExplorer:
        self.user_id = user_id
        return self


    def __prase_db_records_into_classes(self, unprocessed_video: Tuple) -> UnprocessedVideo:
        return UnprocessedVideo(
            hash_id=unprocessed_video[0],
            user_id=unprocessed_video[1],
            upload_time=unprocessed_video[2],
            failure_reason=unprocessed_video[3]
        )
