from use_cases.videos.explore_listed_videos import explore_listed_videos_use_case


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(explore_listed_videos_use_case.keywords.keys())
    expected_keys = [
        'get_visibility_settings_fn'
    ]
    assert actual_keys == expected_keys
