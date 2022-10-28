from typing import Dict
import json
import subprocess
import shlex
import boto3
import os
import datetime


s3Client = boto3.client('s3')

video_types_to_extension = {
    'video/x-msvideo': 'avi',
    'video/mp4': 'mp4',
    'video/mpeg': 'mpeg',
    'video/ogg': 'ogv',
    'video/mp2t': 'ts',
    'video/webm': 'webm',
    'video/3gpp': '3gp',
    'video/3gpp2': '3g2'
}

# VIDEO_FILE_STATES
PENDING = 'PENDING'
READY = 'READY'
DELETED = 'DELETED'

# FAILURE_REASONS
INTERNAL_ERROR_PLEASE_TRY_AGAIN_LATER = 'INTERNAL_ERROR_PLEASE_TRY_AGAIN_LATER'
MAX_FILE_SIZE_OVERFLOW = 'MAX_FILE_SIZE_OVERFLOW'
CORRUPTED = 'CORRUPTED'
NOT_A_VIDEO_TYPE = 'NOT_A_VIDEO_TYPE'

# helpers
def object_type(obj: Dict) -> str:
    return obj['ResponseMetadata']['HTTPHeaders']['content-type']
    
    
def object_size_bytes(obj: Dict) -> int:
    return obj['ContentLength']

def get_object_meta(obj: Dict, id: str) -> Dict:
    meta = {
        'id': id,
        'type': object_type(obj),
        'size_in_bytes': object_size_bytes(obj)
    }
    return meta

def get_extension_by_content_type(content_type) -> str:
    return video_types_to_extension.get(content_type, None)

def is_video_type(content_type) -> bool:
    return get_extension_by_content_type(content_type) != None

def mark_as_deleted(video_id: str, reason: str) -> None:
    # todo: mark as deleted in db
    pass

def delete_object(bucket: str, key: str) -> None:
    try:
        print('deletes object')
        response = s3Client.delete_object(
            Bucket=bucket,
            Key=key
        )
        if response['ResponseMetadata']['HTTPStatusCode'] != 204:
            raise Exception('status code is not 204')
        print('response')
        print(response)
    except Exception as e:
        print('An exception occurred: failed to delete object')
        print(e)
        return

def get_signed_url(expires_in: int, bucket: str, key: str) -> str:
    return s3Client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expires_in)

def upload_frame_as_thumbnail(s3_source_signed_url: str, duration_seconds: float, bucket: str, thumbnail_key: str) -> None:
    executable_path = '/opt/var/task/python/ffmpeg'

    mid_of_video_duration_seconds = duration_seconds / 2
    time_frame_to_extract = str(datetime.timedelta(seconds=mid_of_video_duration_seconds))# hh:mm:ss

    ffmpeg_cmd = f"{executable_path} -i \"" + str(s3_source_signed_url) + f"\" -ss {time_frame_to_extract} -vframes 1 /tmp/output.jpg"
    print(ffmpeg_cmd)
    try:
        os.system(ffmpeg_cmd)
    except Exception as e:
        print('Extract Thumbnail exception')
        print(e)
        raise e
        
    print('Going to upload thumbnail: ' + bucket + '/' + thumbnail_key)
    with open('/tmp/output.jpg', "rb") as f:
        resp = s3Client.put_object(Body=f, Bucket=bucket, Key=thumbnail_key, ACL='public-read')
        print(resp)
        print('thumbnail has been uploaded')

def get_video_duration_seconds(s3_source_signed_url: str) -> float:
    executable_path = '/opt/var/task/python/ffprobe'
    ffmpeg_cmd = f"{executable_path} \"" + str(s3_source_signed_url) + "\" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1"
    print(ffmpeg_cmd)
    try:
        result = subprocess.run(shlex.split(ffmpeg_cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        duration = float(result.stdout)
    except Exception as e:
        print('Extract Duration exception')
        print(e)
        raise e
    return duration

def lambda_handler(event, context):
    MAX_FILE_SIZE_IN_BYTES: int = 5e+9   # 5GB
    SIGNED_URL_EXPIRATION: int = 300     # The number of seconds that the Signed URL is valid

    s3Ref = event['Records'][0]['s3']
    bucket = s3Ref['bucket']['name']
    key = s3Ref['object']['key']

    try:
        obj: Dict = s3Client.get_object(
            Bucket=bucket,
            Key=key
        )
    except Exception as e:
        # internal error
        print('An exception occurred, internal error on get_object, can not even delete object yet')
        print(e)
        raise e
    
    file_name: str = key.split('/')[-1]
    video_id: str = file_name.split('.')[0]
    
    try:
        meta = get_object_meta(obj, video_id)
        print(meta)
    except Exception as e:
        delete_object(bucket, key)
        mark_as_deleted(video_id, CORRUPTED)
        print('An exception occurred, failed to get meta')
        print(e)
        return

    if MAX_FILE_SIZE_IN_BYTES < meta['size_in_bytes']:
        delete_object(bucket, key)
        mark_as_deleted(video_id, MAX_FILE_SIZE_OVERFLOW)
        return
    
    if not is_video_type(meta['type']):
        print('not a video')
        # not a video, delete file!
        delete_object(bucket, key)
        mark_as_deleted(video_id, NOT_A_VIDEO_TYPE)
    else:
        print('a video')
        # video
        try:
            # Generate a signed URL for the uploaded asset
            s3_source_signed_url: str = get_signed_url(SIGNED_URL_EXPIRATION, bucket, key)
        except Exception as e:
            delete_object(bucket, key)
            mark_as_deleted(video_id, INTERNAL_ERROR_PLEASE_TRY_AGAIN_LATER)
            print('An exception occurred, internal error')
            print(e)
            raise e

        try:
            duration_seconds: float = get_video_duration_seconds(s3_source_signed_url)

            thumbnail_key: str = f'thumbnails/{video_id}.jpg'
            upload_frame_as_thumbnail(s3_source_signed_url, duration_seconds, bucket, thumbnail_key)
        except Exception as e:
            print('Video processing exception occurred')
            print(e)
            delete_object(bucket, key)
            mark_as_deleted(video_id, CORRUPTED)

    # STATES = {PENDING, DELETED, READY}
    # todo: ON SCRIPT START, get data from meta (and set state as PENDING) (by video id) and combine with thumbnail and duration data
    # todo: create in db

    # todo: remove meta file (also when deletes object)

    # call SQS

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete successfully')
    }

