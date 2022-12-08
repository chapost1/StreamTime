from typing import List, Any, Dict
from use_cases.videos.update_video.use_case import use_case
from common.utils import calc_server_time
from common.app_errors import InputError
from entities.videos import Video
from uuid import uuid4
from use_cases.videos.update_video.new_listing_preparations import prepare_new_listing_before_publish
from use_cases.videos.update_video.listed_videos_preparations import prepare_listed_record_before_update
from use_cases.videos.update_video.parse_video_into_state_dict import parse_video_into_state_dict
from use_cases.db_operation_utils.concrete import (
    search_one_in_database,
    update_in_database
)
import pytest
import random

user_id = uuid4()
video_id = uuid4()
hash_id = uuid4()

def get_database_describer(matching_videos_in_db=List[Video]):
    class SearchableUpdatable:
        desired_update_state_record: Dict
        def __init__(self) -> None:
            self.desired_update_state_record = None

        async def search(self) -> List[Any]:
            return matching_videos_in_db

        async def update(self, new_desired_state: Dict) -> None:
            self.desired_update_state_record = new_desired_state
            return None
    
    return SearchableUpdatable()


# the tests below checks specific behaviors
# and on the go checks the use case calls the right building blocks (which are tested individually)


@pytest.mark.asyncio
async def test_unlisted_video_will_get_listing_time_on_the_update_db_fn():
    matching_videos_in_db = [
        Video(
            user_id=user_id,
            hash_id=hash_id,
            listing_time=None
        )
    ]

    su = get_database_describer(matching_videos_in_db=matching_videos_in_db)

    called_right_prepate_fn = False
    def prepare_new_listing_before_publish_call_recorder(*args, **kwagrs) -> Any:
        nonlocal called_right_prepate_fn
        called_right_prepate_fn = True
        return prepare_new_listing_before_publish(*args, **kwagrs)

    description = 'dummy desc'
    title = 'dummy title'
    update_input = Video(
        description=description,
        title=title,
        # expected to be omitted
        user_id=user_id,
        hash_id=hash_id,
        size_in_bytes=random.randint(1, 1000)
    )

    await use_case(
        database=None,
        search_one_in_database_fn=search_one_in_database,
        update_in_database_fn=update_in_database,
        describe_videos_in_database_fn=lambda *args, **kwds: su,
        prepare_new_listing_before_publish_fn=prepare_new_listing_before_publish_call_recorder,
        prepare_listed_record_before_update_fn=prepare_listed_record_before_update,
        parse_video_into_state_dict_fn=parse_video_into_state_dict,
        # usage scope
        authenticated_user_id=user_id,
        video=update_input,
        hash_id=hash_id
    )

    # listing time has been attached
    assert su.desired_update_state_record['listing_time'] is not None

    expected = {
        'description': description,
        'title': title,
        # need to be attached as it unpredictable
        'listing_time': su.desired_update_state_record['listing_time']
    }

    # assert exact structure
    assert su.desired_update_state_record == expected

    # assert the right prepare method for unlisted video has been called
    assert called_right_prepate_fn == True


@pytest.mark.asyncio
async def test_unlisted_video_will_raise_exception_if_title_is_missing_which_is_requied():
    matching_videos_in_db = [
        Video(listing_time=None)
    ]

    su = get_database_describer(matching_videos_in_db=matching_videos_in_db)

    try:
        await use_case(
            database=None,
            search_one_in_database_fn=search_one_in_database,
            update_in_database_fn=update_in_database,
            describe_videos_in_database_fn=lambda *args, **kwds: su,
            prepare_new_listing_before_publish_fn=prepare_new_listing_before_publish,
            prepare_listed_record_before_update_fn=prepare_listed_record_before_update,
            parse_video_into_state_dict_fn=parse_video_into_state_dict,
            # usage scope
            authenticated_user_id=user_id,
            video=Video(description='dummy desc'),
            hash_id=hash_id
        )
        # should not rech here
        assert 1 == 2
    except InputError:
        assert 1 == 1


@pytest.mark.asyncio
async def test_listed_video_will_not_get_listing_time_on_update_func_as_it_is_immutable():
    matching_videos_in_db = [
        Video(
            user_id=user_id,
            hash_id=hash_id,
            listing_time=calc_server_time()
        )
    ]

    su = get_database_describer(matching_videos_in_db=matching_videos_in_db)

    called_right_prepate_fn = False
    def prepare_listed_record_before_update_call_recorder(*args, **kwagrs) -> Any:
        nonlocal called_right_prepate_fn
        called_right_prepate_fn = True
        return prepare_listed_record_before_update(*args, **kwagrs)

    description = 'dummy desc'
    update_input = Video(
        description=description,
        # expected to be omitted
        listing_time=calc_server_time(),
        user_id=user_id,
        hash_id=hash_id,
        size_in_bytes=random.randint(1, 1000)
    )

    await use_case(
        database=None,
        search_one_in_database_fn=search_one_in_database,
        update_in_database_fn=update_in_database,
        describe_videos_in_database_fn=lambda *args, **kwds: su,
        prepare_new_listing_before_publish_fn=prepare_new_listing_before_publish,
        prepare_listed_record_before_update_fn=prepare_listed_record_before_update_call_recorder,
        parse_video_into_state_dict_fn=parse_video_into_state_dict,
        # usage scope
        authenticated_user_id=user_id,
        video=update_input,
        hash_id=hash_id
    )

    expected = { 'description': description,}

    # assert exact structure
    assert su.desired_update_state_record == expected

    # assert the right prepare method for unlisted video has been called
    assert called_right_prepate_fn == True
