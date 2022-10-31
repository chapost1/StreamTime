from environment import environment
from rds import test_pg_connection
from fastapi import FastAPI

print('app start')

app = FastAPI()


@app.get(environment.HEALTH_CHECK_PATH)
async def health_check():
    return {"message": "ok"}


@app.get('/db_check')
async def db_check():
    print('before test')
    test_pg_connection()
    print('after test')
    return {"message": "done"}
