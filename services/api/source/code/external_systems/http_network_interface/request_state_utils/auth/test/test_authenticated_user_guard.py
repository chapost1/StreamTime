import common.constants as constants
from fastapi import HTTPException
from external_systems.http_network_interface.request_state_utils.auth.auth_guards import authenticated_user
from uuid import uuid4
import common.constants as constants
from mock import patch
import pytest
from asyncmock import AsyncMock

user_id = uuid4()


@pytest.mark.asyncio
@patch(
    'external_systems.http_network_interface.request_state_utils.auth.auth_guards.any_user',
    AsyncMock(return_value=constants.ANONYMOUS_USER)
)
async def test_raise_http_exception_if_any_user_returns_anonymous_user():
    try:
        await authenticated_user(None)
        # should not work
        assert 1 == 2
    except HTTPException:
        assert 1 == 1


@pytest.mark.asyncio
@patch(
    'external_systems.http_network_interface.request_state_utils.auth.auth_guards.any_user',
    AsyncMock(return_value=user_id)
)
async def test_returns_user_id_if_valid():
    result = await authenticated_user(None)
    assert result == user_id
