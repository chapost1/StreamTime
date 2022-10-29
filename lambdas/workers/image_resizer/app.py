from typing import Tuple
import json
import boto3
import os
from PIL import Image

s3Client = boto3.client('s3')

def resize_image(image_path: str, resized_path: str, size: Tuple[int, int]):
  with Image.open(image_path) as image:
      image.thumbnail(size)
      image.save(resized_path)

def lambda_handler(event, context):
    try:
        ACL = event.get('ACL', 'private')
        source_bucket = event['source_bucket']
        dest_bucket = event['dest_bucket']
        source_file_key = event['source_file_key']
        dest_file_key = event['dest_file_key']
        file_name = source_file_key.split('/')[-1]
        temp_file_path = f'/tmp/{file_name}'
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        with open(temp_file_path, 'wb') as f:
            s3Client.download_fileobj(source_bucket, source_file_key, f)

        new_file_path = f'/tmp/resized_{file_name}'
        if os.path.exists(new_file_path):
            os.remove(new_file_path)

        resize_image(
            temp_file_path,
            new_file_path,
            tuple(event['new_size'])
        )

        print('Going to upload resized image: ' + dest_bucket + '/' + dest_file_key)
        with open(new_file_path, "rb") as f:
            resp = s3Client.put_object(Body=f, Bucket=dest_bucket, Key=dest_file_key, ACL=ACL)
            print(resp)
            print('Resized imaged has been uploaded')


    except Exception as e:
        print('Exception')
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete successfully')
    }

