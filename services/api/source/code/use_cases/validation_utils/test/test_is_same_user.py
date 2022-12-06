from use_cases.validation_utils.concrete import is_same_user
from common.constants import ANONYMOUS_USER

fixtures = {
    'uuid4_1': 'fe51b79e-63d8-43d6-97b8-b369890868ee',
    'uuid4_2': '603dec13-e08c-49a8-88c7-dedb23193107'
}


def test_should_return_true_on_anonymous_user_with_anonymous_user():
    assert is_same_user(id_a=ANONYMOUS_USER, id_b=ANONYMOUS_USER) == True


def test_should_return_false_on_anonymous_user_with_any_other_user():
    assert is_same_user(id_a=fixtures['uuid4_1'], id_b=ANONYMOUS_USER) == False


def test_should_return_false_on_different_users():
    assert is_same_user(id_a=fixtures['uuid4_1'], id_b=fixtures['uuid4_2']) == False


def test_should_return_true_on_same_user():
    assert is_same_user(id_a=fixtures['uuid4_1'], id_b=fixtures['uuid4_1']) == True
