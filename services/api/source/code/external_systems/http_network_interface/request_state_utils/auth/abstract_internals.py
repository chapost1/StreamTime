from uuid import UUID
from typing import Protocol

class State(Protocol):
    @property
    def auth_user_id(self) -> UUID: ...

class HasState:
    @property
    def state(self) -> State: ...
