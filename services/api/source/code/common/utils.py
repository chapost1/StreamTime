import datetime

def calc_server_time() -> datetime.datetime:
    return datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

def nl() -> str:
    return '\n'
