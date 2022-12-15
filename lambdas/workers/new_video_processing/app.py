from typing import Dict, Tuple, Any
import ast
import json
import subprocess
import shlex
import boto3
import os
import datetime


# CONSTANTS
EXECUTABLES_DIRECTORY = '/opt/var/task/python'
THUMBNAIL_SIZE = (360, 200)

##########################
######## ENV VARS ########
##########################
# PROCESSING EVENTS
PROCESSING_HAS_BEEN_STARTED_EVENT_ENV_NAME = 'new_video_events_processing_has_been_started'
PROCESSING_FAILED_EVENT_ENV_NAME = 'new_video_events_processing_failure'
PROCESSED_VIDEO_MOVED_TO_DRAFTS_EVENT_ENV_NAME = 'new_video_events_moved_to_drafts'
# S3 prefixes
THUMBNAILS_PREFIX_ENV_NAME = 's3_thumbnails_prefix'
VIDEOS_PREFIX_ENV_NAME = 's3_videos_prefix'
UPLOADED_VIDEOS_PREFIX_ENV_NAME = 's3_uploaded_videos_prefix'
UNPROCESSED_VIDEOS_PREFIX_ENV_NAME = 's3_unprocessed_videos_prefix'
# S3 restrictions
S3_THUMBNAILS_ACL_ENV_NAME = 's3_thumbnails_acl'
S3_MAX_VIDEO_SIZE_IN_BYTES_ENV_NAME = 's3_max_video_file_size_in_bytes'
ALLOWED_VIDEO_TYPES_TO_EXTENSION = 'allowed_video_types_to_extension'
# FAILURE REASONS
INTERNAL_ERROR_ENV_NAME = 'new_video_processing_failure_internal_error'
MAX_FILE_SIZE_EXCEEDED_ENV_NAME = 'new_video_processing_failure_max_file_size_exceeded'
CORRUPTED_ENV_NAME = 'new_video_processing_failure_corrupted'
UNSUPPORTED_FILE_FORMAT_ENV_NAME = 'new_video_processing_failure_unsupported_video_type'
# uploaded_video_feedback_event
UPLOADED_VIDEO_FEEDBACK_EVENT = 'uploaded_video_feedback_event'
# ARNs
IMAGE_RESIZER_LAMBDA_ARN_ENV_NAME = 'image_resizer_lambda_arn'
VIDEOS_RDS_UPDATE_LAMBDA_ARN_ENV_NAME = 'videos_rds_update_arn'
NOTIFY_CLIENT_SNS_TOPIC = 'uploaded_videos_client_sync_sns_topic_arn'


s3Client = boto3.client('s3')
sns = boto3.client('sns')


def get_utc_timestamp_of_the_next_n_hours(hours: int = 0) -> int:
    return int(datetime.datetime.utcnow().timestamp()) + hours * 3600


def object_type(obj: Dict) -> str:
    return obj['ResponseMetadata']['HTTPHeaders']['content-type']


def object_size_bytes(obj: Dict) -> int:
    return obj['ContentLength']


def get_object_meta(obj: Dict) -> Dict:
    meta = {
        'type': object_type(obj),
        'size_in_bytes': object_size_bytes(obj)
    }
    return meta


def get_extension_by_content_type(content_type: str) -> str:
    video_types_to_extension = json.loads(json.dumps(ast.literal_eval(os.environ[ALLOWED_VIDEO_TYPES_TO_EXTENSION])))
    return video_types_to_extension.get(content_type, None)


def is_supported_video_type(content_type: str) -> bool:
    return get_extension_by_content_type(content_type) != None


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


