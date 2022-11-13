from typing import Any, List, Union
from uuid import UUID
from environment import constants

def required_fields_validator(entity: Any, fields: List[str]):
    missing_fields = []
    for field in fields:
        if entity.get(field, None) is None:
            missing_fields.append(field)
    
    if 0 < len(missing_fields):
        return list(map(lambda field: f'missing required field: {field}', missing_fields))

    return None

def is_same_user(id_a: Union[UUID, str], id_b: Union[UUID, str]):
    return str(id_a) == str(id_b)    

def is_anonymous_user(user_id: Union[UUID, str]):
    return str(user_id) == constants.ANONYMOUS_USER
