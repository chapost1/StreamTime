from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
from entities.videos.video import Video
from entities.videos.next_page import NextPage


class VideosPage(BaseModel):
    videos: List[Video]
    next: Optional[str] = None


    @staticmethod
    def calc_next_page(videos: List[Video]) -> str:
        def next_page_key_lambda(video: Video) -> int:
            return video.pagination_index
        
        if len(videos) < 1:
            return None

        next_page = NextPage(
            minimum_pagination_index=min(videos, key=next_page_key_lambda).pagination_index
        )

        return next_page.encode()
