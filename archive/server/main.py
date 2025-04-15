from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import dotenv

from pathlib import Path
import json
from enum import Enum
import os
import time
import logging

dotenv.load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
)

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, base: str) -> None:
        super().__init__(app)
        self.base = base

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        if 400 <= response.status_code < 500:
            logging.error(f"{self.base} {request.method} {request.url}: {response.status_code} - {duration:.4f}s")
        elif 500 <= response.status_code < 600:
            logging.critical(f"{self.base} {request.method} {request.url}: {response.status_code} - {duration:.4f}s\nRequest Data: {vars(request)}\nResponse Data: {vars(response)}")
        else:
            logging.info(f"{self.base} {request.method} {request.url}: {response.status_code} - {duration:.4f}s")

        return response

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

api = FastAPI()

app.add_middleware(LoggingMiddleware, base="app")
api.add_middleware(LoggingMiddleware, base="api")

class ServerStatus(int, Enum):
    OK = status.HTTP_200_OK 
    MAINTENANCE = status.HTTP_503_SERVICE_UNAVAILABLE

STATUS = ServerStatus.OK


@app.get("/")
async def root():
    return FileResponse("static/html/index.html")


@app.get("/sites")
async def sites():
    return FileResponse("static/sites/index.html")


@app.get("/sites/{site}/{subpath:path}")
async def site(site: str, subpath: str):
    # if subpath is a file, return it
    if "." in subpath:
        return FileResponse(f"static/sites/{site}/{subpath}")

    return FileResponse(f"static/sites/{site}/index.html")


@api.get("/sites")
async def get_sites():
    result = []

    for site in Path("static/sites").iterdir():
        if site.is_dir():
            project = f"static/sites/{site.name}/project.json"
            if not Path(project).exists():
                continue
            
            with open(project) as f:
                result.append(json.load(f))

    return {'sites': result}


@api.get('/status')
async def status_ep(response: Response):
    response.status_code = STATUS.value
    return {'status': STATUS.name}


@api.post('/status')
async def set_status_ep(new_status: ServerStatus, authorization: str, response: Response):
    if authorization != SECRET_KEY:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return status.HTTP_401_UNAUTHORIZED

    global STATUS
    STATUS = new_status

    return new_status.value


app.mount("/api", api)
