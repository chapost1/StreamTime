from shared.models.garbage.garbage import Garbage
from typing import Dict
import json
import base64


def garbage_to_event(garbage: Garbage) -> Dict:
    return {
        'data': base64.urlsafe_b64encode(garbage.to_message().encode()).decode()
    }


def publish(garbage: Garbage) -> None:
    message = json.dumps(garbage_to_event(garbage=garbage))
    # TODO: produce task to queue
    print(message)
