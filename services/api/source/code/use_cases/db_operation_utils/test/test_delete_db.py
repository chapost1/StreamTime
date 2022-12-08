from use_cases.db_operation_utils.concrete import delete_in_database
import pytest
from common.app_errors import AppError


@pytest.mark.asyncio
async def test_should_return_none_on_successful_delete():
    class SuccessulDeleter:
        async def delete(self) -> None:
            return None
    
    assert await delete_in_database(deletable=SuccessulDeleter()) is None


@pytest.mark.asyncio
async def test_should_propagate_exception():
    class ExceptionalDeletable:
        async def delete(self) -> None:
            raise AppError()
    
    try:
        await delete_in_database(deletable=ExceptionalDeletable())
        # should not reach
        assert 2 == 1
    except AppError as ae:
        assert 1 == 1
