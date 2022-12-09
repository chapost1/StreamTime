from functools import partial
from .use_case import use_case
from entities.videos import NextPage, VideosPage
from .helpers import get_visibility_settings


explore_listed_videos_use_case = partial(
    use_case,
    get_visibility_settings_fn=get_visibility_settings
)
