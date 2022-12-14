import datetime
from common.utils.calc_server_time import calc_server_time
from mock import patch


def test_calc_server_time():
    """Tests that the function returns the current UTC timestamp"""

    mock_datetime_result = datetime.datetime(
        2020, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc
    )

    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = mock_datetime_result
        assert calc_server_time() == '2020-01-01T00:00:00+00:00'
