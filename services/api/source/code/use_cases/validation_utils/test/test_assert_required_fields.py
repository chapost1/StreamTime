from use_cases.validation_utils.concrete import assert_required_fields
import pytest
from common.app_errors import InputError


def test_raise_an_exception_when_field_is_missing():
    with pytest.raises(expected_exception=InputError):
        assert assert_required_fields({}, ['key'])


def test_raised_exception_is_as_the_same_count_of_missing_fileds():
    fields = ['key', 'name', 'date']
    try:
        assert_required_fields({'message': 'hello world!'}, fields)
        # should not get here
        assert 2 == 1
    except InputError as e:
        assert e.details is not None
        assert len(e.details['errors']) == len(fields)


def test_returns_none_if_no_fields_are_missing():
    assert assert_required_fields({'message': 'hello world!', 'key': 'val'}, ['message', 'key']) is None


def test_returns_none_if_fields_are_empty():
    assert assert_required_fields({'message': 'hello world!', 'key': 'val'}, []) is None
