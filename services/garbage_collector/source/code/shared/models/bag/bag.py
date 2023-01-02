from dataclasses import dataclass
from typing import Callable


@dataclass
class GarbageBag:
    """Represents a garbage bag."""

    collect_fn: Callable


    def collect(self) -> None:
        self.collect_fn()
