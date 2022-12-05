from entities.videos.user_videos_list import UserVideosList
from entities.videos.unprocessed_video import UnprocessedVideo
from entities.videos.video import Video
import pytest
from pydantic import ValidationError


def test_should_require_unprocessed_videos_argument():
    with pytest.raises(expected_exception=ValidationError):
        UserVideosList(videos=[])


def test_should_require_videos_argument():
    with pytest.raises(expected_exception=ValidationError):
        UserVideosList(unprocessed_videos=[])


def test_should_not_fail_on_valid_arguments():
    # on the go, checks the expected types
    UserVideosList(
        unprocessed_videos=[
            UnprocessedVideo()
        ],
        videos=[
            Video()
        ]
    )
    assert 1 == 1
