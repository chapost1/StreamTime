from use_cases.videos.get_upload_file_signed_instructions import get_upload_video_signed_instructions_use_case


def test_partial_binded_kwargs_are_the_expected_ones():
    actual_keys = list(get_upload_video_signed_instructions_use_case.keywords.keys())
    expected_keys = [
        'generate_new_video_hash_id_fn',
        'assert_file_name_fn',
        'assert_file_content_type_fn'
    ]
    assert actual_keys == expected_keys
