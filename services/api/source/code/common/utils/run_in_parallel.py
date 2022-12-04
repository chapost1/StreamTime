import asyncio
from typing import List, Any, Awaitable, Tuple


async def run_in_parallel(*tasks: List[Awaitable]) -> Tuple[Any]:
    """
    Runs awaitables in parallel and returns the results as a list
    In case any of the awaitables raise an exception, an exception is thrown
    """

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True
    )

    output: List[Any] = []

    for result in results:
        if isinstance(result, Exception):
            raise result
        else:
            output.append(result)
    
    return tuple(output)
