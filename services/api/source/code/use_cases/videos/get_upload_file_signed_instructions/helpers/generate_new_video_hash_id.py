from uuid import UUID, uuid4
from external_systems.data_access.rds.abstract.videos import VideosDatabase


async def generate_new_video_hash_id(database: VideosDatabase, user_id: UUID) -> UUID:
    """Returns a unique video hash_id for particular user"""

    found = False
    attempts_left = 5
    while not found:
        # should happen once on average due to probability
        hash_id = uuid4()
        video_stage = await database.find_video_stage(
            user_id=user_id,
            hash_id=hash_id
        )
        if video_stage is None:
            break
        attempts_left -= 1
        if attempts_left < 1:
            raise RuntimeError('failed to create new hash_id for video upload url, after too many chances')
    return hash_id
