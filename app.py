from fastapi import FastAPI
from pydantic import BaseModel

from worker import send

# This is the producer / client

# Create the FastAPI app
app = FastAPI()

# Use pydantic to keep track of the input request payload
class SendMessage(BaseModel):
    msg: str


@app.post('/send')
def enqueue_send(req: SendMessage):
    # Use celery delay method in order to enqueue the task with the given parameters
    send.delay(req.msg)
    return {"status": "success"}