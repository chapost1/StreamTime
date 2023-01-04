from typing import Awaitable
from dataclasses import dataclass


@dataclass
class ScanToTaskStepConfig:
    garbage_type: str
    detect_garbage_fn: Awaitable[None]
