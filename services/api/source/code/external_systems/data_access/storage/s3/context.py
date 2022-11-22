from dataclasses import dataclass

@dataclass
class Context:
    bucket: str
    upload_prefix: str
