import pytest
from common.utils import find_one
from common.app_errors import NotFoundError


def test_find_one_returns_first_element():
    first_item = 1
    second_item = 2
    items = [first_item, second_item]
    item = find_one(items=items)
    assert item == first_item
    assert item != second_item


def test_find_one_raise_not_found_error_if_no_elements():
    with pytest.raises(NotFoundError):
        find_one(items=[])
