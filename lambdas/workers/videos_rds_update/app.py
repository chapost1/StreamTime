from typing import Tuple, Any, List
import psycopg2
from psycopg2.extensions import connection as pg_connection
import json
import os

##########################
######## ENV VARS ########
##########################
# PROCESSING EVENTS
PROCESSING_HAS_BEEN_STARTED_EVENT_ENV_NAME = 'new_video_events_processing_has_been_started'
PROCESSING_FAILED_EVENT_ENV_NAME = 'new_video_events_processing_failure'
PROCESSED_VIDEO_MOVED_TO_DRAFTS_EVENT_ENV_NAME = 'new_video_events_moved_to_drafts'
# RDS Connection
RDS_HOST_ENV_NAME = 'rds_host'
RDS_PORT_ENV_NAME = 'rds_port'
RDS_USER_ENV_NAME = 'rds_user'
RDS_PASSWORD_ENV_NAME = 'rds_password'
RDS_DB_NAME_ENV_NAME = 'rds_db_name'
# DB tables names
UNPROCESSED_VIDEOS_TABLE_ENV_NAME = 'rds_table_uprocessed_videos'
VIDEOS_TABLE_ENV_NAME = 'rds_table_videos'

# it is good practice in lambda to open connection outside of handler and never close it,
# according to: https://aws.amazon.com/premiumsupport/knowledge-center/lambda-rds-connection-timeouts/
rds_connection: pg_connection = psycopg2.connect(
    host=os.environ[RDS_HOST_ENV_NAME],
    port=os.environ[RDS_PORT_ENV_NAME],
    user=os.environ[RDS_USER_ENV_NAME],
    password=os.environ[RDS_PASSWORD_ENV_NAME],
    database=os.environ[RDS_DB_NAME_ENV_NAME],
    connect_timeout=5
)


def assert_necessery_env_are_here() -> None:
    for env in [UNPROCESSED_VIDEOS_TABLE_ENV_NAME, VIDEOS_TABLE_ENV_NAME,
                PROCESSING_HAS_BEEN_STARTED_EVENT_ENV_NAME, PROCESSING_FAILED_EVENT_ENV_NAME,
                PROCESSED_VIDEO_MOVED_TO_DRAFTS_EVENT_ENV_NAME
                ]:
        if os.environ.get(env, None) is None:
            raise RuntimeError(f'missing env varialbe: {env}')


def sql_executor(transaction_steps: List[Tuple[str, Tuple[Any]]]) -> None:
    cursor = rds_connection.cursor()
    for sql, params in transaction_steps:
        try:
            cursor.execute(sql, params)
        except:
            cursor.execute("rollback")
            cursor.execute(sql, params)
    rds_connection.commit()


def mark_upload_as_unprocessed(user_id: str, hash_id: str, upload_time: str) -> None:
    print('mark_upload_as_unprocessed')
    sql = f'INSERT INTO {os.environ[UNPROCESSED_VIDEOS_TABLE_ENV_NAME]} (user_id, hash_id, upload_time) VALUES(%s, %s, %s)'
    params = (user_id, hash_id, upload_time)
    sql_executor(
        transaction_steps=[(sql, params)]
    )


def mark_processing_as_failed(user_id: str, hash_id: str, upload_time: str, failure_reason: str) -> None:
    print('mark_processing_as_failed')
    print(f'failure reason: {failure_reason}')
    sql = \
        f"""INSERT INTO {os.environ[UNPROCESSED_VIDEOS_TABLE_ENV_NAME]} (user_id, hash_id, upload_time, failure_reason)
        VALUES(%s, %s, %s, %s)
        ON CONFLICT (user_id, hash_id)
        DO
        UPDATE SET failure_reason = %s;"""
    params = (user_id, hash_id, upload_time, failure_reason, failure_reason)
    sql_executor(
        transaction_steps=[(sql, params)]
    )


def mark_video_as_a_draft(
    user_id: str,
    hash_id: str,
    video_type: str,
    size_in_bytes: int,
    duration_seconds: int,
    thumbnail_url: str,
    upload_time: str
) -> None:
    print('mark_video_as_a_draft')
    # delete unprocessed marker
    delete_unprocessed_entry_sql = \
        f"""DELETE FROM {os.environ[UNPROCESSED_VIDEOS_TABLE_ENV_NAME]} WHERE user_id = %s AND hash_id = %s AND upload_time = %s;"""
    delete_unprocessed_entry_params = (user_id, hash_id, upload_time)
    # insert into drafts
    insert_sql = \
        f"""INSERT INTO {os.environ[VIDEOS_TABLE_ENV_NAME]} (user_id, hash_id, upload_time, size_in_bytes, duration_seconds, video_type, thumbnail_url, is_listed)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_params = (user_id, hash_id, upload_time, size_in_bytes,
                     duration_seconds, video_type, thumbnail_url, False)
    sql_executor(
        transaction_steps=[
            (delete_unprocessed_entry_sql, delete_unprocessed_entry_params),
            (insert_sql, insert_params)
        ]
    )


def lambda_handler(event, context):
    assert_necessery_env_are_here()
    try:
        trigger = event['trigger']
        record = event['record']
        if trigger == os.environ[PROCESSING_HAS_BEEN_STARTED_EVENT_ENV_NAME]:
            mark_upload_as_unprocessed(
                user_id=record['user_id'], hash_id=record['hash_id'], upload_time=record['upload_time'])
        elif trigger == os.environ[PROCESSING_FAILED_EVENT_ENV_NAME]:
            mark_processing_as_failed(
                user_id=record['user_id'], hash_id=record['hash_id'], upload_time=record['upload_time'], failure_reason=record['failure_reason'])
        elif trigger == os.environ[PROCESSED_VIDEO_MOVED_TO_DRAFTS_EVENT_ENV_NAME]:
            mark_video_as_a_draft(
                user_id=record['user_id'],
                hash_id=record['hash_id'],
                video_type=record['video_type'],
                size_in_bytes=record['size_in_bytes'],
                duration_seconds=record['duration_seconds'],
                thumbnail_url=record['thumbnail_url'],
                upload_time=record['upload_time']
            )
        else:
            print('unsupported event')
            print(event)
            return {
                'statusCode': 404,
                'body': json.dumps('Unsupported event')
            }
    except Exception as e:
        print('unexpected exception')
        print(e)
        raise e

    return {
        'statusCode': 204,
        'body': json.dumps('Processing complete successfully')
    }
