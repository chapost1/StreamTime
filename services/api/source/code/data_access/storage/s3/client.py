from environment import (
    environment,
    constants
)
from aws import Boto3
from botocore.exceptions import ClientError
from models.storage import FileUploadSignedInstructions
from data_access.storage.s3.context import Context

class S3:
    def __init__(self, context: Context):
        self.context = context

    def __get_client(self):
        return Boto3().session().create_client(
            's3',
            region_name=environment.AWS_REGION
        )
    
    async def get_upload_file_signed_instructions(self, item_relative_path: str) -> FileUploadSignedInstructions:
        async with self.__get_client() as client:
            object_key = f'{self.context.upload_prefix}/{item_relative_path}'
            try:
                response = await client.generate_presigned_post(
                    self.context.bucket,
                    object_key,
                    ExpiresIn=constants.MAXIMUM_SECONDS_TO_START_UPLOAD_A_FILE_USING_PRESIGNED_URL
                )
                return FileUploadSignedInstructions(
                    url=response['url'],
                    signatures=response['fields']
                )
            except ClientError as e:
                print(f'Client error during S3 presigned url creation, {e}')
                raise e
