import common.environment as environment
from shared.infrastructure.storage.client import S3
from shared.infrastructure.storage.context import Context


# exports an instance of Videos relevant S3 client class
videos_s3_client = S3(
    context=Context(
        bucket=environment.VIDEOS_BUCKET
    )
)