def get_video_duration_seconds(s3_source_signed_url: str) -> float:
    executable_path = f'{EXECUTABLES_DIRECTORY}/ffprobe'
    ffmpeg_cmd = f"{executable_path} \"" + str(s3_source_signed_url) + \
        "\" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1"
    print(ffmpeg_cmd)
    try:
        result = subprocess.run(shlex.split(
            ffmpeg_cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        duration = float(result.stdout)
    except Exception as e:
        print('Extract Duration exception')
        print(e)
        raise e
    
    return duration


def run_ffmpeg_thumbnail_extraction_command(command) -> Any:
    print(command)
    try:
        subprocess.call(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        print('Extract Thumbnail exception')
        print(e)
        raise e


def upload_frame_as_thumbnail(s3_source_signed_url: str, duration_seconds: float, bucket: str, thumbnail_key: str) -> None:
    executable_path = f'{EXECUTABLES_DIRECTORY}/ffmpeg'

    mid_of_video_duration_seconds = int(duration_seconds / 3)
    frame_path = '/tmp/frame.png'
    
    if os.path.exists(frame_path):
        os.remove(frame_path)

    ffmpeg_cmd = f"{executable_path} -ss {mid_of_video_duration_seconds} -i \"" + \
        str(s3_source_signed_url) + f"\" -vframes 1 -vcodec png -an -y {frame_path}"
    run_ffmpeg_thumbnail_extraction_command(ffmpeg_cmd)
    
    if not os.path.exists(frame_path):
        # fallback extract first frame - usually happens on very large files - will finish quickly as a last resort solution
        ffmpeg_cmd = f"{executable_path} -y -i \"" + \
            str(s3_source_signed_url) + f"\" -vframes 1 {frame_path}"
        run_ffmpeg_thumbnail_extraction_command(ffmpeg_cmd)

    print('Going to upload thumbnail: ' + bucket + '/' + thumbnail_key)
    with open(frame_path, "rb") as f:
        resp = s3Client.put_object(
            Body=f, Bucket=bucket, Key=thumbnail_key, ACL=os.environ[S3_THUMBNAILS_ACL_ENV_NAME])
        print(resp)
        print('Thumbnail has been uploaded')


def resize_thumbnail(bucket: str, thumbnail_key: str, new_size=Tuple[int, int]) -> None:
    lambdaClient = boto3.client('lambda')
    try:
        response = lambdaClient.invoke(
            FunctionName=os.environ[IMAGE_RESIZER_LAMBDA_ARN_ENV_NAME],
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'source_file_key': thumbnail_key,
                'dest_file_key': thumbnail_key,
                'source_bucket': bucket,
                'dest_bucket': bucket,
                'new_size': list(new_size),
                'ACL': os.environ[S3_THUMBNAILS_ACL_ENV_NAME]
            })
        )
        responseFromChild = json.load(response['Payload'])
    except Exception as e:
        print('Error during waiting for response from child')
        print(e)
        raise e
    print(responseFromChild)


def assert_necessery_env_are_here() -> None:
    for env in [IMAGE_RESIZER_LAMBDA_ARN_ENV_NAME, THUMBNAILS_PREFIX_ENV_NAME,
                VIDEOS_PREFIX_ENV_NAME, UNPROCESSED_VIDEOS_PREFIX_ENV_NAME,
                UPLOADED_VIDEOS_PREFIX_ENV_NAME, S3_THUMBNAILS_ACL_ENV_NAME,
                S3_MAX_VIDEO_SIZE_IN_BYTES_ENV_NAME, INTERNAL_ERROR_ENV_NAME,
                MAX_FILE_SIZE_EXCEEDED_ENV_NAME, CORRUPTED_ENV_NAME,
                UNSUPPORTED_FILE_FORMAT_ENV_NAME, VIDEOS_RDS_UPDATE_LAMBDA_ARN_ENV_NAME,
                UPLOADED_VIDEO_FEEDBACK_EVENT, NOTIFY_CLIENT_SNS_TOPIC,
                PROCESSING_HAS_BEEN_STARTED_EVENT_ENV_NAME, PROCESSING_FAILED_EVENT_ENV_NAME,
                PROCESSED_VIDEO_MOVED_TO_DRAFTS_EVENT_ENV_NAME,
                ALLOWED_VIDEO_TYPES_TO_EXTENSION
                ]:
        if os.environ.get(env, None) is None:
            raise RuntimeError(f'missing env varialbe: {env}')


def send_sns(user_id: str, hash_id: str, event: str) -> None:
    message = {
        'default': json.dumps({
            'user_id': user_id,
            'hash_id': hash_id,
            'event': event,
            'trigger': os.environ[UPLOADED_VIDEO_FEEDBACK_EVENT]
        })
    }
    try:
        response = sns.publish(
            TargetArn=os.environ[NOTIFY_CLIENT_SNS_TOPIC],
            Message=json.dumps(message),
            MessageStructure='json'
        )
        print('send sns response')
        print(response)
    except Exception as e:
        print('failed to send SNS')
        print(message)
        print(e)
        raise e


def update_rds(record: Dict, trigger: str) -> None:
    lambdaClient = boto3.client('lambda')
    try:
        response = lambdaClient.invoke(
            FunctionName=os.environ[VIDEOS_RDS_UPDATE_LAMBDA_ARN_ENV_NAME],
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'trigger': trigger,
                'record': record
            })
        )
        responseFromChild = json.load(response['Payload'])
        if responseFromChild.get('errorMessage', None) is not None:
            raise Exception(responseFromChild['errorMessage'])
    except Exception as e:
        print('Error during waiting for response from child')
        print(e)
        raise e
    print(responseFromChild)


