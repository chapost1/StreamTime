from use_cases.db_operation_utils.concrete import search_one_in_database
import random
import pytest
from typing import List, Any
from common.app_errors import (
    AppError,
    NotFoundError
)


@pytest.mark.asyncio
async def test_returns_first_element_of_list():
    mock = random.sample(range(1, 1000), 100)
    first = mock[0]
    class NormalSearchable:
        async def search(self) -> List[Any]:
            return mock

    result = await search_one_in_database(searchable=NormalSearchable())

    assert result == first


@pytest.mark.asyncio
async def test_if_searchable_raise_an_exception_it_is_propagated():
    class ExceptionalSearchable:
        async def search(self) -> List[Any]:
            raise AppError()
    
    try:
        await search_one_in_database(searchable=ExceptionalSearchable())
        # should not reach
        assert 2 == 1
    except AppError as ae:
        assert 1 == 1


@pytest.mark.asyncio
async def test_raise_not_found_exception_if_list_is_empty():
    class EmptySearchable:
        async def search(self) -> List[Any]:
            return []
    
    try:
        await search_one_in_database(searchable=EmptySearchable())
        # should not reach
        assert 2 == 1
    except NotFoundError as ae:
        assert 1 == 1
