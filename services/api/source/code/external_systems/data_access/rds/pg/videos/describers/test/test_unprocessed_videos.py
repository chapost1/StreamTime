from typing import List
from external_systems.data_access.rds.pg.videos.describers.unprocessed_videos import UnprocessedVideosDescriberPG
from external_systems.data_access.rds.pg.connection.mock import ConnectionMock
from entities.videos import UnprocessedVideo
from external_systems.data_access.rds.pg.videos import tables
from uuid import uuid4
import pytest
from common.utils.nl import nl
from common.utils.run_in_parallel import run_in_parallel
from common.utils.calc_server_time import calc_server_time
from unittest.mock import (
    Mock,
    AsyncMock
)


@pytest.mark.asyncio
async def test_search_pass_expected_envs_to_conn_query_no_conditions():
    # create mocks
    records = [
        (uuid4(), uuid4(), 'im.py', calc_server_time(), None),
        (uuid4(), uuid4(), 'f.mp', calc_server_time(), 'incomple file')
    ]

    conn_mock = ConnectionMock(return_value=records)

    describer = UnprocessedVideosDescriberPG(
        get_connection_fn=Mock(return_value=conn_mock)
    )

    describer_spy: UnprocessedVideosDescriberPG = AsyncMock(wraps=describer)

    result: List[UnprocessedVideo] = await describer_spy.search()

    # AsyncMock need to be awaited
    expected_result = list(await run_in_parallel(*list(map(describer_spy._prase_db_records_into_classes, records))))

    # assert result of records after parse.
    assert result == expected_result

    assert conn_mock.last_recorded_transaction_steps == [
        (
            nl().join([
                'SELECT',
                'hash_id,',
                'user_id,',
                'file_name,',
                'upload_time,',
                'failure_reason',
                f'FROM {tables.UNPROCESSED_VIDEOS_TABLE}',
                f'WHERE deleted_at IS null',
                'ORDER BY upload_time DESC'
            ]),
            tuple([])
        )
    ]


@pytest.mark.asyncio
async def test_search_pass_expected_envs_to_conn_query_with_user_id_hash_id():
    # create mocks
    records = [
        (uuid4(), uuid4(), 'file.py', calc_server_time(), None),
        (uuid4(), uuid4(), 'ba.m', calc_server_time(), 'incomple file'),
        (uuid4(), uuid4(), '!.>', calc_server_time(), 'internal server error')
    ]

    conn_mock = ConnectionMock(return_value=records)

    describer: UnprocessedVideosDescriberPG = UnprocessedVideosDescriberPG(
        get_connection_fn=Mock(return_value=conn_mock)
    )

    user_id = uuid4()
    hash_id = uuid4()

    describer.with_hash(id=hash_id).owned_by(user_id=user_id)

    describer_spy: UnprocessedVideosDescriberPG = AsyncMock(wraps=describer)

    result: List[UnprocessedVideo] = await describer_spy.search()

    # AsyncMock need to be awaited
    expected_result = list(await run_in_parallel(*list(map(describer_spy._prase_db_records_into_classes, records))))

    # assert result of records after parse.
    assert result == expected_result

    # AsyncMock need to be awaited
    conditions, params = await describer_spy.build_query_conditions_params()
    conditions, params = await describer_spy.build_deleted_conditions_params(conditions=conditions, params=params)

    assert conn_mock.last_recorded_transaction_steps == [
        (
            nl().join([
                'SELECT',
                'hash_id,',
                'user_id,',
                'file_name,',
                'upload_time,',
                'failure_reason',
                f'FROM {tables.UNPROCESSED_VIDEOS_TABLE}',
                f"WHERE {f'{nl()}AND '.join(conditions)}",
                'ORDER BY upload_time DESC'
            ]),
            tuple(params)
        )
    ]


@pytest.mark.asyncio
async def test_delete_calls_parent_delete_with_the_correct_table_using_conn_mock():
    conn_mock = ConnectionMock()

    describer: UnprocessedVideosDescriberPG = UnprocessedVideosDescriberPG(
        get_connection_fn=Mock(return_value=conn_mock)
    )

    user_id = uuid4()
    hash_id = uuid4()

    describer.with_hash(id=hash_id).owned_by(user_id=user_id)

    await describer.delete()

    # assert using the right delete table with expected query structure
    assert conn_mock.last_recorded_transaction_steps[0][0].find('UPDATE') == 0
    assert conn_mock.last_recorded_transaction_steps[0][0].index('deleted_at = %s') != -1


def test_with_hash_works():
    # it is checked before method is overriden
    describer: UnprocessedVideosDescriberPG = UnprocessedVideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )
    assert len(describer.hash_ids) < 1
    describer.with_hash(id=uuid4())
    assert len(describer.hash_ids) == 1


def test_owned_by_works():
    # it is checked before method is overriden
    describer: UnprocessedVideosDescriberPG = UnprocessedVideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )
    assert len(describer.user_ids) < 1
    describer.owned_by(user_id=uuid4())
    assert len(describer.user_ids) == 1


def test__prase_db_records_into_classes():
    records = [
        (uuid4(), uuid4(), 'vid.mp4', calc_server_time(), None),
        (uuid4(), uuid4(), 'hey-shahar', calc_server_time(), 'internal server error')
    ]

    describer: UnprocessedVideosDescriberPG = UnprocessedVideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    result = list(map(describer._prase_db_records_into_classes, records))

    expected_result = [
        UnprocessedVideo(
            hash_id=records[0][0],
            user_id=records[0][1],
            file_name=records[0][2],
            upload_time=records[0][3],
            failure_reason=records[0][4]
        ),
        UnprocessedVideo(
            hash_id=records[1][0],
            user_id=records[1][1],
            file_name=records[1][2],
            upload_time=records[1][3],
            failure_reason=records[1][4]
        )
    ]

    assert result == expected_result
