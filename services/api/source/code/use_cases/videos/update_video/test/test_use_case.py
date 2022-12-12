from use_cases.videos.update_video.use_case import use_case
from common.utils import calc_server_time
from common.app_errors import (
    InputError,
    NotFoundError
)
from entities.videos import Video
from uuid import uuid4
from use_cases.videos.update_video.helpers import resolve_update_state_for_pre_listing
from use_cases.videos.update_video.helpers import resolve_update_state_for_post_listing
import pytest
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
async def test_notfound_video_update_will_raise_exception_of_not_found():
    matching_videos_in_db = []

    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        matching_videos_in_db,
        None
    )

    try:
        await use_case(
            database=mock_database,
            resolve_update_state_for_pre_listing_fn=resolve_update_state_for_pre_listing,
            resolve_update_state_for_post_listing_fn=resolve_update_state_for_post_listing,
            # usage scope
            authenticated_user_id=user_id,
            video=Video(),
            hash_id=hash_id
        )
        # unexpected
        assert 1 == 2
    except NotFoundError:
        # as expected
        assert 1 == 1


@pytest.mark.asyncio
async def test_unlisted_video_update_will_raise_exception_of_some_unsupported_field():
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

    update_input = Video(
        upload_time=calc_server_time()
    )

    try:
        await use_case(
            database=mock_database,
            resolve_update_state_for_pre_listing_fn=resolve_update_state_for_pre_listing,
            resolve_update_state_for_post_listing_fn=resolve_update_state_for_post_listing,
            # usage scope
            authenticated_user_id=user_id,
            video=update_input,
            hash_id=hash_id
        )
        # unexpected
        assert 1 == 2
    except InputError:
        # as expected
        assert 1 == 1


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

    spy_resolve_update_state_for_pre_listing = Mock(
        wraps=resolve_update_state_for_pre_listing
    )
    spy_resolve_update_state_for_post_listing = Mock(
        wraps=resolve_update_state_for_post_listing
    )


    description = 'dummy desc'
    title = 'dummy title'
    update_input = Video(
        description=description,
        title=title,
    )

    await use_case(
        database=mock_database,
        resolve_update_state_for_pre_listing_fn=spy_resolve_update_state_for_pre_listing,
        resolve_update_state_for_post_listing_fn=spy_resolve_update_state_for_post_listing,
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
    # therefore, the helpers logic will take place
    spy_resolve_update_state_for_pre_listing.assert_called()
    spy_resolve_update_state_for_post_listing.assert_not_called()


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
            resolve_update_state_for_pre_listing_fn=resolve_update_state_for_pre_listing,
            resolve_update_state_for_post_listing_fn=resolve_update_state_for_post_listing,
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
async def test_listed_video_will_not_get_listing_time_on_update_func_as_it_is_not_suppose_to_attach():
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

    spy_resolve_update_state_for_pre_listing = Mock(
        wraps=resolve_update_state_for_pre_listing
    )
    spy_resolve_update_state_for_post_listing = Mock(
        wraps=resolve_update_state_for_post_listing
    )


    description = 'dummy desc'
    update_input = Video(
        description=description,
        is_private=False
    )

    await use_case(
        database=mock_database,
        resolve_update_state_for_pre_listing_fn=spy_resolve_update_state_for_pre_listing,
        resolve_update_state_for_post_listing_fn=spy_resolve_update_state_for_post_listing,
        # usage scope
        authenticated_user_id=user_id,
        video=update_input,
        hash_id=hash_id
    )

    expected = { 'description': description, 'is_private': False }

    # assert exact structure
    mock_database.update_video.assert_called_once_with(
        user_id=user_id,
        hash_id=hash_id,
        new_desired_state=expected
    )

    # assert the right prepare method for unlisted video has been called
    spy_resolve_update_state_for_pre_listing.assert_not_called()
    spy_resolve_update_state_for_post_listing.assert_called()
