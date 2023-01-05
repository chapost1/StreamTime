import common.environment as environment
from shared.models.garbage.garbage import Garbage
from shared.infrastructure.aws_integration import Boto3
from botocore.exceptions import ClientError
from shared.infrastructure.queue.context import Context
from functools import partial
from shared.infrastructure.queue.pipe import (
    garbage_to_message,
    message_to_garbage
)
from typing import Callable, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


class SQS:
    f"""
    SQS as a message queue.
    """

    def __init__(self, context: Context):
        self.context = context


    def __get_client(self):
        return Boto3().session().create_client(
            'sqs',
            region_name=environment.AWS_REGION
        )
    

    async def publish(self, garbage: Garbage) -> bool:
        """Publishes a message to the queue"""

        try:
            message: str = garbage_to_message(garbage=garbage)
            await self.__get_client().send_message(
                QueueUrl=self.context.queue_url,
                MessageBody=message
            )
            return True
        except ClientError as e:
            logger.error(f'Client error during SQS publish op, {e}')
            return False


    async def subscribe(self, on_message: Callable[[Garbage, Callable], None]) -> None:
        """Subscribes to the queue and calls the callback when a message is received"""

        while True:
            try:
                # This loop wont spin really fast as there is
                # essentially a sleep in the receieve_message call
                response = await self.__get_client().receive_message(
                    QueueUrl=self.context.queue_url,
                    # max wait time of 2 seconds, to avoid spinning
                    WaitTimeSeconds=2,
                    # others cannot see the message for 30 seconds
                    VisibilityTimeout=30,
                    # get up to 5 messages at a time
                    # we process them asynchonously
                    # so we can have more throughput
                    MaxNumberOfMessages=5
                )

                # extract the message and call the callback
                if 'Messages' in response:
                    for message in response['Messages']:
                        message_body = message['Body']
                        garbage = message_to_garbage(message=message_body)
                        # call the callback with the garbage and a callback to delete the message
                        asyncio.get_event_loop().create_task(
                            on_message(
                                # garbage=garbage
                                garbage,
                                # done=callback to delete the message (if no error)
                                partial(self.delete_from_queue, message['ReceiptHandle'])
                            )
                        )

            except KeyboardInterrupt:
                # exit the loop
                break
            except ClientError as e:
                # wait 5 seconds before trying again
                await asyncio.sleep(5)
                logger.error(f'Client error during SQS subscribe op, {e}')


    async def delete_from_queue(self, receipt_handle: str, error: Optional[Exception]) -> None:
        """Deletes a message from the queue"""
        if error is not None:
            # if there was an error, do not delete the message
            # so that it can be retried
            logger.error(f'Error during SQS delete op, {error}')
            return
        # delete the message
        await self.__get_client().delete_message(
            QueueUrl=self.context.queue_url,
            ReceiptHandle=receipt_handle
        )