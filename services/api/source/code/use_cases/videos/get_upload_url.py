from typing import Dict
from uuid import UUID, uuid4
from data_access.rds.abstract import VideosDB
from data_access.storage.abstract import Storage
from models.storage import FileUploadUrlRecord


async def generate_new_hash_id(videos: VideosDB, user_id: UUID) -> UUID:
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


def make_get_upload_url(videos: VideosDB, storage: Storage):
    async def get_upload_url(authenticated_user_id: UUID) -> FileUploadUrlRecord:
        # todo: validate user sends valid file

        hash_id = await generate_new_hash_id(videos=videos, user_id=authenticated_user_id)

        object_key = f'{authenticated_user_id}/{hash_id}'

        return await storage.get_upload_file_url(
            item_relative_path=object_key
        )

    return get_upload_url
