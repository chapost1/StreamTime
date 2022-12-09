from use_cases.videos.get_watch_video_record.helpers import is_access_allowed


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(is_access_allowed.keywords.keys())
    expected_keys = [
        'is_same_user_fn'
    ]
    assert actual_keys == expected_keys
