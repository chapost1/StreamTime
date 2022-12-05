from typing import Any, List, Union
from uuid import UUID
import common.constants as constants
from common.app_errors import InputError

def assert_required_fields(entity: Any, fields: List[str]) -> None:
    missing_fields = []
    for field in fields:
        if entity.get(field, None) is None:
            missing_fields.append(field)
    
    if 0 < len(missing_fields):
        errors = list(map(lambda field: f'missing required field: {field}', missing_fields))
        raise InputError(details={
            'errors': errors
        })


    return None


def is_same_user(id_a: Union[UUID, str], id_b: Union[UUID, str]) -> bool:
    return str(id_a) == str(id_b)    


def is_anonymous_user(user_id: Union[UUID, str]) -> bool:
    return str(user_id) == constants.ANONYMOUS_USER
