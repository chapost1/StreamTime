from dataclasses import dataclass


@dataclass
class Context:
    """Context to conatain on what the SQS client should work on"""

    queue_url: str
