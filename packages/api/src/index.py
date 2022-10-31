import os
from fastapi import FastAPI

app = FastAPI()

print(os.environ)

@app.get("/health_check")
def root():
    return {"message": "Hello World"}
