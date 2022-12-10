from use_cases.videos.explore_listed_videos.helpers import (
    get_visibility_settings
)


def test_get_visibility_settings_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(get_visibility_settings.keywords.keys())
    expected_keys = [
        'is_anonymous_user_fn'
    ]
    assert actual_keys == expected_keys
