from functools import partial
from .explore_listed_videos import explore_listed_videos as __explore_listed_videos
from .search_videos import search_videos
from .next_videos_page import next_videos_page

next_videos_page_fn = partial(next_videos_page, search_videos_fn=search_videos)

explore_listed_videos = partial(__explore_listed_videos, next_videos_page_fn=next_videos_page_fn)
