from entities.videos.next_page import NextPage
import pytest
from common.app_errors import InputError
import random


def test_encode_returns_a_next_as_str():
    next_page = NextPage(pagination_index_is_smaller_than=random.randint(1, 100))
    assert isinstance(next_page.encode(), str) == True


def test_decode_returns_empty_next_page_when_str_is_none():
    next_page = NextPage.decode(b64=None)
    assert next_page.pagination_index_is_smaller_than is None


def test_decode_raise_an_exception_if_str_is_invalid():
    with pytest.raises(expected_exception=InputError):
        NextPage.decode(b64='invalid string...')


def test_decode_raise_an_exception_if_str_is_valid_next_page_but_empty_one():
    next_string = NextPage.decode(b64=None).encode()
    with pytest.raises(expected_exception=InputError):
        NextPage.decode(b64=next_string)


def test_decode_should_return_a_valid_next_page_if_str_is_completely_valid_one():
    # this test is also includes an encode decode flow in it
    random_number = random.randint(1, 100)
    next_page = NextPage(pagination_index_is_smaller_than=random_number)
    next_page_string = next_page.encode()
    valid_next_page = NextPage.decode(b64=next_page_string)
    assert valid_next_page.pagination_index_is_smaller_than == random_number
