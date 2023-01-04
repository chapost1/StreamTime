from .client import SQS
from .context import Context
from common.environment import GARBAGE_QUEUE_URL

garbage_queue = SQS(
    context=Context(
        queue_url=GARBAGE_QUEUE_URL
    )
)
