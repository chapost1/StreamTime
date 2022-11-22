import os
import ast
import json

HEALTH_CHECK_PATH = os.environ['health_check_path']

UI_HOST_URL = os.environ['ui_host_url']

RDS_HOST = os.environ['rds_address']
RDS_PORT = os.environ['rds_port']
RDS_USER = os.environ['rds_username']
RDS_PASSWORD = os.environ['rds_password']
RDS_DB = os.environ['rds_db']

AWS_REGION = os.environ.get('aws_region')
AWS_ACCESS_KEY = os.environ.get('aws_access_key', None)
AWS_SECRET_KEY = os.environ.get('aws_secret_key', None)

AWS_CONTAINER_CREDENTIALS_RELATIVE_URI = os.environ.get('AWS_CONTAINER_CREDENTIALS_RELATIVE_URI', None)

VIDEOS_BUCKET = os.environ['videos_bucket']
UPLOADDED_VIDEOS_PREFIX = os.environ['uploaded_videos_prefix']

SUPPORTED_VIDEO_TYPES = set(json.loads(json.dumps(ast.literal_eval(os.environ['allowed_video_types_to_extension']))).keys())
MAX_VIDEO_FILE_SIZE_IN_BYTES = int(float(os.environ['max_video_file_size_in_bytes']))

def is_running_as_an_ecs_task() -> bool:
    return AWS_CONTAINER_CREDENTIALS_RELATIVE_URI is not None

