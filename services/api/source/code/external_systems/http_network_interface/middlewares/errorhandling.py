from typing import Callable
from fastapi import Request, status, Response
from fastapi.responses import JSONResponse
import common.app_errors as app_errors


def http_error(details: app_errors.AppError, status_code: status) -> Response:
    """Retuens an HTTP Response based on the relevant structure"""

    if details is not None:
        return JSONResponse(content=details, status_code=status_code)
    else:
        return Response(content=details, status_code=status_code)


async def app_errors_handler(request: Request, call_next: Callable):
    """Catches application level errors and translates them into http errors"""

    try:
        return await call_next(request)
    except app_errors.NotFoundError as e:
        return http_error(details=e.details, status_code=status.HTTP_404_NOT_FOUND)
    except app_errors.InputError as e:
        return http_error(details=e.details, status_code=status.HTTP_400_BAD_REQUEST)
    except app_errors.UnauthorizedError as e:
        return http_error(details=e.details, status_code=status.HTTP_401_UNAUTHORIZED)
    except app_errors.AccessDeniedError as e:
        return http_error(details=e.details, status_code=status.HTTP_403_FORBIDDEN)
    except app_errors.TooEarlyError as e:
        return http_error(details=e.details, status_code=status.HTTP_425_TOO_EARLY)
