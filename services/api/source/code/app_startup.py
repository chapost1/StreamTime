from data_access.rds import init as init_rds

async def init():
    await init_rds()
