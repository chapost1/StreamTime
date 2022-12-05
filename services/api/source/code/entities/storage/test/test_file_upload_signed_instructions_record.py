from entities.storage.file_upload_signed_instructions_record import FileUploadSignedInstructions
import pytest
from pydantic import ValidationError

some_valid_url = 'https://foo.bar.com'


def test_should_require_url_argument():
    with pytest.raises(expected_exception=ValidationError):
        FileUploadSignedInstructions(signatures={})


def test_should_require_signatures_argument():
    with pytest.raises(expected_exception=ValidationError):
        FileUploadSignedInstructions(url=some_valid_url)


def test_should_fail_on_invalid_url():
    with pytest.raises(expected_exception=ValidationError):
        FileUploadSignedInstructions(watchable_url='invalid', signatures={})


def test_should_not_fail_on_valid_arguments():
    with pytest.raises(expected_exception=ValidationError):
        FileUploadSignedInstructions(watchable_url=some_valid_url, signatures={})
