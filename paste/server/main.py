import os
from typing import Annotated
import uuid

from fastapi.responses import FileResponse
import redis
from fastapi import Body, FastAPI, Response
from fastapi.staticfiles import StaticFiles

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

EXPIRY = 60 * 60 * 4
INDEX = 'static/html/index.html'
PASTE = 'static/html/paste.html'
NOT_FOUND = 'static/html/404.html'
TEMPLATE = 'static/html/template.html'

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get('/')
def root():
    return FileResponse(INDEX)


@app.get('/paste')
def paste():
    return FileResponse(PASTE)

@app.get('/paste/{key}')
def get_paste(key: str, response: Response):
    # return html
    result = r.hgetall(key)
    if not result:
        response.status_code = 404
        return FileResponse(NOT_FOUND)

    return FileResponse(open(TEMPLATE).read().format(data=result['data'], language=result['language']))


api = FastAPI()

@api.post('/post')
def post_data(data: Annotated[str, Body(...)], language: Annotated[str, Body(...)]):
    key = str(uuid.uuid4())

    r.hset(key, mapping={'data': data, 'language': language})
    r.expire(key, EXPIRY)

    return {"key": key}


app.mount("/api", api)
app.mount("/static", StaticFiles(directory="static"), name="static")
