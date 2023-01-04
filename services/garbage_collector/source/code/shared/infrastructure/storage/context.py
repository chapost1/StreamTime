from dataclasses import dataclass


@dataclass
class Context:
    """Context to conatain on what the S3 client should work on"""

    bucket: str
