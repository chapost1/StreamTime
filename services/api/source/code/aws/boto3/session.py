from typing import Optional
from aiobotocore.session import (
    get_session as aio_get_session,
    AioSession
)
from environment import environment

async def create_boto3_session(region: str, access_key: Optional[str], secret_key: Optional[str]) -> AioSession:
    session: AioSession = aio_get_session()
    if not environment.is_running_as_an_ecs_task():
        session.set_credentials(access_key, secret_key)
    async with session.create_client('sts', region_name=region) as client:
        # asserts session
        response = await client.get_caller_identity()
        print('boto3: got caller identity')
        print(response)
    return session
