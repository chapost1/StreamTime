from use_cases.videos.get_specific_user_listed_videos import get_specific_user_listed_videos_use_case


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(get_specific_user_listed_videos_use_case.keywords.keys())
    expected_keys = [
        'search_in_database_fn',
        'describe_videos_in_database_fn',
        'next_page_text_decoder',
        'next_videos_page_calculator'
    ]
    assert actual_keys == expected_keys
