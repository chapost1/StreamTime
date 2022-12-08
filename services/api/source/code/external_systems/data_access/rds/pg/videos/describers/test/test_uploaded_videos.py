from typing import Any
from external_systems.data_access.rds.pg.videos.describers.uploaded_videos import UploadedVideosDescriberPG
from external_systems.data_access.rds.pg.connection.mock import ConnectionMock
from uuid import uuid4
import random
import pytest
from common.utils.nl import nl
from mock import patch

mock_table_name = 'mock_table'

def get_connection_mock(return_value: Any = None, side_effect: Exception = None):
    return ConnectionMock(return_value=return_value, side_effect=side_effect)


def test_build_property_conditions_params_does_not_affect_base_if_raw_is_empty():
    base_conditions = [uuid4()]
    base_params = [random.randint(0, 1000)]
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    conditions, params = uv.build_property_conditions_params(
        raw_params=[],
        col_name='test',
        conditions=base_conditions,
        params=base_params
    )

    assert conditions == base_conditions
    assert params == base_params


def test_build_property_conditions_params_returns_expected_value():
    dummy_first_condition = uuid4()
    dummy_second_condition = uuid4()
    dummy_first_param = random.randint(0, 1000)
    dummy_second_param = random.randint(0, 1000)
    dummy_third_param = random.randint(0, 1000)
    # makes sure order is not changed and base is not overridden
    base_conditions = [dummy_first_condition, dummy_second_condition]
    base_params = [dummy_first_param, dummy_second_param, dummy_third_param]

    col_name = uuid4()

    default_casting_type = 'text'

    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    conditions, params = uv.build_property_conditions_params(
        raw_params=[
            'dummy_constant_param_value',
            5
        ],
        col_name=col_name,
        conditions=base_conditions,
        params=base_params
    )

    assert conditions == [
        dummy_first_condition, dummy_second_condition,
        f'{col_name}::{default_casting_type} in (%s::{default_casting_type}, %s::{default_casting_type})'
    ]

    assert params == [
        dummy_first_param, dummy_second_param, dummy_third_param,
        'dummy_constant_param_value',
        5
    ]


def test_build_property_conditions_params_returns_expected_value_with_exclude_as_not():
    col_name = uuid4()
    random_param = random.randint(1, 100)

    casting_type = 'bool'

    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    conditions, params = uv.build_property_conditions_params(
        raw_params=[random_param],
        casting_type=casting_type,
        col_name=col_name,
        exclude=True
    )

    assert conditions == [
        f'{col_name}::{casting_type} not in (%s::{casting_type})'
    ]

    assert params == [random_param]


def test_build_hash_ids_conditions_params_returns_expected_values():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    uid_1 = uuid4()
    uid_2 = uuid4()
    uv.with_hash(id=uid_1)
    uv.with_hash(id=uid_2)

    conditions, params = uv.build_hash_ids_conditions_params()

    assert conditions == [
        f'hash_id::text in (%s::text, %s::text)'
    ]

    assert params == [uid_1, uid_2]


def test_with_hash_adds_hash_id_into_list():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    h1 = uuid4()
    uv.with_hash(id=h1)
    h2 = uuid4()
    uv.with_hash(id=h2)
    assert uv.hash_ids == [h1, h2]


def test_with_hash_adds_nothing_if_none():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    uv.with_hash(id=None)
    assert uv.hash_ids == []


def test_build_user_ids_conditions_params_returns_expected_values():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    uid_1 = uuid4()
    uid_2 = uuid4()
    uv.owned_by(user_id=uid_1)
    uv.owned_by(user_id=uid_2)

    conditions, params = uv.build_user_ids_conditions_params()

    assert conditions == [
        f'user_id::text in (%s::text, %s::text)'
    ]

    assert params == [uid_1, uid_2]


def test_owned_by_adds_user_id_into_list():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    user_id = uuid4()
    uv.owned_by(user_id=user_id)
    assert uv.user_ids == [user_id]


def test_owned_by_adds_nothing_if_none():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    uv.owned_by(user_id=None)
    assert uv.user_ids == []


