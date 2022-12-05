from entities.videos.unprocessed_video import UnprocessedVideo


def test_unprocessed_video_can_be_initialized_without_arguments():
    vid = UnprocessedVideo()
    assert vid is not None


def test_is_still_processing_is_true_when_failure_reason_is_null():
    # on the go, it validates the existence of failure_reason
    vid = UnprocessedVideo()
    assert vid.is_still_processing() == True
    assert vid.is_failed() == False


def test_is_still_processing_is_false_when_failure_reason_exists():
    vid = UnprocessedVideo(failure_reason='dummy reason')
    assert vid.is_still_processing() == False
    assert vid.is_failed() == True
