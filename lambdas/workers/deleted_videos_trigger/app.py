import gzip
import json
import base64


def decode_gzip(event):
    """
    Decodes the event data from gzip
    """
    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)
    return payload


def get_statement(log_event):
    """
    Returns the statement from the log event
    """
    log_event_message = log_event['message']
    # removed the timestamp and the log level
    delimeter = 'statement:'
    del_index = log_event_message.index(delimeter)
    statement = log_event_message[del_index + len(delimeter):]
    return statement


def parse_log_event(log_event):
    """
    Parses the log event
    """
    statement = get_statement(log_event)
    return statement


def lambda_handler(event, context):
    """
    Lambda function to process deleted videos events
    Triggered by CloudWatch Events
    Triggers an SQS message to be sent to the deleted_videos_queue
    """

    print('triggering deleted_videos_queue')
    payload = decode_gzip(event)
    log_events = payload['logEvents']
    # merge all the statements into one long statement
    log = [parse_log_event(log_event) for log_event in log_events]
    stmt = ' '.join(log)
    stmt = ' '.join(line.strip() for line in stmt.splitlines())
    print(stmt)

    # parse the statement into a dict
    # sql dml statement into a dict


    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete successfully')
    }

