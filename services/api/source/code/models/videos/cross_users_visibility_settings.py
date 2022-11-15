from dataclasses import dataclass
from models.videos.enums import SortKeys


@dataclass
class CrossUsersVisibilitySettings:
    hide_private: bool
    hide_unlisted: bool
    sort_key: SortKeys
