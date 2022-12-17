import asyncio
from builtins import ExceptionGroup
from typing import List, Any, Awaitable, Tuple


async def run_in_parallel(*tasks: List[Awaitable]) -> Tuple[Any]:
    """
    Runs awaitables in parallel and returns the results as a tuple in the same order as the awaitables
    In case any of the awaitables raises exceptions, the exceptions are thrown in an ExceptionGroup
    """

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True
    )

    exceptions = [result for result in results if isinstance(result, Exception)]
    # if any of the tasks raised an exception, raise an exception group
    if exceptions:
        raise ExceptionGroup('coudln\'t run in parallel', exceptions)

    return tuple(results)
