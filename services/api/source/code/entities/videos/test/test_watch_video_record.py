from entities.videos.watch_video_record import WatchVideoRecord
from entities.videos.video import Video
import pytest
from pydantic import ValidationError

some_valid_url = 'https://foo.bar.com'


def test_should_require_watchable_url_argument():
    with pytest.raises(expected_exception=ValidationError):
        WatchVideoRecord(video=Video())


def test_should_require_video_argument():
    with pytest.raises(expected_exception=ValidationError):
        WatchVideoRecord(watchable_url=some_valid_url)


def test_should_fail_on_invalid_url():
    with pytest.raises(expected_exception=ValidationError):
        WatchVideoRecord(watchable_url='invalid', video=Video())


def test_should_init_with_valid_arguments():
    r = WatchVideoRecord(watchable_url=some_valid_url, video=Video())
    assert r.watchable_url == some_valid_url
    assert r.video == Video()
