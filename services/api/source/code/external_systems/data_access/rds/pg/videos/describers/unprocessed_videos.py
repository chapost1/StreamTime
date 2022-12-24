from __future__ import annotations
from external_systems.data_access.rds.pg.videos.describers.uploaded_videos import UploadedVideosDescriberPG
from typing import List, Tuple
from uuid import UUID
from entities.videos import UnprocessedVideo
from entities.videos import VideoStages
from external_systems.data_access.rds.pg.videos import tables
from common.utils import nl


class UnprocessedVideosDescriberPG(UploadedVideosDescriberPG):
    """
    DescribedUnprocessedVideos database class
    Uses postgres as a concrete implementation
    """


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    async def search(self) -> List[UnprocessedVideo]:
        conditions, params = super().build_query_conditions_params()

        # default to true to prevent query crash for invalid WHERE syntax where conditions are empty
        where_condition = 'true'
        if 0 < len(conditions):
            where_condition = f'{nl()}AND '.join(conditions)

        sql = nl().join([
            'SELECT',
            'hash_id,',
            'user_id,',
            'file_name,',
            'upload_time,',
            'failure_reason',
            f'FROM {tables.UNPROCESSED_VIDEOS_TABLE}',
            f'WHERE {where_condition}',
            'ORDER BY upload_time DESC'
        ])

        videos = await self.get_connection_fn().query([
            (sql, tuple(params))
        ])

        return list(map(self._prase_db_records_into_classes, videos))
    

    async def delete(self) -> None:
        await super().delete(stage=VideoStages.UNPROCESSED.value)


    def with_hash(self, id: UUID) -> UnprocessedVideosDescriberPG:
        return super().with_hash(id=id)


    def owned_by(self, user_id: UUID) -> UnprocessedVideosDescriberPG:
        return super().owned_by(user_id=user_id)


    def _prase_db_records_into_classes(self, unprocessed_video: Tuple) -> UnprocessedVideo:
        return UnprocessedVideo(
            hash_id=unprocessed_video[0],
            user_id=unprocessed_video[1],
            file_name=unprocessed_video[2],
            upload_time=unprocessed_video[3],
            failure_reason=unprocessed_video[4]
        )
