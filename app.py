from fastapi import FastAPI
from pydantic import BaseModel

from worker import send

# This is the producer / client

app = FastAPI()

# pydantic schema
class SendMessage(BaseModel):
    msg: str


@app.post('/send')
def enqueue_send(req: SendMessage):
    # Use celery delay method in order to enqueue the task with the given parameters
    send.delay(req.msg)
    return {"status": "success"}