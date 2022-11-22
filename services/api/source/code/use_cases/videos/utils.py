from uuid import UUID, uuid4
from typing import Union
from entities.videos import SortKeys, CrossUsersVisibilitySettings
from external_systems.data_access.rds.abstract import VideosDB
from use_cases.validation_utils import is_same_user

async def generate_new_video_hash_id_for_user(videos: VideosDB, user_id: UUID) -> UUID:
    found = False
    attempts_left = 5
    while not found:
        # should happen once on average due to probability
        hash_id = uuid4()
        video_stage = await videos.find_video_stage(user_id=user_id, hash_id=hash_id)
        if video_stage is None:
            break
        attempts_left -= 1
        if attempts_left < 1:
            raise RuntimeError('failed to create new hash_id for video upload url, after too many chances')
    return hash_id

def get_cross_users_visibility_settings(authenticated_user_id: Union[UUID, str], user_id: UUID) -> CrossUsersVisibilitySettings:
    # build visibility settings by matching selected user id to the viewer
    if is_same_user(authenticated_user_id, user_id):
        hide_private = False
        hide_unlisted = False
        sort_key = SortKeys.upload_time
    else:
        hide_private = True
        hide_unlisted = True
        sort_key = SortKeys.listing_time
    
    return CrossUsersVisibilitySettings(
        hide_private=hide_private,
        hide_unlisted=hide_unlisted,
        sort_key=sort_key
    )
