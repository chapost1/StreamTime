from use_cases.videos.get_video_upload_config import get_video_upload_config_use_case


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(get_video_upload_config_use_case.keywords.keys())
    expected_keys = []
    assert actual_keys == expected_keys
