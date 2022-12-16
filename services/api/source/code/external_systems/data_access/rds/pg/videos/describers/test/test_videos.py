from external_systems.data_access.rds.pg.videos.describers.videos import VideosDescriberPG
from external_systems.data_access.rds.pg.connection.mock import ConnectionMock
from external_systems.data_access.rds.pg.videos import tables
from entities.videos import Video, NextPage
from typing import List
from uuid import uuid4
import pytest
import random
from common.utils import (
    nl,
    run_in_parallel,
    calc_server_time
)
from unittest.mock import (
    Mock,
    AsyncMock
)


def test_build_query_conditions_params_with_no_params_added():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    conditions, params = describer.build_query_conditions_params()
    assert conditions == ['is_private IS NOT true']
    assert params == []


def test_build_query_conditions_params_with_user_id_hash_id():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    user_id = uuid4()
    hash_id = uuid4()

    conditions, params = (
        describer
        .with_hash(id=hash_id)
        .owned_by(user_id=user_id)
        .build_query_conditions_params()
    )

    expected_conditions = [
        f"{describer.cast('user_id', 'text')} IN ({describer.cast('%s', 'text')})",
        f"{describer.cast('hash_id', 'text')} IN ({describer.cast('%s', 'text')})",
        'is_private IS NOT true'
    ]
    assert conditions == expected_conditions
    assert params == [user_id, hash_id]
    assert describer.user_ids == [user_id]
    assert describer.hash_ids == [hash_id]


def test_build_query_conditions_params_with_hash_id_and_excluded_user_id():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    hash_id = uuid4()
    excluded_user_ids = [uuid4(), uuid4()]

    conditions, params = (
        describer
        .with_hash(id=hash_id)
        .not_owned_by(user_id=excluded_user_ids[0])
        .not_owned_by(user_id=excluded_user_ids[1])
        .build_query_conditions_params()
    )

    expected_conditions = [
        f"{describer.cast('hash_id', 'text')} IN ({describer.cast('%s', 'text')})",
        f"{describer.cast('user_id', 'text')} NOT IN ({describer.cast('%s', 'text')}, {describer.cast('%s', 'text')})",
        'is_private IS NOT true'
    ]
    assert conditions == expected_conditions
    assert params == [hash_id, *excluded_user_ids]
    assert describer.excluded_user_ids == excluded_user_ids


def test_build_query_conditions_params_with_paginate():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    last_page_min_index = random.randint(0, 100000)

    hash_id = uuid4()

    conditions, params = (
        describer
        .with_hash(id=hash_id)
        .paginate(pagination_index_is_smaller_than=last_page_min_index)
        .limit(limit=random.randint(0, 100))
        .build_query_conditions_params()
    )

    expected_conditions = [
        f"{describer.cast('hash_id', 'text')} IN ({describer.cast('%s', 'text')})",
        f"pagination_index < %s",
        'is_private IS NOT true'
    ]
    assert conditions == expected_conditions   
    assert params == [hash_id, last_page_min_index]
    assert describer.pagination_index_is_smaller_than == last_page_min_index


def test_build_query_conditions_params_with_paginate_none():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    limit = random.randint(0, 100)

    conditions, params = (
        describer
        .paginate(pagination_index_is_smaller_than=None)
        .limit(limit=limit)
        .build_query_conditions_params()
    )

    assert conditions == ['is_private IS NOT true']   
    assert params == []
    assert describer.pagination_index_is_smaller_than is None
    assert describer.requested_limit == limit


@pytest.mark.parametrize(
    'flag,condition',
    [
        (True, 'listing_time IS NOT null'),
        (False, None)
    ]
)
def test_build_query_conditions_params_with_listing_conditions_listing_is_added(flag: bool, condition: str):
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    # using user_id to assert conditions and params are not overwritten
    user_id = uuid4()

    conditions, params = (
        describer
        .owned_by(user_id=user_id)
        .filter_unlisted(flag=flag)
        .build_query_conditions_params()
    )

    expected_conditions = [
        f"{describer.cast('user_id', 'text')} IN ({describer.cast('%s', 'text')})"
    ]

    if condition is not None:
        expected_conditions.append(condition)

    expected_conditions.append('is_private IS NOT true')

    assert conditions == expected_conditions

    assert params == [user_id]
    assert describer.unlisted_should_be_hidden == flag


