from uuid import uuid4
from unittest.mock import Mock
from external_systems.http_network_interface.request_state_utils.auth.auth_state import (
    set_authenticated_user_id,
    get_authenticated_user_id
)


def test_setter_add_authenticated_user_id_in_the_correct_property():
    user_id = uuid4()
    mock_request = Mock()
    mock_request.state.auth_user_id = None

    set_authenticated_user_id(request=mock_request, authenticated_user_id=user_id)
    assert mock_request.state.auth_user_id == user_id


def test_getter_returns_none_when_request_has_no_state_yet():
    mock_request = Mock()
    mock_request.state.auth_user_id = None
    assert get_authenticated_user_id(request=mock_request) is None


def test_getter_returns_correct_user_id():
    user_id = uuid4()
    mock_request = Mock()
    mock_request.state.auth_user_id = None

    set_authenticated_user_id(request=mock_request, authenticated_user_id=user_id)

    assert get_authenticated_user_id(request=mock_request) == user_id
