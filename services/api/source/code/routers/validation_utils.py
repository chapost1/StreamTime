from typing import Any, List

def required_fields_validator(entity: Any, fields: List[str]):
    missing_fields = []
    for field in fields:
        if entity.get(field, None) is None:
            missing_fields.append(field)
    
    if 0 < len(missing_fields):
        return list(map(lambda field: f'missing required field: {field}', missing_fields))

    return None
