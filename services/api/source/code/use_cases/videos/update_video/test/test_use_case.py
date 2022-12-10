from use_cases.videos.update_video.use_case import use_case
from common.utils import calc_server_time
from common.app_errors import InputError
from entities.videos import Video
from uuid import uuid4
from use_cases.videos.update_video.helpers import prepare_new_listing_before_publish
from use_cases.videos.update_video.helpers import prepare_listed_record_before_update
from use_cases.videos.update_video.helpers import parse_video_into_state_dict
import pytest
import random
from unittest.mock import (
    Mock,
    AsyncMock
)


user_id = uuid4()
video_id = uuid4()
hash_id = uuid4()


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

    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        matching_videos_in_db,
        None
    )
    mock_database.update_video.return_value = None

    spy_prepare_new_listing_before_publish = Mock(
        wraps=prepare_new_listing_before_publish
    )
    spy_prepare_listed_record_before_update = Mock(
        wraps=prepare_listed_record_before_update
    )


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
        database=mock_database,
        prepare_new_listing_before_publish_fn=spy_prepare_new_listing_before_publish,
        prepare_listed_record_before_update_fn=spy_prepare_listed_record_before_update,
        parse_video_into_state_dict_fn=parse_video_into_state_dict,
        # usage scope
        authenticated_user_id=user_id,
        video=update_input,
        hash_id=hash_id
    )

    # listing time has been attached via new desired state
    listing_time = mock_database.update_video.call_args.kwargs['new_desired_state']['listing_time']
    assert listing_time is not None

    expected = {
        'description': description,
        'title': title,
        # need to be attached as it unpredictable
        'listing_time': listing_time
    }

    # assert exact structure
    mock_database.update_video.assert_called_once_with(
        user_id=user_id,
        hash_id=hash_id,
        new_desired_state=expected
    )

    # assert the right prepare method for unlisted video has been called
    spy_prepare_new_listing_before_publish.assert_called()
    spy_prepare_listed_record_before_update.assert_not_called()


@pytest.mark.asyncio
async def test_unlisted_video_will_raise_exception_if_title_is_missing_which_is_requied():
    matching_videos_in_db = [
        Video(listing_time=None)
    ]

    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        matching_videos_in_db,
        None
    )

    try:
        await use_case(
            database=mock_database,
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

    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        matching_videos_in_db,
        None
    )
    mock_database.update_video.return_value = None

    spy_prepare_new_listing_before_publish = Mock(
        wraps=prepare_new_listing_before_publish
    )
    spy_prepare_listed_record_before_update = Mock(
        wraps=prepare_listed_record_before_update
    )
    spy_parse_video_into_state_dict = Mock(
        wraps=parse_video_into_state_dict
    )


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
        database=mock_database,
        prepare_new_listing_before_publish_fn=spy_prepare_new_listing_before_publish,
        prepare_listed_record_before_update_fn=spy_prepare_listed_record_before_update,
        parse_video_into_state_dict_fn=spy_parse_video_into_state_dict,
        # usage scope
        authenticated_user_id=user_id,
        video=update_input,
        hash_id=hash_id
    )

    expected = { 'description': description }

    # assert exact structure
    mock_database.update_video.assert_called_once_with(
        user_id=user_id,
        hash_id=hash_id,
        new_desired_state=expected
    )

    spy_parse_video_into_state_dict.assert_called_once_with(
        video=Video(
            description=description
        )
    )

    # assert the right prepare method for unlisted video has been called
    spy_prepare_new_listing_before_publish.assert_not_called()
    spy_prepare_listed_record_before_update.assert_called()
