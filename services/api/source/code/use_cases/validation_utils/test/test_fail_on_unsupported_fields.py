from use_cases.validation_utils.concrete import fail_on_unsupported_fields
import pytest
from common.app_errors import InputError


def test_raise_input_error_on_unsupported_fields_empty():
    with pytest.raises(expected_exception=InputError):
        fail_on_unsupported_fields(
            entity={'key': 'value'},
            supported_fields=[]
        )


def test_raise_input_error_on_unsupported_fields_not_empty():
    with pytest.raises(expected_exception=InputError):
        fail_on_unsupported_fields(
            entity={'key': 'value', 'key2': 'value2'},
            supported_fields=['key']
        )


def test_return_none_if_there_are_no_unsupported_fields():
    result = fail_on_unsupported_fields(
        entity={'key': 'value', 'key2': 'value2'},
        supported_fields=['key', 'key2']
    )

    assert result is None


def test_return_none_if_dict_is_just_empty():
    result = fail_on_unsupported_fields(
        entity={},
        supported_fields=['key', 'key2']
    )

    assert result is None
