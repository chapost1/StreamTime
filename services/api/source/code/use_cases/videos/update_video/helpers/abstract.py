from typing import Protocol, Dict, List
from entities.videos import Video


class ResolveUpdateStateForPreListingFunction(Protocol):
    def __call__(self, video: Video) -> Dict:
        ...

class ResolveUpdateStateForPostListingFunction(Protocol):
    def __call__(self, video: Video) -> Dict:
        ...

class ParseVideoIntoStateDictFunction(Protocol):
    def __call__(self, video: Video, include_fields: List[str]) -> Dict:
        ...
