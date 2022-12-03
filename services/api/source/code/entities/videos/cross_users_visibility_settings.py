from dataclasses import dataclass


@dataclass
class CrossUsersVisibilitySettings:
    hide_private: bool
    hide_unlisted: bool
