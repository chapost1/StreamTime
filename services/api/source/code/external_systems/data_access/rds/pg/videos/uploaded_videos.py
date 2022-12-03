from __future__ import annotations
from external_systems.data_access.rds.abstract.videos.uploaded_videos import UploadedVideos
from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.pg.videos import tables
from entities.videos import VideoStages
from uuid import UUID
from typing import Tuple, List, Any, Dict
from common.utils import nl


class UploadedVideosPG:
    f"""
    UploadedVideos database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {UploadedVideos.__doc__}
    """

    hash_id: UUID = None
    user_id: UUID = None


    def with_hash(self, id: UUID) -> UploadedVideos:
        self.hash_id = id
        return self


    def owned_by(self, user_id: UUID) -> UploadedVideos:
        self.user_id = user_id
        return self


    def build_query_conditions_params(self, base_conditions: List[str] = [], base_params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        conditions: List[str] = []
        conditions.extend(base_conditions)
        params: List[Any] = []
        params.extend(base_params)

        if self.user_id is not None:
            # user_id is an index and therefore it is a good first filter condition
            conditions.append('user_id::text = %s::text')
            params.append(self.user_id)
        
        if self.hash_id is not None:
            conditions.append('hash_id::text = %s::text')
            params.append(self.hash_id)

        return conditions, params
    
    
    def build_update_statement(self, to_update: Dict, base_params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        params: List[Any] = []
        params.extend(base_params)
        update_statement = []

        for field, value in to_update.items():
            update_statement.append(f'{field} = %s')
            params.append(value)

        return update_statement, params


    async def update(self, to_update: Dict, stage: VideoStages) -> None:
        self.__assert_required_values_before_specific_video_query_execution()

        update_statement, params = self.build_update_statement(to_update=to_update)

        if len(update_statement) < 1:
            # nothing to update, skip
            return None

        conditions, params = self.build_query_conditions_params(base_params=params)
        
        table = self.__get_table_of_uploaded_video_by_stage(stage=stage)

        await Connection().execute([
            (
                f"""UPDATE {table}
                    SET {', '.join(update_statement)}
                    WHERE {f'{nl()}AND '.join(conditions)};""",
                tuple(params)
            )
        ])


    async def delete(self, stage: VideoStages) -> None:
        self.__assert_required_values_before_specific_video_query_execution()
        
        table = self.__get_table_of_uploaded_video_by_stage(stage=stage)
        
        conditions, params = self.build_query_conditions_params()

        await Connection().execute([
            (
                f"""DELETE FROM {table}
                    WHERE {f'{nl()}AND '.join(conditions)}""",
                tuple(params)
            )
        ])


    def __assert_required_values_before_specific_video_query_execution(self) -> None:
        if self.user_id is None:
            raise ValueError('delete query: user_id is None')

        if self.hash_id is None:
            raise ValueError('delete query: hash_id is None')


    def __get_table_of_uploaded_video_by_stage(self, stage: VideoStages) -> str:
        table = tables.video_stages_to_table(stage)
        
        if table is None:
            raise Exception(f'invalid uploaded video stage found. {self.user_id}/{self.hash_id} in stage [{stage}]')

        return table
