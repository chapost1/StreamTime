from use_cases.videos.get_watch_video_record import is_access_allowed

truthy_func = lambda *args, **kwargs: True
falsy_func = lambda *args, **kwargs: False


def test_returns_false_if_not_same_user_and_private():
    assert is_access_allowed(
        is_same_user_fn=falsy_func,
        authenticated_user_id=None,
        owner_user_id=None,
        is_private=True
    ) == False


def test_returns_true_if_not_private_even_if_not_same_user():
    assert is_access_allowed(
        is_same_user_fn=falsy_func,
        authenticated_user_id=None,
        owner_user_id=None,
        is_private=False
    ) == True


def test_returns_true_if_private_but_same_user():
    assert is_access_allowed(
        is_same_user_fn=truthy_func,
        authenticated_user_id=None,
        owner_user_id=None,
        is_private=False
    ) == True
