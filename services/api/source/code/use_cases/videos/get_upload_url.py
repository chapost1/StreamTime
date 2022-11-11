from typing import Dict
from uuid import UUID, uuid4
from data_access.abstract import VideosDB
from environment import (
    environment,
    constants
)
from aws import Boto3
from botocore.exceptions import ClientError


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


def make_get_upload_url(videos: VideosDB, boto3_session_factory: Boto3):
    async def get_upload_url(authenticated_user_id: UUID) -> Dict:
        # todo: validate user sends valid file

        hash_id = await generate_new_hash_id(videos=videos, user_id=authenticated_user_id)

        object_key = f'{environment.UPLOADDED_VIDEOS_PREFIX}/{authenticated_user_id}/{hash_id}'
        boto3 = boto3_session_factory().session()
        async with boto3.create_client('s3', region_name=environment.AWS_REGION) as client:
            try:
                response = await client.generate_presigned_post(
                    environment.VIDEOS_BUCKET,
                    object_key,
                    ExpiresIn=constants.MAXIMUM_SECONDS_TO_START_UPLOAD_A_FILE_USING_PRESIGNED_URL
                )
                return response
            except ClientError as e:
                print(f'ClientError during presigned url generation request, {e}')
                raise e

    return get_upload_url
