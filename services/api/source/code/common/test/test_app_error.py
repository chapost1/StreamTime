from common.app_errors import AppError
import json


def test_should_have_default_message_as_empty_string():
    ae = AppError()
    assert f'{ae}' == ''


def test_should_have_message_as_passed():
    message = 'test_message'
    ae = AppError(message=message)
    assert f'{ae}' == message


def test_should_have_default_details_as_None():
    ae = AppError()
    assert ae.details is None


def test_should_contain_details_the_same_as_received_as_an_argument():
    details = {
        'hello': 'world!'
    }
    ae = AppError(details=details)
    assert json.dumps(ae.details) == json.dumps(details)


def test_should_be_an_instance_of_exception():
    assert isinstance(AppError(), Exception) == True


def test_should_be_able_to_raise_with_traceback():
    try:
        raise AppError()
    except AppError as ae:
        assert ae.__traceback__ is not None
