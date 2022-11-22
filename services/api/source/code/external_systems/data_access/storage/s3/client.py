from environment import (
    environment,
    constants
)
from external_systems.aws_integration import Boto3
from botocore.exceptions import ClientError
from entities.storage import FileUploadSignedInstructions
from external_systems.data_access.storage.s3.context import Context

class S3:
    def __init__(self, context: Context):
        self.context = context

    def __get_client(self):
        return Boto3().session().create_client(
            's3',
            region_name=environment.AWS_REGION
        )
    
    async def prepare_bucket_region(self) -> None:
        if self.context.region is not None:
            return
        async with self.__get_client() as client:
            try:
                response = await client.get_bucket_location(Bucket=self.context.bucket)
                self.context.region = response['LocationConstraint']
            except ClientError as e:
                print(f'Client error during fetching bucket region, {e}')
                raise e

    
    async def get_upload_file_signed_instructions(self, item_relative_path: str, file_content_type: str) -> FileUploadSignedInstructions:
        await self.prepare_bucket_region()
        async with self.__get_client() as client:
            object_key = f'{self.context.upload_prefix}/{item_relative_path}'
            try:
                response = await client.generate_presigned_post(
                    self.context.bucket,
                    object_key,
                    Fields={'Content-Type': file_content_type},
                    Conditions=[
                        ['starts-with', '$Content-Type', file_content_type]
                    ],
                    ExpiresIn=constants.MAXIMUM_SECONDS_TO_START_UPLOAD_A_FILE_USING_PRESIGNED_URL
                )
                # creating bucket url with region to avoid 5xx errors until DNS propagation is fully done
                # https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingRouting.html
                url = f'https://{self.context.bucket}.s3-{self.context.region}.amazonaws.com/'
                return FileUploadSignedInstructions(
                    url=url,
                    signatures=response['fields']
                )
            except ClientError as e:
                print(f'Client error during S3 presigned url creation, {e}')
                raise e

    
    async def get_file_signed_url(self, item_relative_path: str, signature_duration_seconds: int) -> str:
        async with self.__get_client() as client:
            try:
                response = await client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': self.context.bucket,
                        'Key': item_relative_path
                    },
                    ExpiresIn=signature_duration_seconds
                )
                if response is None:
                    err = f'S3 create GET signed url - no response. respone={response}'
                    print(err)
                    raise Exception(err)

                return response  
            except ClientError as e:
                print(f'Client error during S3 create GET signed url, {e}')
                raise e


    async def delete_file(self, item_relative_path: str) -> None:
         async with self.__get_client() as client:
            try:
                await client.delete_object(
                    Bucket=self.context.bucket,
                    Key=item_relative_path
                )
            except ClientError as e:
                print(f'Client error during S3 delete object op, {e}')
                raise e
