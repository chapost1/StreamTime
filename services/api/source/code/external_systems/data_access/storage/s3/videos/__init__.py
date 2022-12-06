import common.environment as environment
from external_systems.data_access.storage.s3.client import S3
from external_systems.data_access.storage.s3.context import Context
from external_systems.aws_integration import Boto3


# exports an instance of Videos relevant S3 client class
videos_s3_client = S3(
    boto3=Boto3(),
    context=Context(
        bucket=environment.VIDEOS_BUCKET,
        upload_prefix=environment.UPLOADDED_VIDEOS_PREFIX
    )
)
