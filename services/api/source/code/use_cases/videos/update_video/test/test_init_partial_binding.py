from use_cases.videos.update_video import update_video_use_case


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(update_video_use_case.keywords.keys())
    expected_keys = [
        'search_one_in_database_fn',
        'update_in_database_fn',
        'describe_videos_in_database_fn',
        'prepare_new_listing_before_publish_fn',
        'prepare_listed_record_before_update_fn',
        'parse_video_into_state_dict_fn'
    ]
    assert actual_keys == expected_keys
