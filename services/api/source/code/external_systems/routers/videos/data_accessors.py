from environment import environment
from external_systems.data_access.rds.pg import Videos
from external_systems.data_access.storage.s3.client import S3
from external_systems.data_access.storage.s3.context import Context

videos_s3_client = S3(Context(
    bucket=environment.VIDEOS_BUCKET,
    upload_prefix=environment.UPLOADDED_VIDEOS_PREFIX
))

videos_db_client = Videos()
