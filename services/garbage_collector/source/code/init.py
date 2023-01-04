from shared.infrastructure.rds import handle_connection as init_rds_connection
from shared.infrastructure.aws_integration.boto3 import init as init_boto3
import asyncio
import logging


async def init():
    """
    Initialize the garbage collector service.
    Initialize the app dependencies.
    """
    logging.info('Initializing garbage collector service')

    tasks = [
        init_boto3(),
        init_rds_connection()
    ]

    await asyncio.gather(*tasks)