def mark_upload_as_unprocessed(user_id: str, hash_id: str, upload_time: str) -> None:
    print('mark_upload_as_unprocessed')
    update_rds({
        'user_id': user_id,
        'hash_id': hash_id,
        'upload_time': upload_time,
    }, os.environ[PROCESSING_HAS_BEEN_STARTED_EVENT_ENV_NAME])

    send_sns(user_id, hash_id,
             os.environ[PROCESSING_HAS_BEEN_STARTED_EVENT_ENV_NAME])


def mark_processing_as_failed(user_id: str, hash_id: str, upload_time: str, failure_reason: str) -> None:
    print('mark_processing_as_failed')
    print(f'failure reason: {failure_reason}')
    update_rds({
        'user_id': user_id,
        'hash_id': hash_id,
        'upload_time': upload_time,
        'failure_reason': failure_reason
    }, os.environ[PROCESSING_FAILED_EVENT_ENV_NAME])

    send_sns(user_id, hash_id, os.environ[PROCESSING_FAILED_EVENT_ENV_NAME])


def mark_video_as_a_draft(
    user_id: str,
    hash_id: str,
    video_type: str,
    size_in_bytes: int,
    duration_seconds: int,
    thumbnail_url: str,
    storage_thumbnail_key: str,
    storage_object_key: str,
    upload_time: str
) -> None:
    print('mark_video_as_a_draft')
    update_rds({
        'user_id': user_id,
        'hash_id': hash_id,
        'video_type': video_type,
        'size_in_bytes': size_in_bytes,
        'duration_seconds': duration_seconds,
        'thumbnail_url': thumbnail_url,
        'storage_thumbnail_key': storage_thumbnail_key,
        'storage_object_key': storage_object_key,
        'upload_time': upload_time
    }, os.environ[PROCESSED_VIDEO_MOVED_TO_DRAFTS_EVENT_ENV_NAME])

    send_sns(user_id, hash_id,
             os.environ[PROCESSED_VIDEO_MOVED_TO_DRAFTS_EVENT_ENV_NAME])


