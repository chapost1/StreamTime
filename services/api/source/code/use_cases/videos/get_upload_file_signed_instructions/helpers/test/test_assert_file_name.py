from use_cases.videos.get_upload_file_signed_instructions.helpers.assert_file_name import (
    assert_file_name,
    is_valid
)
from common.app_errors import InputError
import pytest


def test_assert_file_name__valid() -> None:
    assert_file_name(file_name='valid-file-name.mp4')


def test_assert_file_name__invalid() -> None:
    with pytest.raises(expected_exception=InputError):
        assert_file_name(file_name='invalid file name^.mp4')


@pytest.mark.parametrize(
    'file_name,expected',
    [
        ('valid-file-name.mp4', True),
        ('s!.mp4', True),
        ('s^.mp4', False),
        ('s$.mp4', False),
        ('s*.mp4', False),
        ('s(.mp4', True),
        ('s).mp4', True),
        ('s[.mp4', False),
        ('s].mp4', False),
        ('s{.mp4', False),
        ('s}.mp4', False),
        ('s|.mp4', False),
        ('s\\.mp4', False),
        ('s/.mp4', False),
        ('s?.mp4', False),
        ('s<.mp4', False),
        ('s>.mp4', False),
        ('s;.mp4', False),
        ('s:.mp4', False),
        ('s".mp4', False),
        ('s\'.mp4', True),
        ('s`.mp4', False),
        ('s~.mp4', False),
        ('s=.mp4', False),
        ('s+.mp4', False),
        ('s-.mp4', True),
        ('s_.mp4', True),
        ('s!.mp4', True),
        ('s@.mp4', True),
        ('s#.mp4', False),
        ('s$.mp4', False),
        ('s%.mp4', False),
        ('s^.mp4', False),
        ('s&.mp4', False),
        ('', False),
        ('.mp4', False),
    ]

)
def test_is_valid(file_name: str, expected: bool) -> None:
    assert is_valid(file_name) == expected
