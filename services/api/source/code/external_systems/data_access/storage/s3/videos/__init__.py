import common.environment as environment
from external_systems.data_access.storage.s3.client import S3
from external_systems.data_access.storage.s3.context import Context

# exports an instance of Videos relevant S3 client class
videos_s3_client = S3(Context(
    bucket=environment.VIDEOS_BUCKET,
    upload_prefix=environment.UPLOADDED_VIDEOS_PREFIX
))
