from shared.garbage.garbage import Garbage
from typing import Optional
from uuid import UUID
import json
from dataclasses import dataclass


@dataclass
class UploadedVideo(Garbage):
    hash_id: Optional[UUID]
    user_id: Optional[UUID]


    def to_message(self) -> str:
        return json.dumps(
            {
                'type': self.type,
                'user_id': str(self.user_id),
                'hash_id': str(self.hash_id)
            }
        )
