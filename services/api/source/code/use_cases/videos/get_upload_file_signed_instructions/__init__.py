from .use_case import use_case
from functools import partial
from .helpers import (
    generate_new_video_hash_id,
    assert_file_content_type
)


get_upload_video_signed_instructions_use_case = partial(
    use_case,
    generate_new_video_hash_id_fn=generate_new_video_hash_id,
    assert_file_content_type_fn=assert_file_content_type
)
