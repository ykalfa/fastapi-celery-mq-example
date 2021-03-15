from celery import Celery
from celery.utils.log import get_task_logger
import time

CELERY_BROKER_URL = 'pyamqp://guest:guest@localhost:5672'
# CELERY_BROKER_URL = 'pyamqp://guest@rabbit//'

# Create the celery app and get the logger
celery_app = Celery('tasks', broker=CELERY_BROKER_URL)
logger = get_task_logger(__name__)

class VendorException(Exception):
    pass

# If your tasks depend on another service, like making a request to an API, then it’s a good idea to use exponential backoff to avoid overwhelming the service with your requests.
# https://docs.celeryproject.org/en/latest/userguide/tasks.html#retrying
@celery_app.task(bind=True, autoretry_for=(VendorException,), retry_kwargs={'max_retries': 3}, retry_backoff=True)
def send(self, msg: str):
    logger.info("1")
    time.sleep(1)
    if msg == "test_vendor_error":
        raise VendorException("testing vendor exception")
    if msg == "test_error":
        raise Exception("testing exception")
    logger.info("2")
    time.sleep(1)
    logger.info("3")
    time.sleep(1)

    logger.info("Sending a message with the content of : %s" % (msg))
    return