def test_build_query_conditions_params_privacy_while_allowed_globally():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    # using user_id to assert conditions and params are not overwritten
    user_id_0 = uuid4()

    conditions, params = (
        describer
        .owned_by(user_id=user_id_0)
        .unfilter_privates(flag=True)
        .build_query_conditions_params()
    )

    # expects to see private self.case as not all users are allowed to see privates
    expected_conditions = [
        f"{describer.cast('user_id', 'text')} IN ({describer.cast('%s', 'text')})"
    ]

    assert conditions == expected_conditions
    assert params == [user_id_0]
    assert describer.allow_privates_globally is True


def test_build_query_conditions_params_privacy_while_allowed_globally_while_also_allowed_specific_users():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    # using user_id to assert conditions and params are not overwritten
    user_id_0 = uuid4()

    conditions, params = (
        describer
        .owned_by(user_id=user_id_0)
        .unfilter_privates(flag=True)
        .include_privates_of(user_id=user_id_0)
        .build_query_conditions_params()
    )

    # expects to see private self.case as not all users are allowed to see privates
    expected_conditions = [
        f"{describer.cast('user_id', 'text')} IN ({describer.cast('%s', 'text')})"
    ]

    assert conditions == expected_conditions
    assert params == [user_id_0]
    assert describer.allow_privates_globally is True


def test_build_query_conditions_params_privacy_not_same_users_but_some_should_be_allowed_to_see_privates():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    # using user_id to assert conditions and params are not overwritten
    user_id_0 = uuid4()
    user_id_1 = uuid4()
    user_id_2 = uuid4()

    conditions, params = (
        describer
        .owned_by(user_id=user_id_0)
        .include_privates_of(user_id=user_id_1)
        .include_privates_of(user_id=user_id_2)
        .build_query_conditions_params()
    )

    # expects to see private self.case as not all users are allowed to see privates
    expected_conditions = [
        f"{describer.cast('user_id', 'text')} IN ({describer.cast('%s', 'text')})",
        f"CASE WHEN {describer.cast('user_id', 'text')} IN ({describer.cast('%s', 'text')}, {describer.cast('%s', 'text')}) THEN true ELSE {describer.cast(val_name='is_private IS NOT true', casting_type='bool')} END"
    ]

    assert conditions == expected_conditions
    assert params == [user_id_0, user_id_1, user_id_2]
    assert describer.allowed_privates_of_user_ids == [user_id_1, user_id_2]
    # did not change and therefore it should be false
    assert describer.allow_privates_globally is False


def test_build_query_conditions_params_privacy_no_specified_users_but_yes_private_allowed():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    # using user_id to assert conditions and params are not overwritten
    user_id_0 = uuid4()

    conditions, params = (
        describer
        .include_privates_of(user_id=user_id_0)
        .build_query_conditions_params()
    )

    # expects to see private self.case as some of the data is relevant to users which are not allwed to see privates
    expected_conditions = [
        f"CASE WHEN {describer.cast('user_id', 'text')} IN ({describer.cast('%s', 'text')}) THEN true ELSE {describer.cast(val_name='is_private IS NOT true', casting_type='bool')} END"
    ]

    assert conditions == expected_conditions
    assert params == [user_id_0]
    assert describer.allowed_privates_of_user_ids == [user_id_0]


def test_build_query_conditions_params_privacy_all_users_are_allowed():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    # using user_id to assert conditions and params are not overwritten
    user_id_0 = uuid4()
    user_id_1 = uuid4()

    conditions, params = (
        describer
        .owned_by(user_id=user_id_0)
        .owned_by(user_id=user_id_1)
        .include_privates_of(user_id=user_id_1)
        .include_privates_of(user_id=user_id_0)
        .build_query_conditions_params()
    )

    # expects to not see private self.case as all users are allowed to see privates even if not at the same order
    expected_conditions = [
        f"{describer.cast('user_id', 'text')} IN ({describer.cast('%s', 'text')}, {describer.cast('%s', 'text')})"
    ]

    assert conditions == expected_conditions
    assert params == [user_id_0, user_id_1]
    assert describer.allowed_privates_of_user_ids == [user_id_1, user_id_0]


