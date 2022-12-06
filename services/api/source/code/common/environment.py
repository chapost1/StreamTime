import os
import ast
import json

APP_PORT = int(os.environ.get('APP_PORT', 80))

HEALTH_CHECK_PATH = os.environ.get('health_check_path', '/health_ceck')

UI_HOST_URL = os.environ.get('ui_host_url', 'http://localhost:4200')

RDS_HOST = os.environ.get('rds_address', None)
RDS_PORT = os.environ.get('rds_port', None)
RDS_USER = os.environ.get('rds_username', None)
RDS_PASSWORD = os.environ.get('rds_password', None)
RDS_DB = os.environ.get('rds_db', None)

AWS_REGION = os.environ.get('aws_region', None)
AWS_ACCESS_KEY = os.environ.get('aws_access_key', None)
AWS_SECRET_KEY = os.environ.get('aws_secret_key', None)

AWS_CONTAINER_CREDENTIALS_RELATIVE_URI = os.environ.get('AWS_CONTAINER_CREDENTIALS_RELATIVE_URI', None)

VIDEOS_BUCKET = os.environ.get('videos_bucket', None)
UPLOADDED_VIDEOS_PREFIX = os.environ.get('uploaded_videos_prefix', None)

SUPPORTED_VIDEO_TYPES = set(json.loads(json.dumps(ast.literal_eval(
    os.environ.get('allowed_video_types_to_extension', '{}')
))).keys())
MAX_VIDEO_FILE_SIZE_IN_BYTES = int(float(
    os.environ.get('max_video_file_size_in_bytes', '0')
))

def is_running_on_amazon_infrastructure() -> bool:
    return AWS_CONTAINER_CREDENTIALS_RELATIVE_URI is not None

