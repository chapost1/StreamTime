from environment import constants
from typing import Dict
from fastapi import APIRouter, Request, HTTPException, status

router = APIRouter()

# upload a video, cosider, maybe return a dataclass...
@router.get("/", response_model=Dict)
async def get_upload_video_url(request: Request) -> Dict:
    authenticated_user_id: str = request.state.auth_user_id
    if authenticated_user_id.__eq__(constants.ANONYMOUS_USER):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    """todo: implement""" # create hash_id and presigned url on s3 (needs the bucket name)