@pytest.mark.asyncio
async def test_search_pass_expected_envs_to_conn_query_with_no_conditions():
    # create mocks
    records = [
        (
            uuid4(), uuid4(), 'title', 'description',
            random.randint(1, 100), random.randint(1, 100),
            'video_type', 'https://thumbnail_url.com',
            'storage_object_key', 'storage_thumbnail_key',
            calc_server_time(), True, calc_server_time(),
            random.randint(1, 100)
        ),
        (
            uuid4(), uuid4(), 'title', 'description',
            random.randint(1, 100), random.randint(1, 100),
            'video_type', 'https://thumbnail_url.com',
            'storage_object_key', 'storage_thumbnail_key',
            calc_server_time(), True, calc_server_time(),
            random.randint(1, 100)
        )
    ]

    conn_mock = ConnectionMock(return_value=records)

    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=conn_mock)
    )

    describer_spy: VideosDescriberPG = AsyncMock(wraps=describer)

    result: List[Video] = await describer_spy.search()
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
                'title,',
                'description,',
                'size_in_bytes,',
                'duration_seconds,',
                'video_type,',
                'thumbnail_url,',
                'storage_object_key,',
                'storage_thumbnail_key,',
                'upload_time,',
                'is_private,',
                'listing_time,',
                'pagination_index',
                f'FROM {tables.VIDEOS_TABLE}',
                f'WHERE is_private IS NOT true',
                'ORDER BY pagination_index DESC',
                'LIMIT %s'
            ]),
            tuple([None])
        )
    ]


@pytest.mark.asyncio
async def test_search_pass_expected_envs_to_conn_query_with_conditions():
    # create mocks
    records = [
        (
            uuid4(), uuid4(), 'title', 'description',
            random.randint(1, 100), random.randint(1, 100),
            'video_type', 'https://thumbnail_url.com',
            'storage_object_key', 'storage_thumbnail_key',
            calc_server_time(), True, calc_server_time(),
            random.randint(1, 100)
        ),
        (
            uuid4(), uuid4(), 'title', 'description',
            random.randint(1, 100), random.randint(1, 100),
            'video_type', 'https://thumbnail_url.com',
            'storage_object_key', 'storage_thumbnail_key',
            calc_server_time(), True, calc_server_time(),
            random.randint(1, 100)
        )
    ]

    conn_mock = ConnectionMock(return_value=records)

    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=conn_mock)
    )

    user_id = uuid4()
    not_user_id = uuid4()
    hash_id = uuid4()
    include_privates_of_user_id = uuid4()
    filter_unlisted = True
    curr_page = NextPage(minimum_pagination_index=random.randint(1, 10))
    page_limit = 10

    (
        describer
        .owned_by(user_id=user_id)
        .not_owned_by(user_id=not_user_id)
        .with_hash(id=hash_id)
        .include_privates_of(user_id=include_privates_of_user_id)
        .filter_unlisted(flag=filter_unlisted)
        .paginate(pagination_index_is_smaller_than=curr_page.minimum_pagination_index)
        .limit(limit=page_limit)
    )

    describer_spy: VideosDescriberPG = AsyncMock(wraps=describer)

    result: List[Video] = await describer_spy.search()
    # AsyncMock need to be awaited
    expected_result = list(map(describer._prase_db_records_into_classes, records))

    # assert result of records after parse.
    assert result == expected_result

    conditions, params = describer.build_query_conditions_params()

    params.append(page_limit)

    assert conn_mock.last_recorded_transaction_steps == [
        (
            nl().join([
                'SELECT',
                'hash_id,',
                'user_id,',
                'title,',
                'description,',
                'size_in_bytes,',
                'duration_seconds,',
                'video_type,',
                'thumbnail_url,',
                'storage_object_key,',
                'storage_thumbnail_key,',
                'upload_time,',
                'is_private,',
                'listing_time,',
                'pagination_index',
                f'FROM {tables.VIDEOS_TABLE}',
                f"WHERE {f'{nl()}AND '.join(conditions)}",
                'ORDER BY pagination_index DESC',
                'LIMIT %s'
            ]),
            tuple(params)
        )
    ]


