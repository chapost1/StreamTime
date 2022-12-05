from entities.videos.enums import VideoStages


def test_video_stages_ready_enum_exists():
    assert VideoStages.READY is not None


def test_video_stages_ready_enum_value():
    assert VideoStages.READY.value == 'READY'


def test_video_stages_unproecessed_enum_exists():
    assert VideoStages.UNPROCESSED is not None


def test_video_stages_unproecessed_enum_value():
    assert VideoStages.UNPROCESSED.value == 'UNPROCESSED'


def test_video_stages_contains_only_expected_enums():
    assert len(VideoStages) == len([
        VideoStages.UNPROCESSED,
        VideoStages.READY
    ])
