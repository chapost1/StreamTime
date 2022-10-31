import os

print(os.environ)

HEALTH_CHECK_PATH = os.environ['health_check_path']

RDS_HOST = os.environ['rds_address']
RDS_PORT = os.environ['rds_port']
RDS_USER = os.environ['rds_username']
RDS_PASSWORD = os.environ['rds_password']
RDS_DB = os.environ['rds_db']