@pytest.mark.asyncio
async def test_delete_calls_parent_delete_with_the_correct_table_using_conn_mock():
    conn_mock = ConnectionMock()

    describer: VideosDescriberPG = VideosDescriberPG(
        get_connection_fn=Mock(return_value=conn_mock)
    )

    user_id = uuid4()
    hash_id = uuid4()

    describer.with_hash(id=hash_id).owned_by(user_id=user_id)

    await describer.delete()
            
    conditions, params = describer.build_query_conditions_params()

    # assert using the right delete table with expected query structure
    assert conn_mock.last_recorded_transaction_steps == [
        (
            nl().join([
                f'DELETE FROM {tables.VIDEOS_TABLE}',
                f"WHERE {f'{nl()}AND '.join(conditions)}"
            ]),
            tuple(params)
        )
    ]


@pytest.mark.asyncio
async def test_update_calls_parent_update_with_the_correct_table_using_conn_mock():
    conn_mock = ConnectionMock()

    describer: VideosDescriberPG = VideosDescriberPG(
        get_connection_fn=Mock(return_value=conn_mock)
    )

    user_id = uuid4()
    hash_id = uuid4()

    describer.with_hash(id=hash_id).owned_by(user_id=user_id)

    new_desired_state = {
        'title': 'new title',
        'description': 'new description',
        'is_private': False
    }

    await describer.update(new_desired_state=new_desired_state)

    conditions, params = describer.build_query_conditions_params()

    # assert using the right update table with expected query structure
    assert conn_mock.last_recorded_transaction_steps == [
        (
            nl().join([
                f'UPDATE {tables.VIDEOS_TABLE}',
                "SET title = %s, description = %s, is_private = %s",
                f"WHERE {f'{nl()}AND '.join(conditions)}"
            ]),
            ('new title', 'new description', False, *params)
        )
    ]


def test_with_hash():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    hash_id = uuid4()

    describer.with_hash(id=hash_id)

    assert describer.hash_ids == [hash_id]


def test_owned_by():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    user_id = uuid4()

    describer.owned_by(user_id=user_id)

    assert describer.user_ids == [user_id]


def test_not_owned_by():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    user_id = uuid4()

    describer.not_owned_by(user_id=user_id)

    assert describer.excluded_user_ids == [user_id]


def test_include_privates_of():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    user_id = uuid4()

    describer.include_privates_of(user_id=user_id)

    assert describer.allowed_privates_of_user_ids == [user_id]


def test_filter_unlisted():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    describer.filter_unlisted(flag=True)

    assert describer.unlisted_should_be_hidden is True


def test_filter_privates():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    describer.unfilter_privates(flag=True)

    assert describer.allow_privates_globally is True


def test_paginate():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    pagination_index_is_smaller_than = random.randint(1, 100)

    describer.paginate(pagination_index_is_smaller_than=pagination_index_is_smaller_than)

    assert describer.pagination_index_is_smaller_than == pagination_index_is_smaller_than


def test_limit():
    describer = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    limit = random.randint(1, 100)

    describer.limit(limit=limit)

    assert describer.requested_limit == limit


def test__prase_db_records_into_classes():
    record = (
        uuid4(), uuid4(), 'title', 'description',
        random.randint(1, 100), random.randint(1, 100),
        'video_type', 'https://thumbnail_url.com',
        'storage_object_key', 'storage_thumbnail_key',
        calc_server_time(), True, calc_server_time(),
        random.randint(1, 100)
    )

    describer: VideosDescriberPG = VideosDescriberPG(
        get_connection_fn=Mock(return_value=ConnectionMock())
    )

    result = describer._prase_db_records_into_classes(video=record)

    expected_result = Video(
        hash_id=record[0],
        user_id=record[1],
        title=record[2],
        description=record[3],
        size_in_bytes=record[4],
        duration_seconds=record[5],
        video_type=record[6],
        thumbnail_url=record[7],
        storage_object_key=record[8],
        storage_thumbnail_key=record[9],
        upload_time=record[10],
        is_private=record[11],
        listing_time=record[12],
        pagination_index=record[13]
    )

    assert result == expected_result
