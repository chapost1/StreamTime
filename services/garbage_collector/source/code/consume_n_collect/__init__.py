from shared.infrastructure.queue import garbage_queue
from consume_n_collect.process_message import on_message

async def collect():
    """Collects garbage from the queue."""
    
    # This is the main loop of the garbage collector.
    # It will subscribe to the queue and call the callback
    # when a message is received.
    await garbage_queue.subscribe(
        on_message=on_message
    )
