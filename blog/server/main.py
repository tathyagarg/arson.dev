from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from dotenv import load_dotenv

import os
import time
import logging
from enum import Enum

from .api import api
from .database import connect


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
LOG_FILE = os.getenv('LOG_FILE')

INDEX = 'static/html/index.html'
BLOG = 'static/html/blog.html'
NOT_FOUND = 'static/html/404.html'
PUBLISH = 'static/html/publish.html'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
)


class ServerStatus(int, Enum):
    OK = status.HTTP_200_OK
    MAINTAINENCE = status.HTTP_503_SERVICE_UNAVAILABLE


STATUS = ServerStatus.OK


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


@asynccontextmanager
async def lifespan(_: FastAPI):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS blog (
            slug TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            html TEXT,
            tree TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            banner_url TEXT,
            summary TEXT,
            is_archived BOOLEAN DEFAULT FALSE
        )''')
        cur.execute('CREATE TABLE IF NOT EXISTS tag (name TEXT PRIMARY KEY, dark_color TEXT, light_color TEXT)')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS blog_tag (
                blog_slug TEXT,
                tag_name TEXT,
                PRIMARY KEY (blog_slug, tag_name),
                FOREIGN KEY (blog_slug) REFERENCES blog(slug) ON DELETE CASCADE,
                FOREIGN KEY (tag_name) REFERENCES tag(name) ON DELETE CASCADE
            )''')
        conn.commit()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggingMiddleware, base='app')
api.add_middleware(LoggingMiddleware, base='api')

@app.get('/')
async def root():
    return FileResponse(INDEX)


@app.get('/blog/{slug}')
async def blog(slug: str):
    template = open(BLOG).read()
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''SELECT title, html, tree, created_at FROM blog WHERE slug = %s''', (slug,))
        res = cur.fetchone()

        if not res:
            return FileResponse(NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

        title, html, tree, created_at = res

        final_tags = []

        cur.execute('''
            SELECT tag.name, tag.dark_color, tag.light_color
            FROM blog_tag
            JOIN tag ON tag.name = blog_tag.tag_name
            WHERE blog_tag.blog_slug = %s
        ''', (slug,))
        for tag, dark_color, light_color in cur.fetchall():
            final_tags.append(f'''
                <span
                    class="tag"
                    data-dark="{dark_color}"
                    data-light="{light_color}"
                >
                    {tag}
                </span>
            ''')

        tag_div = '<div style="padding: 1em 0;">' + ' '.join(final_tags) + '</div>'

        return HTMLResponse(template.format(
            title=title,
            content=html,
            created_at=created_at,
            tags=tag_div,
            tree=tree,
            postScript='''
                <script>
                  const tags = document.querySelectorAll('.tag');
                  console.log(tags);
                  if (tags.length !== 0) {
                    tags.forEach(tag => {
                      tag.style.backgroundColor = theme === 'dark' ? tag.dataset.dark : tag.dataset.light;
                    });
                  }
                </script>
            '''
        ))


@app.get('/publish')
async def publish():
    return FileResponse(PUBLISH)


app.mount('/api', api)
app.mount('/static', StaticFiles(directory='static'), name='static')
