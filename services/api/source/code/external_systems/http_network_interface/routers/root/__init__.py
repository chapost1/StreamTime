from fastapi import APIRouter
from environment import environment
from .health_check import health_check
router = APIRouter(tags=['Root'])

router.add_api_route(environment.HEALTH_CHECK_PATH, health_check)
