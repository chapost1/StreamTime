from uuid import uuid4, UUID

class State:
    _auth_user_id: UUID

    def __init__(self) -> None:
        self._auth_user_id = None

    @property
    def auth_user_id(self) -> UUID:
        return self._auth_user_id
    
    @auth_user_id.setter
    def auth_user_id(self, auth_user_id: UUID) -> None:
        self._auth_user_id = auth_user_id


class HasState:
    state: State

    def __init__(self) -> None:
        self.state = State()


from external_systems.http_network_interface.request_state_utils.auth.auth_state import (
    set_authenticated_user_id,
    get_authenticated_user_id
)


def test_setter_add_authenticated_user_id_in_the_correct_property():
    user_id = uuid4()
    request = HasState()
    set_authenticated_user_id(request=request, authenticated_user_id=user_id)
    assert request.state.auth_user_id == user_id


def test_getter_returns_none_when_request_has_no_state_yet():
    assert get_authenticated_user_id(request=HasState()) is None


def test_getter_returns_correct_user_id():
    user_id = uuid4()
    request = HasState()
    set_authenticated_user_id(request=request, authenticated_user_id=user_id)
    assert get_authenticated_user_id(request=request) == user_id
