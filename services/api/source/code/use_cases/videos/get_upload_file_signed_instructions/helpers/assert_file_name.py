import re
from sanitize_filename import sanitize
from common.app_errors import InputError

ALLOWED_CHARACTERS = {'a-z', 'A-Z', '0-9', '!', '@', '_', '.', '*', "'", '(', ')', '-'}

def is_valid(file_name: str) -> bool:
    m = re.match(
        pattern=r"""
        ^                        # the start of the string
        [a-zA-Z0-9!@_.*'()-]+     # 1 or more: ~abc*(def)
        (
            /
            [a-zA-Z0-9!@_.*'()-]+
        )*                       # 0 or more of /~abc*(def)
        $                        # the end of the string
        """,
        string=file_name,
        flags=re.X
    )
    is_safe_characters = m is not None
    sanitized = sanitize(file_name)
    is_safe_filename = sanitized == file_name
    not_empty = file_name != ''
    not_start_with_dot = not file_name.startswith('.')
    return is_safe_characters and is_safe_filename and not_empty and not_start_with_dot


def assert_file_name(file_name: str) -> None:
    if not is_valid(file_name):
        raise InputError(details={
            'error': f'invalid file name::{file_name}, allowed characters: {ALLOWED_CHARACTERS}'
        })
