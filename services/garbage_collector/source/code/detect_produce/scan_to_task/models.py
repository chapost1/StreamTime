from typing import Protocol, List
from shared.models.garbage.garbage import Garbage
from dataclasses import dataclass
from shared.rds.abstract import Database


class SearchableDatabase(Database, Protocol):
    def get_garbage(self, limit: int) -> List[Garbage]:
        ...


@dataclass
class ScanToTaskStepConfig:
    garbage_type: str
    get_database: SearchableDatabase
    scan_limit: int
