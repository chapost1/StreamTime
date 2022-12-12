import pytest
from common.utils import first_item
from common.app_errors import NotFoundError


def test_first_item_returns_first_element():
    first = 1
    second = 2
    items = [first, second]
    item = first_item(items=items)
    assert item == first
    assert item != second


def test_first_item_raise_not_found_error_if_no_elements():
    with pytest.raises(NotFoundError):
        first_item(items=[])
