from fastapi import APIRouter
from .my import router as my_videos_router
from .explore import router as explore_videos_router
from .user import router as user_videos_router
from .upload import router as upload_video_router
from .watch import router as watch_video_router

router = APIRouter(tags=['Videos'])

router.include_router(explore_videos_router, prefix='/explore')

router.include_router(upload_video_router, prefix='/upload')

router.include_router(my_videos_router, prefix='/my')

router.include_router(user_videos_router, prefix='/user')

router.include_router(watch_video_router, prefix='/watch')
