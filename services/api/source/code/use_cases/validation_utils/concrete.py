from typing import Dict, List, Union
from uuid import UUID
import common.constants as constants
from common.app_errors import InputError

def assert_required_fields(entity: Dict, fields: List[str]) -> None:
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


def fail_on_unsupported_fields(entity: Dict, supported_fields: List[str]) -> None:
    supported = set(supported_fields)
    unsupported_fields = list(filter(lambda field: field not in supported, list(entity.keys())))
    if 0 < len(unsupported_fields):
        errors = list(map(lambda field: f'unsupported field: {field}', unsupported_fields))
        raise InputError(details={
            'errors': errors
        })

    return None


def is_same_user(id_a: Union[UUID, str], id_b: Union[UUID, str]) -> bool:
    return str(id_a) == str(id_b)    


def is_anonymous_user(user_id: Union[UUID, str]) -> bool:
    return str(user_id) == constants.ANONYMOUS_USER
