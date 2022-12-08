from __future__ import annotations
from external_systems.data_access.rds.abstract.videos.describers import UnprocessedVideosDescriber
from external_systems.data_access.rds.pg.abstract_internals import GetConnectionFunction
from external_systems.data_access.rds.pg.videos import tables
from entities.videos import VideoStages
from uuid import UUID
from typing import Tuple, List, Any, Dict
from common.utils import nl


class UploadedVideosDescriberPG:
    f"""
    DescribedUploadedVideos database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {UnprocessedVideosDescriber.__doc__}
    """

    get_connection_fn: GetConnectionFunction

    hash_ids: List[UUID]
    user_ids: List[UUID]


    def __init__(self, get_connection_fn: GetConnectionFunction) -> None:
        self.get_connection_fn = get_connection_fn
        self.hash_ids = []
        self.user_ids = []


    def with_hash(self, id: UUID) -> UnprocessedVideosDescriber:
        if id is not None:
            self.hash_ids.append(id)
        return self


    def owned_by(self, user_id: UUID) -> UnprocessedVideosDescriber:
        if user_id is not None:
            self.user_ids.append(user_id)
        return self


    def build_query_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        # user_id is an index and therefore it is a good first filter condition
        conditions, params = self.build_user_ids_conditions_params(conditions=conditions, params=params)

        conditions, params = self.build_hash_ids_conditions_params(conditions=conditions, params=params)

        return conditions, params


    def build_user_ids_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        return self.build_property_conditions_params(
            raw_params=self.user_ids,
            col_name='user_id',
            conditions=conditions,
            params=params
        )


    def build_hash_ids_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        return self.build_property_conditions_params(
            raw_params=self.hash_ids,
            col_name='hash_id',
            conditions=conditions,
            params=params
        )


    def build_property_conditions_params(
        self,
        raw_params: List[Any],
        col_name: str,
        casting_type: str = 'text',
        exclude: bool = False,
        conditions: List[str] = [],
        params: List[Any] = []
    ) -> Tuple[List[str], List[Any]]:
        if len(raw_params) < 1:
            return conditions, params

        conditions = conditions.copy()
        params = params.copy()

        s = []
        for param in raw_params:
            s.append(f'%s::{casting_type}')
            params.append(param)
        
        pre_in_expression = 'not' if exclude else ''

        statement_building_blocks = [
            f'{col_name}::{casting_type}',
            pre_in_expression,
            'in',
            f"({', '.join(s)})"
        ]

        statement = ' '.join(filter(None, statement_building_blocks))

        conditions.append(statement)

        return conditions, params

    
    def build_update_statement(self, fields: Dict, params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        params = params.copy()

        update_statement = []

        for field, value in fields.items():
            update_statement.append(f'{field} = %s')
            params.append(value)

        return update_statement, params


    async def update(self, new_desired_state: Dict, stage: VideoStages) -> None:
        self.assert_required_values_before_specific_video_query_execution()

        update_statement, params = self.build_update_statement(fields=new_desired_state)

        if len(update_statement) < 1:
            # nothing to update, skip
            return None

        conditions, params = self.build_query_conditions_params(params=params)
        
        table = self.get_table_of_uploaded_video_by_stage(stage=stage)

        await self.get_connection_fn().execute([
            (
                nl().join([
                   f'UPDATE {table}',
                   f"SET {', '.join(update_statement)}",
                   f"WHERE {f'{nl()}AND '.join(conditions)}"
                ]),
                tuple(params)
            )
        ])


    async def delete(self, stage: VideoStages) -> None:
        self.assert_required_values_before_specific_video_query_execution()
        
        table = self.get_table_of_uploaded_video_by_stage(stage=stage)
        
        conditions, params = self.build_query_conditions_params()

        await self.get_connection_fn().execute([
            (
                nl().join([
                   f'DELETE FROM {table}',
                   f"WHERE {f'{nl()}AND '.join(conditions)}"
                ]),
                tuple(params)
            )
        ])


    def assert_required_values_before_specific_video_query_execution(self) -> None:
        if len(self.user_ids) < 1:
            raise ValueError('delete query: user_id is missing')

        if len(self.hash_ids) < 1:
            raise ValueError('delete query: hash_id is missing')


    def get_table_of_uploaded_video_by_stage(self, stage: VideoStages) -> str:
        table = tables.video_stages_to_table(stage)
        
        if table is None:
            identifiers = f'user_ids={self.user_ids}, hash_ids={self.hash_ids}'
            raise Exception(f'invalid uploaded video stage found for identifiers=[{identifiers}]. stage: [{stage}]')

        return table
