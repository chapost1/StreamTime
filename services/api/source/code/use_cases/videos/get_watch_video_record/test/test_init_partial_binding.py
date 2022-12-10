from use_cases.videos.get_watch_video_record import get_watch_video_record_use_case


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(get_watch_video_record_use_case.keywords.keys())
    expected_keys = [
        'is_access_allowed_fn'
    ]
    assert actual_keys == expected_keys
