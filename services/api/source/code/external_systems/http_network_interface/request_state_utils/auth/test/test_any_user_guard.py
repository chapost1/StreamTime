import common.constants as constants
from uuid import uuid4
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import any_user
from mock import patch
import pytest

user_id = uuid4()

def raiseKeyError(*args, **kwargs):
    raise KeyError()

@pytest.mark.asyncio
@patch(
    'external_systems.http_network_interface.request_state_utils.auth.auth_state.get_authenticated_user_id',
    raiseKeyError
)
async def test_returns_anonymous_user_mark_when_key_error_has_been_raised():
    assert (await any_user(request=None)) == constants.ANONYMOUS_USER


@pytest.mark.asyncio
@patch(
    'external_systems.http_network_interface.request_state_utils.auth.auth_state.get_authenticated_user_id',
    lambda request: user_id
)
async def test_returns_exact_user_id_when_exists():
    assert (await any_user(request=None)) == user_id
