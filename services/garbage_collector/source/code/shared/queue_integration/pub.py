from shared.models.garbage.garbage import Garbage
from typing import Dict
import json
import base64
import logging


def garbage_to_event(garbage: Garbage) -> Dict:
    return {
        'data': base64.urlsafe_b64encode(garbage.to_message().encode()).decode()
    }


async def publish(garbage: Garbage) -> bool:
    """
    Publishes a garbage to the queue
    :param garbage: the garbage to publish
    :return: True if the garbage was published, False otherwise
    """

    try:
        # TODO: create boto3 session for each function call
        # client = boto3.session.Session().client('sqs')
        message = json.dumps(garbage_to_event(garbage=garbage))
        # TODO: produce task to queue
        logging.info(message)
    except Exception as e:
        logging.error(e)
        return False
    else:
        return True
