import os

HEALTH_CHECK_PATH = os.environ['health_check_path']

RDS_HOST = os.environ['rds_address']
RDS_PORT = os.environ['rds_port']
RDS_USER = os.environ['rds_username']
RDS_PASSWORD = os.environ['rds_password']
RDS_DB = os.environ['rds_db']

AWS_REGION = os.environ['aws_region']
AWS_ACCESS_KEY = os.environ['aws_access_key']
AWS_SECRET_KEY = os.environ['aws_secret_key']

VIDEOS_BUCKET = os.environ['videos_bucket']
UPLOADDED_VIDEOS_PREFIX = os.environ['uploaded_videos_prefix']
