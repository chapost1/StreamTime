import datetime


def calc_server_time() -> datetime.datetime:
    """Returns UTC timestamp of the execution moment"""

    return datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc
    ).isoformat()
