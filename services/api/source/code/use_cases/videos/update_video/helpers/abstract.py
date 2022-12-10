from typing import Protocol, Dict
from entities.videos import Video


class PrepareNewListingBeforePublishFunction(Protocol):
    def __call__(self, video: Video) -> Video:
        ...

class PrepareListedRecordBeforeUpdateFunction(Protocol):
    def __call__(self, video: Video) -> Video:
        ...

class ParseVideoIntoStateDictFunction(Protocol):
    def __call__(self, video: Video) -> Dict:
        ...
