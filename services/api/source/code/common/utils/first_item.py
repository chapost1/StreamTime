from typing import List, Any
from common.app_errors import NotFoundError


def first_item(items: List[Any]) -> Any:
    """Takes first element of list, if none, raises an exception"""

    if len(items) < 1:
        raise NotFoundError()

    return items[0]
