from uuid import UUID, uuid4
from data_access.rds.abstract import VideosDB

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