def test_build_update_statement_does_not_affect_base_params():
    dummy_first_param = random.randint(0, 1000)

    base_params = [dummy_first_param]

    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    _, _ = uv.build_update_statement(
        fields={
            'message': 'hello-world',
        },
        params=base_params
    )

    assert base_params == [dummy_first_param]


def test_build_update_statement_params_should_contain_base_params():
    dummy_first_param = random.randint(0, 1000)

    base_params = [dummy_first_param]

    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    _, params = uv.build_update_statement(
        fields={
            'message': 'hello-world',
        },
        params=base_params
    )

    assert params == [dummy_first_param, 'hello-world']


def test_build_update_statement_does_not_affect_returns_expectd_values():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    update_statement, params = uv.build_update_statement(
        fields={
            'message': 'hello-world',
            'second_field': 3
        }
    )

    assert update_statement == ['message = %s', 'second_field = %s']
    assert params == ['hello-world', 3]


def test_assert_required_values_before_specific_video_query_execution_when_no_user_id():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    uv.with_hash(id=uuid4())
    with pytest.raises(expected_exception=ValueError):
        uv.assert_required_values_before_specific_video_query_execution()


def test_assert_required_values_before_specific_video_query_execution_when_no_hash_id():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    uv.owned_by(user_id=uuid4())
    with pytest.raises(expected_exception=ValueError):
        uv.assert_required_values_before_specific_video_query_execution()


def test_assert_required_values_before_specific_video_query_execution_with_both_req():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    uv.owned_by(user_id=uuid4())
    uv.with_hash(id=uuid4())
    uv.assert_required_values_before_specific_video_query_execution()
    assert 1 == 1


@patch('external_systems.data_access.rds.pg.videos.tables.video_stages_to_table', lambda *args, **kwargs: None)
def test_get_table_of_uploaded_video_by_stage_raise_exception_if_stage_table_is_none():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    with pytest.raises(expected_exception=Exception):
        uv.get_table_of_uploaded_video_by_stage(stage=None)


@patch('external_systems.data_access.rds.pg.videos.tables.video_stages_to_table', lambda *args, **kwargs: mock_table_name)
def test_get_table_of_uploaded_video_by_stage_returns_valid_table():
    uv = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    result = uv.get_table_of_uploaded_video_by_stage(stage=None)
    assert result == mock_table_name


@pytest.mark.asyncio
@patch('external_systems.data_access.rds.pg.videos.tables.video_stages_to_table', lambda *args, **kwargs: mock_table_name)
async def test_update_calls_with_expected_steps():
    connection_mock = get_connection_mock()
    uv = UploadedVideosDescriberPG(get_connection_fn=lambda *args, **kwargs: connection_mock)

    user_id = uuid4()
    hash_id = uuid4()

    (
        uv
        .owned_by(user_id=user_id)
        .with_hash(id=hash_id)
    )

    new_desired_state = {
        'hello': 'world',
        'a': 'b',
        'c': 4
    }

    await uv.update(
        new_desired_state=new_desired_state,
        stage=None
    )

    expectd_ts = [
        (
            nl().join([
                f'UPDATE {mock_table_name}',
                'SET hello = %s, a = %s, c = %s',
                'WHERE user_id::text in (%s::text)',
                'AND hash_id::text in (%s::text)'
            ]),
            tuple(['world', 'b', 4, user_id, hash_id])
        )
    ]

    assert connection_mock.last_recorded_transaction_steps == expectd_ts


@pytest.mark.asyncio
@patch('external_systems.data_access.rds.pg.videos.tables.video_stages_to_table', lambda *args, **kwargs: mock_table_name)
async def test_delete_calls_with_expected_steps():
    connection_mock = get_connection_mock()
    uv = UploadedVideosDescriberPG(get_connection_fn=lambda *args, **kwargs: connection_mock)

    user_id = uuid4()
    hash_id = uuid4()

    (
        uv
        .owned_by(user_id=user_id)
        .with_hash(id=hash_id)
    )

    await uv.delete(
        stage=None
    )

    expectd_ts = [
        (
            nl().join([
                f'DELETE FROM {mock_table_name}',
                'WHERE user_id::text in (%s::text)',
                'AND hash_id::text in (%s::text)'
            ]),
            tuple([user_id, hash_id])
        )
    ]

    assert connection_mock.last_recorded_transaction_steps == expectd_ts
