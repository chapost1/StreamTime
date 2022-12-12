from use_cases.videos.update_video import update_video_use_case


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(update_video_use_case.keywords.keys())
    expected_keys = [
        'resolve_update_state_for_pre_listing_fn',
        'resolve_update_state_for_post_listing_fn'
    ]
    assert actual_keys == expected_keys
