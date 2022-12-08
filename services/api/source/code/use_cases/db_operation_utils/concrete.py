from typing import List, Dict, Any
from common.utils import find_one
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable,
    Updatable,
    Deletable
)

async def search_in_database(searchable: Searchable) -> List[Any]:
    return await searchable.search()


async def search_one_in_database(searchable: Searchable) -> Any:
    return find_one(
        items=await search_in_database(searchable=searchable)
    )


async def update_in_database(updatable: Updatable, new_desired_state: Dict) -> None:
    await updatable.update(new_desired_state=new_desired_state)


async def delete_in_database(deletable: Deletable) -> None:
    await deletable.delete()
