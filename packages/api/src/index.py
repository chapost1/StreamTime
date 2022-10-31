from .environment import environment
from fastapi import FastAPI


app = FastAPI()


@app.get(environment.HEALTH_CHECK_PATH)
def root():
    return {"message": "Hello World"}
