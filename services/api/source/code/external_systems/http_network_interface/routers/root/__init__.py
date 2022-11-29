from fastapi import APIRouter
import common.environment as environment
from .health_check import health_check
from starlette.responses import RedirectResponse

router = APIRouter(tags=['Root'])

router.add_api_route(environment.HEALTH_CHECK_PATH, health_check)

@router.api_route('/')
async def redirect_to_health_check() -> None:
    return RedirectResponse(url=environment.HEALTH_CHECK_PATH)
