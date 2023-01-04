from shared.models.garbage.garbage import Garbage
from shared.models.garbage.factory import GarbageFactory
from typing import Dict
import json
import base64


def event_to_garbage(event: Dict) -> Garbage:
    b64: str = event['data']
    kwargs = json.loads(base64.urlsafe_b64decode(b64.encode()).decode())
    return GarbageFactory.create(**kwargs)


async def subscribe():
    ...
