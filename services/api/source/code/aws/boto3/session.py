from aiobotocore.session import (
    get_session as aio_get_session,
    AioSession
)

async def create_boto3_session(access_key: str, secret_key: str, region: str) -> AioSession:
    session: AioSession = aio_get_session()
    session.set_credentials(access_key, secret_key)
    async with session.create_client('sts', region_name=region) as client:
        # test session
        response = await client.get_caller_identity()
        print('boto3: got caller identity')
        print(response)
    return session
