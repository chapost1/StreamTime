from environment import environment
from aws import Boto3

class S3:
    @staticmethod
    def get_client():
        return Boto3().session().create_client(
            's3',
            region_name=environment.AWS_REGION
        )
