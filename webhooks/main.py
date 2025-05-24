from contextlib import asynccontextmanager
import os
from typing import Annotated

from fastapi import Body, FastAPI, Request
import argon2

from database import db, Listener, migrate_db
from models import ListenerModel
from verification import VALIDATORS

ph = argon2.PasswordHasher()

PASSPHRASE: str = os.getenv('PASSPHRASE', 'unauthenticated')

@asynccontextmanager
async def lifespan(_: FastAPI):
    db.connect()

    db.create_tables([Listener], safe=True)
    yield
    db.close()


app = FastAPI(lifespan=lifespan)

@app.get('/')
async def root():
    return {"message": "Hello, World!"}


@app.get('/webhooks')
async def get_webhooks():
    webhooks = Listener.select()
    return [webhook.__data__ for webhook in webhooks]


@app.post('/webhooks')
async def create_webhook(listener_data: ListenerModel, passphrase: Annotated[str, Body(...)]):
    if ph.verify(PASSPHRASE, passphrase) is False:
        return {"error": "Invalid passphrase"}, 401

    try:
        os.makedirs('handlers', exist_ok=True)

        with open(f'handlers/{listener_data.name}.py', 'w') as f:
            f.write(listener_data.handler)

        listener = Listener.create(
            name=listener_data.name,
            verification_type=listener_data.verification_type,
            other_data=listener_data.other_data or ""
        )
        return {"message": "Webhook created successfully", "id": listener.id}
    except Exception as e:
        return {"error": str(e)}, 400


@app.post('/listeners/{webhook}')
async def handle_webhook(webhook: str, request: Request):
    listener = Listener.get_or_none(Listener.name == webhook)
    if not listener:
        return {"error": "Webhook not found"}, 404

    if listener.verification_type < 0 or listener.verification_type >= len(VALIDATORS):
        return {"error": "Invalid verification type"}, 400

    verification_function = VALIDATORS[listener.verification_type]
    _, verified = await verification_function(listener.other_data, request)

    if not verified:
        return {"error": "Verification failed"}, 400

    module = __import__(f'handlers.{listener.name}', fromlist=['handler'])
    handler_function = getattr(module, 'handler', None)

    if not handler_function:
        return {"error": "Handler function not found"}, 500

    response_code = await handler_function(request)

    return {"message": "Webhook handled successfully"}, response_code

