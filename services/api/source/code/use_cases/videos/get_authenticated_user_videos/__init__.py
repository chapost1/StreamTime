from functools import partial
from .use_case import use_case

get_authenticated_user_videos_use_case = partial(use_case)
