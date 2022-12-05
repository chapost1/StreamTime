from typing import Protocol, List, Dict, Any

class Searchable(Protocol):
    async def search(self) -> List[Any]: ...


class Updatable(Protocol):
    async def update(self, new_desired_state: Dict) -> None: ...


class Deletable(Protocol):
    async def delete(self) -> None: ...

