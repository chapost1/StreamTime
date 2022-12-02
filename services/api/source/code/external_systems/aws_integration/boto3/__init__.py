from external_systems.aws_integration.boto3.boto3 import Boto3
from external_systems.aws_integration.boto3.session import create_boto3_session
import common.environment as environment

async def init() -> None:
    """Initialize the Singleton boto3 client using the async boto3 session"""

    session = await create_boto3_session(
        region=environment.AWS_REGION,
        access_key=environment.AWS_ACCESS_KEY,
        secret_key=environment.AWS_SECRET_KEY
    )

    Boto3(session)
