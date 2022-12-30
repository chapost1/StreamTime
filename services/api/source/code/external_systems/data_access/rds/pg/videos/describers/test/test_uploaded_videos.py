from typing import Any
from external_systems.data_access.rds.pg.videos.describers.uploaded_videos import UploadedVideosDescriberPG
from external_systems.data_access.rds.pg.connection.mock import ConnectionMock
from uuid import uuid4
import random
import pytest
from common.utils.nl import nl
from mock import patch
from unittest.mock import Mock

mock_table_name = 'mock_table'
mock_server_time = '2020-01-01T00:00:00+00:00'

def get_connection_mock(return_value: Any = None, side_effect: Exception = None):
    return ConnectionMock(return_value=return_value, side_effect=side_effect)


def test_case():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    val_name = 'dummy'
    casting_type = 'text'
    expression = describer.cast(val_name=val_name, casting_type='text')
    assert expression == f'CAST ( ({val_name}) AS {casting_type} )'


def test_case_no_cases_should_return_falsy_case_so_default_will_be_used():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    statement = describer.case(
        cases=[],
        default='false'
    )

    assert statement == 'CASE WHEN false THEN null ELSE false END'


def test_case_no_default_should_be_truthy():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    statement = describer.case(
        cases=[],
        default=None
    )

    assert statement == 'CASE WHEN false THEN null ELSE true END'


def test_case_should_be_build_as_expected():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    statement = describer.case(
        cases=[
            tuple(['condition_2', 'then_2']),
            tuple(['condition_1', 'then_1'])
        ],
        default='null'
    )

    assert statement == 'CASE WHEN condition_2 THEN then_2 WHEN condition_1 THEN then_1 ELSE null END'


