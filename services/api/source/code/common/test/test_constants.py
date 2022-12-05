from common.constants import (
    ANONYMOUS_USER,
    LISTED_VIDEOS_QUERY_PAGE_LIMIT,
    MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION,
    MAXIMUM_SECONDS_TO_START_UPLOAD_A_FILE_USING_PRESIGNED_URL
)


def test_assert_anonymouse_user_mark():
    assert ANONYMOUS_USER == 'anonymous'


def test_assert_listed_videos_query_page_limit():
    # this number is relatively small and yet it is divisable by: 1, 2, 3, 4, 5, 6...
    # (all the numbers which is potentially the count of items to display on the same time while exploring)
    # which are good for UX
    assert LISTED_VIDEOS_QUERY_PAGE_LIMIT == 30


def test_assert_max_upload_expiration_time_is_no_longer_than_one_minute():
    # for security purposes
    # note: using the client, even 5 seconds should be more than enough
    assert MAXIMUM_SECONDS_TO_START_UPLOAD_A_FILE_USING_PRESIGNED_URL <= 60


def test_assert_max_watch_file_expiration_time():
    # as far as it is known, this is seven days
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html
    assert MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION == 7 * 24 * 3600
