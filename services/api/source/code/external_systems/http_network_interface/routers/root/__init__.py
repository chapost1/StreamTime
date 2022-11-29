from fastapi import APIRouter
import common.environment as environment
from .health_check import health_check
router = APIRouter(tags=['Root'])

router.add_api_route(environment.HEALTH_CHECK_PATH, health_check)
