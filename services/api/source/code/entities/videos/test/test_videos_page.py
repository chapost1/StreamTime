from entities.videos.videos_page import VideosPage
from entities.videos.video import Video
from entities.videos.next_page import NextPage
from typing import List
import pytest
from pydantic import ValidationError
import random


def test_videos_property_is_requied():
    with pytest.raises(expected_exception=ValidationError):
        VideosPage()


def test_next_property_is_optional():
    vp = VideosPage(videos=[])
    assert vp.next is None


def test_calc_next_page_will_return_none_when_list_is_empty():
    assert VideosPage.calc_next_page(videos=[]) is None


def test_calc_next_page_will_return_an_encoded_next_page_with_minimal_pagination_index_the_when_valid_videos_list_is_inserted():
    videos: List[Video] = []
    max_boundary = 65535
    min_pi = max_boundary + 1
    for _ in range(0, random.randint(5, 25)):
        local_min = random.randint(1, max_boundary)
        if local_min < min_pi:
            min_pi = local_min
        videos.append(Video(pagination_index=local_min))

    encoded_next_page = VideosPage.calc_next_page(videos=videos)
    next_page = NextPage.decode(b64=encoded_next_page)
    
    assert next_page.pagination_index_is_smaller_than == min_pi
