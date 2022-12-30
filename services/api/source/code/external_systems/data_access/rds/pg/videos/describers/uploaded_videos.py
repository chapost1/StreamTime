from __future__ import annotations
from external_systems.data_access.rds.pg.abstract_internals import GetConnectionFunction
from external_systems.data_access.rds.pg.videos import tables
from entities.videos import VideoStages
from uuid import UUID
from typing import Tuple, List, Any, Dict
from common.utils.nl import nl
from common.utils.calc_server_time import calc_server_time


class UploadedVideosDescriberPG:
    """
    DescribedUploadedVideos database class
    Uses postgres as a concrete implementation
    """

    get_connection_fn: GetConnectionFunction

    hash_ids: List[UUID]
    user_ids: List[UUID]
    deleted_should_be_hidden: bool


    def __init__(self, get_connection_fn: GetConnectionFunction) -> None:
        self.get_connection_fn = get_connection_fn
        self.hash_ids = []
        self.user_ids = []
        self.deleted_should_be_hidden = True


    def with_hash(self, id: UUID) -> UploadedVideosDescriberPG:
        if id is not None:
            self.hash_ids.append(id)
        return self


    def owned_by(self, user_id: UUID) -> UploadedVideosDescriberPG:
        if user_id is not None:
            self.user_ids.append(user_id)
        return self


    def unfilter_deleted(self, flag: bool = True) -> UploadedVideosDescriberPG:
        self.deleted_should_be_hidden = not flag
        return self


    def build_query_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        # user_id is an index and therefore it is a good first filter condition
        conditions, params = self.build_property_conditions_params(
            raw_params=self.user_ids,
            col_name='user_id',
            conditions=conditions,
            params=params
        )

        # hash_id
        conditions, params = self.build_property_conditions_params(
            raw_params=self.hash_ids,
            col_name='hash_id',
            conditions=conditions,
            params=params
        )

        return conditions, params
    

    def build_deleted_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        conditions = conditions.copy()
        params = params.copy()

        if self.deleted_should_be_hidden:
            conditions.append('deleted_at IS null')

        return conditions, params


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
            s.append(self.cast(val_name='%s', casting_type=casting_type))
            params.append(param)
        
        pre_in_expression = 'NOT' if exclude else ''

        statement_building_blocks = [
            self.cast(val_name=col_name, casting_type=casting_type),
            pre_in_expression,
            'IN',
            f"({', '.join(s)})"
        ]

        statement = ' '.join(filter(None, statement_building_blocks))

        conditions.append(statement)

        return conditions, params
    

    def cast(self, val_name: str, casting_type: str) -> str:
        return f'CAST ( ({val_name}) AS {casting_type} )'

    
    def case(self, cases: List[Tuple[str, str]], default: str) -> str:
        statement = ['CASE']

        if cases is None:
            cases = []
        if len(cases) < 1:
            cases.append(tuple(['false', 'null']))

        if default is None:
            default = 'true'

        for case in cases:
            statement.append(f'WHEN {case[0]}')
            statement.append(f'THEN {case[1]}')
        
        statement.append(f'ELSE {default}')

        statement.append('END')

        return ' '.join(statement)


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

        params = [calc_server_time()]

        conditions, params = self.build_query_conditions_params(params=params)
        
        table = self.get_table_of_uploaded_video_by_stage(stage=stage)

        await self.get_connection_fn().execute([
            (
                nl().join([
                   f'UPDATE {table}',
                   f"SET deleted_at = %s",
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
