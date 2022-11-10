from environment import environment
import time
from typing import Callable
from fastapi import FastAPI, Request
from routers import routeList
from services import init as init_services
print('app start')

app = FastAPI()

@app.on_event('startup')
async def init():
    await init_services()

@app.middleware('http')
async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response

@app.middleware('http')# todo: replace with actual authentication mechanism
async def inject_temporary_dummy_username(request: Request, call_next: Callable):
    request.state.auth_user_id = 'ae6d14eb-d222-4967-98d9-60a7cc2d7891'
    return await call_next(request)

@app.get(environment.HEALTH_CHECK_PATH)
async def health_check():
    return {"message": "ok"}
    
app.include_router(routeList.videos_router, prefix="/video")
