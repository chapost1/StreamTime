from use_cases.videos.delete_video import delete_video_use_case


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(delete_video_use_case.keywords.keys())
    expected_keys = []
    assert actual_keys == expected_keys
