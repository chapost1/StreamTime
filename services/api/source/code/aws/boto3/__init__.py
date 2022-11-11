from aws.boto3.boto3 import Boto3
from aws.boto3.session import create_boto3_session
from environment import environment

async def init() -> None:
    session = await create_boto3_session(
        access_key=environment.AWS_ACCESS_KEY,
        secret_key=environment.AWS_SECRET_KEY,
        region=environment.AWS_REGION
    )
    Boto3(session)
