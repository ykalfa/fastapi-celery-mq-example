from celery import Celery
from celery.utils.log import get_task_logger
from celery.exceptions import MaxRetriesExceededError # New import
import time
import random # New import

CELERY_BROKER_URL = 'pyamqp://guest@rabbit//'

# Create the celery app and get the logger
celery_app = Celery('tasks', broker=CELERY_BROKER_URL)
logger = get_task_logger(__name__)

class VendorException(Exception):
    pass

# The 'send' task with improved retry logic
# We'll change autoretry_for to handle any Exception
@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3}, retry_backoff=True)
def send(self, msg: str):
    logger.info(f"Attempt {self.request.retries + 1} for task {self.request.id}") # New log message
    
    try:
        # Simulate a temporary failure with a 70% chance
        # This only happens if there are still retries available
        if random.random() < 0.7 and self.request.retries < self.max_retries:
            logger.warning(f"Simulating temporary failure for task {self.request.id}")
            raise ValueError("Simulating a temporary failure.")

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
        return f"Message '{msg}' sent successfully after {self.request.retries} retries." # Changed success message

    except (ValueError, VendorException, Exception) as exc: # Catch ValueError and general Exception
        if isinstance(exc, MaxRetriesExceededError):
            logger.error(f"Task {self.request.id} failed permanently after max retries: {exc}")
            raise # Re-raise the final exception
        
        # Celery's autoretry_for handles the retry, so we just log and re-raise for Celery to catch
        logger.warning(f"Task {self.request.id} failed with {type(exc).__name__}. Retrying...")
        raise self.retry(exc=exc) # Important to re-raise the exception for Celery to handle the retry
