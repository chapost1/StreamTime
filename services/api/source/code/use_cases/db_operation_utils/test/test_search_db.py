from use_cases.db_operation_utils.concrete import search_db
from typing import List, Any
import random
import pytest
from common.app_errors import AppError


@pytest.mark.asyncio
async def test_returns_a_list_as_the_searchable_returns():
    mock = random.sample(range(1, 1000), 100)
    class NormalSearchable:
        async def search(self) -> List[Any]:
            return mock
    
    assert await search_db(searchable=NormalSearchable()) == mock


@pytest.mark.asyncio
async def test_if_searchable_raise_an_exception_it_is_propagated():
    class ExceptionalSearchable:
        async def search(self) -> List[Any]:
            raise AppError()
    
    try:
        await search_db(searchable=ExceptionalSearchable())
        # should not reach
        assert 2 == 1
    except AppError as ae:
        assert 1 == 1