def lambda_handler(event, context):
    """
    Triggers on a new video upload to S3
    This function orchestrate the processing logic and responsible on:
    - Validation
    - Processing and Thumbnail extraction
    - Update relevant services on the processing state (i.e: failures, stage progress)
      - i.e: SNS, Another lambdas for thumbnail resize, RDS update, etc..
    - Delete asset from S3 on failure

    * On unhandled failures such as timeout a garbage-collectore service should delete assets and update DB
    """

    assert_necessery_env_are_here()

    # request constants
    MAX_FILE_SIZE_IN_BYTES: int = int(
        float(os.environ[S3_MAX_VIDEO_SIZE_IN_BYTES_ENV_NAME]))
    # The number of seconds that the Signed URL is valid
    SIGNED_URL_EXPIRATION: int = 60 * 10
    # server time
    upload_time: str = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    # extract key identifier as var
    bucket = event['Records'][0]['s3']['bucket']['name']
    current_file_key = event['Records'][0]['s3']['object']['key']

    # validates object key format is as supported (and not a directory for example)
    if current_file_key.split('/')[0] != os.environ[UPLOADED_VIDEOS_PREFIX_ENV_NAME]:
        print(
            f'An invalid s3 prefix, for key: {current_file_key}, processing has been stopped before being able to get hash_id due to infrastructure failure')
        # avoid retries
        return {'statusCode': 200, 'body': 'invalid prefix, no need to retry'}

    # validate object key exists and accessable
    try:
        obj: Dict = s3Client.get_object(
            Bucket=bucket,
            Key=current_file_key
        )
    except Exception as e:
        # internal error
        print(
            f'An exception occurred, internal error on get_object, processing has been stopped before being able to get hash_id, infrastructure failure, bucket={bucket}, key={current_file_key}')
        print(e)
        raise e

    # validate object key format by levels count
    # the uploaded-videos lambda triggered by specific prefix and the format should be known 
    key_levels = current_file_key.split('/')
    if len(key_levels) < 3:
        # internal error
        print(
            f'An exception occurred, infrastructure failure, key is not in valid format: {current_file_key}')
        print(e)
        raise e

    # extract user & video identifiers via object key
    file_name: str = key_levels[-1]
    user_id: str = key_levels[-2]
    hash_id: str = file_name.split('.')[0]
    if hash_id is None or len(hash_id) < 1:
        # internal error
        e = Exception(
            f'An exception occurred, infrastructure failure, key is not in valid format: {current_file_key}')
        print(e)
        raise e

    # mark as processing
    try:
        # mark as processing
        mark_upload_as_unprocessed(
            user_id=user_id, hash_id=hash_id, upload_time=upload_time)
    except Exception as e:
        print('An exception occurred, failed to mark as unprocessed')
        print(e)
        delete_object(bucket, current_file_key),
        mark_processing_as_failed(
            user_id=user_id, hash_id=hash_id, upload_time=upload_time, failure_reason=os.environ[INTERNAL_ERROR_ENV_NAME])
        return {'statusCode': 500}

    # move to videos S3 prefix
    try:
        copy_source = {'Bucket': bucket, 'Key': current_file_key}
        unprocessed_key_levels = key_levels.copy()
        unprocessed_key_levels[0] = os.environ[UNPROCESSED_VIDEOS_PREFIX_ENV_NAME]
        unprocessed_file_key = '/'.join(unprocessed_key_levels)
        s3Client.copy(copy_source, bucket, unprocessed_file_key)
        delete_object(bucket, current_file_key)  # not needed anymore
        current_file_key = unprocessed_file_key
    except Exception as e:
        print(
            'An exception occurred, failed to move uploaded file to unprocessed prefix')
        print(e)
        delete_object(bucket, current_file_key),
        mark_processing_as_failed(
            user_id=user_id, hash_id=hash_id, upload_time=upload_time, failure_reason=os.environ[CORRUPTED_ENV_NAME])
        return {'statusCode': 500}

    # extract object meta data    
    try:
        meta = get_object_meta(obj)
        print(meta)
    except Exception as e:
        print('An exception occurred, failed to get meta')
        print(e)
        delete_object(bucket, current_file_key),
        mark_processing_as_failed(
            user_id=user_id, hash_id=hash_id, upload_time=upload_time, failure_reason=os.environ[CORRUPTED_ENV_NAME])
        return {'statusCode': 400}

    # validate file size
    if MAX_FILE_SIZE_IN_BYTES < meta['size_in_bytes']:
        delete_object(bucket, current_file_key)
        mark_processing_as_failed(user_id=user_id, hash_id=hash_id, upload_time=upload_time,
                                  failure_reason=os.environ[MAX_FILE_SIZE_EXCEEDED_ENV_NAME])
        return {'statusCode': 400}

    # validate video type
    if not is_supported_video_type(meta['type']):
        print('not a video')
        # not a video, delete file!
        delete_object(bucket, current_file_key)
        mark_processing_as_failed(user_id=user_id, hash_id=hash_id, upload_time=upload_time,
                                  failure_reason=os.environ[UNSUPPORTED_FILE_FORMAT_ENV_NAME])
    else:
        print('a video')
        # video
        try:
            # Generate a signed URL for the uploaded asset
            s3_source_signed_url: str = get_signed_url(
                SIGNED_URL_EXPIRATION, bucket, current_file_key)
        except Exception as e:
            delete_object(bucket, current_file_key)
            mark_processing_as_failed(user_id=user_id, hash_id=hash_id, upload_time=upload_time,
                                      failure_reason=os.environ[INTERNAL_ERROR_ENV_NAME])
            print('An exception occurred, internal error')
            print(e)
            raise e

        # get video duration    
        try:
            duration_seconds: float = get_video_duration_seconds(
                s3_source_signed_url)

            thumbnail_key = f'{os.environ[THUMBNAILS_PREFIX_ENV_NAME]}/{user_id}/{hash_id}.png'
            upload_frame_as_thumbnail(
                s3_source_signed_url, duration_seconds, bucket, thumbnail_key)

            resize_thumbnail(bucket, thumbnail_key, THUMBNAIL_SIZE)
        except Exception as e:
            print('Video processing exception occurred')
            print(e)
            delete_object(bucket, current_file_key)
            delete_object(bucket, thumbnail_key)
            mark_processing_as_failed(
                user_id=user_id, hash_id=hash_id, upload_time=upload_time, failure_reason=os.environ[CORRUPTED_ENV_NAME])
            raise e

    # processing is done, mark as ready
    try:
        # move to videos S3 prefix
        copy_source = {'Bucket': bucket, 'Key': current_file_key}
        videos_key_levels = key_levels.copy()
        videos_key_levels[0] = os.environ[VIDEOS_PREFIX_ENV_NAME]
        # restrict video file to have the appropriate extension
        extension = get_extension_by_content_type(meta['type'])
        videos_key_levels[-1] = f'{videos_key_levels[-1].split(".")[0]}.{extension}'
        video_key = '/'.join(videos_key_levels)
        s3Client.copy(copy_source, bucket, video_key)
        delete_object(bucket, current_file_key)  # not needed anymore
        current_file_key = video_key

        mark_video_as_a_draft(  # processed successfully
            user_id=user_id,
            hash_id=hash_id,
            video_type=meta['type'],
            size_in_bytes=meta['size_in_bytes'],
            duration_seconds=duration_seconds,
            thumbnail_url=f'https://{bucket}.s3.amazonaws.com/{thumbnail_key}',
            storage_thumbnail_key=thumbnail_key,
            storage_object_key=current_file_key,
            upload_time=upload_time
        )
    except Exception as e:
        print('Exception, failed to move video into completed prefix')
        print(e)
        delete_object(bucket, current_file_key)
        delete_object(bucket, thumbnail_key)
        mark_processing_as_failed(user_id=user_id, hash_id=hash_id, upload_time=upload_time,
                                  failure_reason=os.environ[INTERNAL_ERROR_ENV_NAME])
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete successfully')
    }
