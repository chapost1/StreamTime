from use_cases.validation_utils.concrete import is_anonymous_user
from common.constants import ANONYMOUS_USER
from uuid import uuid4


def test_should_return_true_on_anonymous_user():
    assert is_anonymous_user(user_id=ANONYMOUS_USER) == True


def test_should_return_false_on_valid_user_id():
    assert is_anonymous_user(user_id=uuid4()) == False


def test_should_return_false_on_None():
    assert is_anonymous_user(user_id=None) == False
