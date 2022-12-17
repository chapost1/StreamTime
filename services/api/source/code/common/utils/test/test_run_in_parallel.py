from builtins import ExceptionGroup
import pytest
from common.utils import run_in_parallel
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_run_in_parallel_should_return_tasks_results_as_tuple_in_the_correct_order():
    values = [1, 2]

    one, two = await run_in_parallel(
        AsyncMock(return_value=values[0])(),
        AsyncMock(return_value=values[1])()
    )

    assert one == values[0]
    assert two == values[1]


@pytest.mark.asyncio
async def test_run_in_parallel_exception_should_be_propagated():
    mock_nie = AsyncMock(side_effect=NotImplementedError)
    mock_re = AsyncMock(side_effect=RuntimeError)

    try:
        await run_in_parallel(
            mock_nie(),
            mock_re()
        )
        # fail
        assert 1 == 2
    except ExceptionGroup as eg:
        # expected
        assert len(eg.exceptions) == 2
        assert isinstance(eg.exceptions[0], NotImplementedError)
        assert isinstance(eg.exceptions[1], RuntimeError)