def test_build_property_conditions_params_does_not_affect_base_if_raw_is_empty():
    base_conditions = [uuid4()]
    base_params = [random.randint(0, 1000)]
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    conditions, params = describer.build_property_conditions_params(
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

    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    conditions, params = describer.build_property_conditions_params(
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
        f"{describer.cast(val_name=col_name, casting_type=default_casting_type)} IN ({describer.cast(val_name='%s', casting_type=default_casting_type)}, {describer.cast(val_name='%s', casting_type=default_casting_type)})"
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

    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    conditions, params = describer.build_property_conditions_params(
        raw_params=[random_param],
        casting_type=casting_type,
        col_name=col_name,
        exclude=True
    )

    assert conditions == [
        f"{describer.cast(val_name=col_name, casting_type=casting_type)} NOT IN ({describer.cast(val_name='%s', casting_type=casting_type)})"
    ]

    assert params == [random_param]


def test_build_query_conditions_params_no_conditions():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    conditions, params = describer.build_query_conditions_params()
    assert conditions == []
    assert params == []


def test_build_query_conditions_params_user_id_conditions():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    u1 = uuid4()
    u2 = uuid4()
    u3 = uuid4()
    describer.owned_by(user_id=u1).owned_by(user_id=u2).owned_by(user_id=u3)
    conditions, params = describer.build_query_conditions_params()
    expected_conditions = [
        f"{describer.cast(val_name='user_id', casting_type='text')} IN ({describer.cast(val_name='%s', casting_type='text')}, {describer.cast(val_name='%s', casting_type='text')}, {describer.cast(val_name='%s', casting_type='text')})"
    ]
    expected_params = [u1, u2, u3]

    assert conditions == expected_conditions
    assert params == expected_params


def test_build_query_conditions_params_hash_id_conditions():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    h1 = uuid4()
    h2 = uuid4()
    h3 = uuid4()
    describer.with_hash(id=h1).with_hash(id=h2).with_hash(id=h3)
    describer.hash_ids = [h1, h2, h3]
    conditions, params = describer.build_query_conditions_params()
    expected_conditions = [
        f"{describer.cast(val_name='hash_id', casting_type='text')} IN ({describer.cast(val_name='%s', casting_type='text')}, {describer.cast(val_name='%s', casting_type='text')}, {describer.cast(val_name='%s', casting_type='text')})"
    ]
    expected_params = [h1, h2, h3]
    assert conditions == expected_conditions
    assert params == expected_params


def test_build_query_conditions_params_user_id_and_hash_id_conditions():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    u1 = uuid4()
    u2 = uuid4()
    u3 = uuid4()
    h1 = uuid4()
    h2 = uuid4()
    h3 = uuid4()
    describer.with_hash(id=h1).with_hash(id=h2).with_hash(id=h3)
    describer.owned_by(user_id=u1).owned_by(user_id=u2).owned_by(user_id=u3)
    conditions, params = describer.build_query_conditions_params()
    expected_conditions = [
        f"{describer.cast(val_name='user_id', casting_type='text')} IN ({describer.cast(val_name='%s', casting_type='text')}, {describer.cast(val_name='%s', casting_type='text')}, {describer.cast(val_name='%s', casting_type='text')})",
        f"{describer.cast(val_name='hash_id', casting_type='text')} IN ({describer.cast(val_name='%s', casting_type='text')}, {describer.cast(val_name='%s', casting_type='text')}, {describer.cast(val_name='%s', casting_type='text')})"
    ]
    expected_params = [u1, u2, u3, h1, h2, h3]

    assert conditions == expected_conditions
    assert params == expected_params


def test_with_hash_adds_hash_id_into_list():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    h1 = uuid4()
    describer.with_hash(id=h1)
    h2 = uuid4()
    describer.with_hash(id=h2)
    assert describer.hash_ids == [h1, h2]


def test_with_hash_adds_nothing_if_none():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    describer.with_hash(id=None)
    assert describer.hash_ids == []


def test_owned_by_adds_user_id_into_list():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    user_id = uuid4()
    describer.owned_by(user_id=user_id)
    assert describer.user_ids == [user_id]


def test_owned_by_adds_nothing_if_none():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    describer.owned_by(user_id=None)
    assert describer.user_ids == []


def test_unfilter_deleted():
    describer = UploadedVideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    describer.unfilter_deleted(flag=True)

    assert describer.deleted_should_be_hidden is False


def test_build_update_statement_does_not_affect_base_params():
    dummy_first_param = random.randint(0, 1000)

    base_params = [dummy_first_param]

    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    _, _ = describer.build_update_statement(
        fields={
            'message': 'hello-world',
        },
        params=base_params
    )

    assert base_params == [dummy_first_param]


def test_build_update_statement_params_should_contain_base_params():
    dummy_first_param = random.randint(0, 1000)

    base_params = [dummy_first_param]

    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    _, params = describer.build_update_statement(
        fields={
            'message': 'hello-world',
        },
        params=base_params
    )

    assert params == [dummy_first_param, 'hello-world']


def test_build_deleted_conditions_params_default():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    conditions, params = describer.build_deleted_conditions_params()
    assert conditions == [
        'deleted_at IS null'
    ]
    assert params == []


def test_build_deleted_conditions_params_unfilter_is_false():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    describer.unfilter_deleted(flag=False)
    conditions, params = describer.build_deleted_conditions_params()
    assert conditions == [
        'deleted_at IS null'
    ]
    assert params == []


def test_build_deleted_conditions_params_unfilter_is_true():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    describer.unfilter_deleted(flag=True)
    conditions, params = describer.build_deleted_conditions_params()
    assert conditions == []
    assert params == []


def test_build_update_statement_does_not_affect_returns_expectd_values():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    update_statement, params = describer.build_update_statement(
        fields={
            'message': 'hello-world',
            'second_field': 3
        }
    )

    assert update_statement == ['message = %s', 'second_field = %s']
    assert params == ['hello-world', 3]


def test_assert_required_values_before_specific_video_query_execution_when_no_user_id():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    describer.with_hash(id=uuid4())
    with pytest.raises(expected_exception=ValueError):
        describer.assert_required_values_before_specific_video_query_execution()


def test_assert_required_values_before_specific_video_query_execution_when_no_hash_id():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    describer.owned_by(user_id=uuid4())
    with pytest.raises(expected_exception=ValueError):
        describer.assert_required_values_before_specific_video_query_execution()


def test_assert_required_values_before_specific_video_query_execution_with_both_req():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    describer.owned_by(user_id=uuid4())
    describer.with_hash(id=uuid4())
    describer.assert_required_values_before_specific_video_query_execution()
    assert 1 == 1


@patch('external_systems.data_access.rds.pg.videos.tables.video_stages_to_table', Mock(return_value=None))
def test_get_table_of_uploaded_video_by_stage_raise_exception_if_stage_table_is_none():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    with pytest.raises(expected_exception=Exception):
        describer.get_table_of_uploaded_video_by_stage(stage=None)


@patch('external_systems.data_access.rds.pg.videos.tables.video_stages_to_table', Mock(return_value=mock_table_name))
def test_get_table_of_uploaded_video_by_stage_returns_valid_table():
    describer = UploadedVideosDescriberPG(get_connection_fn=get_connection_mock)
    result = describer.get_table_of_uploaded_video_by_stage(stage=None)
    assert result == mock_table_name


@pytest.mark.asyncio
@patch('external_systems.data_access.rds.pg.videos.tables.video_stages_to_table', Mock(return_value=mock_table_name))
async def test_update_calls_with_expected_steps():
    connection_mock = get_connection_mock()
    describer = UploadedVideosDescriberPG(get_connection_fn=Mock(return_value=connection_mock))

    user_id = uuid4()
    hash_id = uuid4()

    (
        describer
        .owned_by(user_id=user_id)
        .with_hash(id=hash_id)
    )

    new_desired_state = {
        'hello': 'world',
        'a': 'b',
        'c': 4
    }

    await describer.update(
        new_desired_state=new_desired_state,
        stage=None
    )

    expectd_ts = [
        (
            nl().join([
                f'UPDATE {mock_table_name}',
                'SET hello = %s, a = %s, c = %s',
                f"WHERE {describer.cast(val_name='user_id', casting_type='text')} IN ({describer.cast(val_name='%s', casting_type='text')})",
                f"AND {describer.cast(val_name='hash_id', casting_type='text')} IN ({describer.cast(val_name='%s', casting_type='text')})"
            ]),
            tuple(['world', 'b', 4, user_id, hash_id])
        )
    ]

    assert connection_mock.last_recorded_transaction_steps == expectd_ts


@pytest.mark.asyncio
@patch('external_systems.data_access.rds.pg.videos.tables.video_stages_to_table', Mock(return_value=mock_table_name))
async def test_delete_calls_with_expected_steps():
    connection_mock = get_connection_mock()
    describer = UploadedVideosDescriberPG(get_connection_fn=Mock(return_value=connection_mock))

    user_id = uuid4()
    hash_id = uuid4()

    (
        describer
        .owned_by(user_id=user_id)
        .with_hash(id=hash_id)
    )

    await describer.delete(
        stage=None
    )

    expectd_ts = [
        (
            nl().join([
                   f'UPDATE {mock_table_name}',
                   f"SET deleted_at = %s",
                   f"WHERE {describer.cast(val_name='user_id', casting_type='text')} IN ({describer.cast(val_name='%s', casting_type='text')})",
                   f"AND {describer.cast(val_name='hash_id', casting_type='text')} IN ({describer.cast(val_name='%s', casting_type='text')})"
            ]),
            tuple([mock_server_time, user_id, hash_id])
        )
    ]

    assert connection_mock.last_recorded_transaction_steps is not None
    assert len(connection_mock.last_recorded_transaction_steps) == 1

    # override the server time
    actual = [tuple([
        connection_mock.last_recorded_transaction_steps[0][0],
        tuple([
            expectd_ts[0][1][0], connection_mock.last_recorded_transaction_steps[0][1][1], connection_mock.last_recorded_transaction_steps[0][1][2]
        ])
    ])]

    assert actual == expectd_ts
