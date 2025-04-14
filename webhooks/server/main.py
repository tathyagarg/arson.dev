import os
from typing import Annotated

from fastapi import FastAPI, Header, Body, Response, status
from contextlib import asynccontextmanager

import psycopg2

def connect():
    conn = psycopg2.connect(
        os.getenv("DATABASE_URL"),
    )
    return conn

@asynccontextmanager
async def lifespan(_: FastAPI):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS listeners (
            listener_id TEXT PRIMARY KEY,
            secret TEXT NOT NULL,
            type TEXT CHECK (type IN ('discord', 'slack', 'email', 'webhook')),
            url TEXT NOT NULL,
            active BOOLEAN NOT NULL DEFAULT TRUE
        );""")

        cur.execute("""CREATE TABLE IF NOT EXISTS discord_events (
            event_id TEXT NOT NULL,
            listener_id TEXT NOT NULL,
            payload_url TEXT NOT NULL,
            response_template TEXT NOT NULL,
            PRIMARY KEY (event_id, listener_id)
        );""")

        conn.commit()

    yield

app = FastAPI(lifespan=lifespan)

@app.post("/listeners/{listener_id}")
async def receive_update(
    response: Response,
    listener_id: str,
    x_hub_signature_256: Annotated[str, Header()],
    user_agent: Annotated[str, Header()],
    payload: Annotated[dict, Body(...)],
):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute("SELECT secret, type FROM listeners WHERE listener_id = %s", (listener_id,))
        row = cur.fetchone()

        print(row)


@app.post('/create')
async def create_listener(
    response: Response,
    listener_id: Annotated[str, Body(...)],
    secret: Annotated[str, Body(...)],
    type: Annotated[str, Body(...)],
    url: Annotated[str, Body(...)],
    payload_data: Annotated[dict, Body(...)],
):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute("INSERT INTO listeners (listener_id, secret, type, url) VALUES (%s, %s, %s, %s)",
                    (listener_id, secret, type, url))
        conn.commit()

        response.status_code = status.HTTP_201_CREATED
        return {"message": "Listener created successfully"}


