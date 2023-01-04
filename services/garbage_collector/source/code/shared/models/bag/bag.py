from dataclasses import dataclass
from typing import Awaitable


@dataclass
class GarbageBag:
    """Represents a garbage bag."""

    collect_fn: Awaitable[None]


    async def collect(self) -> None:
        await self.collect_fn()
