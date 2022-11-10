from fastapi import APIRouter
from .my import router as my_videos_router
from .explore import router as explore_videos_router
from .user import router as user_videos_router

router = APIRouter(tags=["Videos"])

router.include_router(explore_videos_router, prefix='/explore')

router.include_router(my_videos_router, prefix='/my')

router.include_router(user_videos_router, prefix='/user')

# todo implement:

# request upload video premission (will return presigned url) (will require nothing)

# /watch video (return meta and watch presigned url, check if not private or actual user.)
