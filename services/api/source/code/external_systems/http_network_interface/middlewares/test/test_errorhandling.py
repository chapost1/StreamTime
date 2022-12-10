from fastapi import status, Response, Request
from fastapi.responses import JSONResponse
import common.app_errors as app_errors
import pytest
from unittest.mock import AsyncMock
from external_systems.http_network_interface.middlewares.errorhandling import (
    app_errors_handler,
    http_error
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="error,http_status_code",
    argvalues=[
        (app_errors.NotFoundError, status.HTTP_404_NOT_FOUND),
        (app_errors.InputError, status.HTTP_400_BAD_REQUEST),
        (app_errors.UnauthorizedError, status.HTTP_401_UNAUTHORIZED),
        (app_errors.AccessDeniedError, status.HTTP_403_FORBIDDEN),
        (app_errors.TooEarlyError, status.HTTP_425_TOO_EARLY)
    ]
)
async def test_md_app_errors_to_http_code_mappings(
    error: app_errors.AppError,
    http_status_code: int
):
    response: Response = await app_errors_handler(
        request=None,
        call_next=AsyncMock(side_effect=error)
    )

    assert response.status_code == http_status_code


@pytest.mark.asyncio
async def test_md_some_unexpected_error_is_being_propagated():
    try:
        await app_errors_handler(
            request=None,
            call_next=AsyncMock(side_effect=RuntimeError)
        )
        # should not reach
        assert 1 == 2
    except RuntimeError:
        assert 1 == 1


def test_http_error_returns_JSONResponse_if_error_has_details():
    response = http_error(details={}, status_code=status.HTTP_418_IM_A_TEAPOT)
    assert isinstance(response, JSONResponse)


def test_http_error_returns_Response_if_error_has_no_details():
    response = http_error(details=None, status_code=status.HTTP_418_IM_A_TEAPOT)
    assert not isinstance(response, JSONResponse) # subclass of response
    assert isinstance(response, Response)


@pytest.mark.asyncio
async def test_md_returns_JSONResponse_if_error_has_details():
    async def mock(request: Request):
        raise app_errors.InputError(details={})

    response: Response = await app_errors_handler(
        request=None,
        call_next=mock
    )
    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_md_returns_Response_if_error_has_no_details():
    response: Response = await app_errors_handler(
        request=None,
        call_next=AsyncMock(side_effect=app_errors.InputError)
    )
    assert not isinstance(response, JSONResponse) # subclass of response
    assert isinstance(response, Response)
