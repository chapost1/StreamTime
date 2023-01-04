from shared.models.garbage.garbage import Garbage
from shared.models.garbage.factory import GarbageFactory
import json
import base64

def garbage_to_message(garbage: Garbage) -> str:
    return json.dumps({
        'data': base64.urlsafe_b64encode(garbage.to_message().encode()).decode()
    })


def message_to_garbage(message: str) -> Garbage:
    json_message = json.loads(message)
    b64: str = json_message['data']
    kwargs = json.loads(base64.urlsafe_b64decode(b64.encode()).decode())
    return GarbageFactory.create(**kwargs)
