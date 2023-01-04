import common.environment as environment
from shared.infrastructure.aws_integration import Boto3
from botocore.exceptions import ClientError
from shared.infrastructure.storage.context import Context
import logging

logger = logging.getLogger(__name__)


class S3:
    f"""
    S3 as a storage service client.
    """

    def __init__(self, context: Context):
        self.context = context


    def __get_client(self):
        return Boto3().session().create_client(
            's3',
            region_name=environment.AWS_REGION
        )


    async def delete_file(self, item_relative_path: str) -> None:
         async with self.__get_client() as client:
            try:
                await client.delete_object(
                    Bucket=self.context.bucket,
                    Key=item_relative_path
                )
            except ClientError as e:
                logger.error(f'Client error during S3 delete object op, {e}')
                raise e
