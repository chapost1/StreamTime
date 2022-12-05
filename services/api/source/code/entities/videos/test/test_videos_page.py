from entities.videos.videos_page import VideosPage
from entities.videos.video import Video
from entities.videos.next_page import NextPage
from typing import List
import pytest
from pydantic import ValidationError


def test_videos_property_is_requied():
    with pytest.raises(expected_exception=ValidationError):
        VideosPage()


def test_next_property_is_optional():
    vp = VideosPage(videos=[])
    assert vp.next is None


def test_calc_next_page_will_return_none_when_list_is_empty():
    assert VideosPage.calc_next_page(videos=[]) is None


def test_calc_next_page_will_return_an_encoded_next_page_with_minimal_pagination_index_the_when_valid_videos_list_is_inserted():
    videos: List[Video] = [
        # minimum is 1
        Video(pagination_index=2),
        Video(pagination_index=4),
        Video(pagination_index=1),
        Video(pagination_index=5),
        Video(pagination_index=3),
        Video(pagination_index=7),
    ]

    encoded_next_page = VideosPage.calc_next_page(videos=videos)
    next_page = NextPage.decode(b64=encoded_next_page)
    
    assert next_page.pagination_index_is_smaller_than == 1
