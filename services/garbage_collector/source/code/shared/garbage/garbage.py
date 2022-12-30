from dataclasses import dataclass
import json


@dataclass
class Garbage:
    """Represents a garbage entity."""
    type: str


    def delete(self) -> None:
        """Deletes the garbage entity."""
        raise NotImplementedError


    def to_message(self) -> str:
        """Returns a message representation of the garbage entity."""
        return json.dumps(
            {
                'type': self.type
            }
        )


    def __str__(self) -> str:
        return self.to_message()