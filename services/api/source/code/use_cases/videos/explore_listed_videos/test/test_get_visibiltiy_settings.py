from uuid import uuid4
from use_cases.videos.explore_listed_videos.get_visibility_settings import get_visibility_settings

truthy_func = lambda *args, **kwargs: True
falsy_func = lambda *args, **kwargs: False

def test_returns_user_id_to_ignore_as_authenticated_user_if_include_my_is_false():
    user_id = uuid4()
    user_id_to_ignore, _ = get_visibility_settings(
        is_anonymous_user_fn=truthy_func,
        authenticated_user_id=user_id,
        include_my=False
    )

    assert user_id_to_ignore == user_id


def test_returns_user_id_to_ignore_as_none_if_include_my_is_true():
    user_id = uuid4()
    user_id_to_ignore, _ = get_visibility_settings(
        is_anonymous_user_fn=truthy_func,
        authenticated_user_id=user_id,
        include_my=True
    )

    assert user_id_to_ignore is None


def test_returns_authenticated_user_to_allow_privates_as_authenticated_user_if_not_anonymous_user():
    user_id = uuid4()
    _, authenticated_user_to_allow_privates = get_visibility_settings(
        is_anonymous_user_fn=falsy_func,
        authenticated_user_id=user_id,
        include_my=True
    )

    assert authenticated_user_to_allow_privates == user_id


def test_returns_authenticated_user_to_allow_privates_as_none_if_anonymous_user():
    user_id = uuid4()
    _, authenticated_user_to_allow_privates = get_visibility_settings(
        is_anonymous_user_fn=truthy_func,
        authenticated_user_id=user_id,
        include_my=True
    )

    assert authenticated_user_to_allow_privates is None
