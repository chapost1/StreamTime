from .next_page import NextPage
from .video import Video
from typing import Protocol, List


class NextPageTextDecoder(Protocol):
    def decode(self, b64: str) -> NextPage:
        ...


class NextVideosPageCalculator(Protocol):
    def calc_next_page(self, videos: List[Video]) -> str:
        ...
