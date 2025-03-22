from contextlib import asynccontextmanager
from fastapi import Body, FastAPI, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

import os
import sqlite3 
from typing import Annotated


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')


@asynccontextmanager
async def lifespan(_: FastAPI):
    with sqlite3.connect('blog.db') as conn:
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS blog (slug TEXT PRIMARY KEY, title TEXT, content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        cur.execute('CREATE TABLE IF NOT EXISTS tag (name TEXT PRIMARY KEY)')
        cur.execute('CREATE TABLE IF NOT EXISTS blog_tag (blog_slug TEXT, tag_name TEXT, PRIMARY KEY (blog_slug, tag_name))')
        conn.commit()

    yield


app = FastAPI(lifespan=lifespan)
api = FastAPI()


@app.get('/')
async def root():
    return FileResponse("static/html/index.html")


@app.get('/blog/{slug}')
async def blog(slug: str):
    template = open('static/html/blog.html').read()
    with sqlite3.connect('blog.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT title, content, created_at FROM blog WHERE slug = ?', (slug,))
        res = cur.fetchone()
        if not res:
            return FileResponse("static/html/404.html")
        title, content, created_at = res
        cur.execute('SELECT tag_name FROM blog_tag WHERE blog_slug = ?', (slug,))
        tags = [tag[0] for tag in cur.fetchall()]

        return HTMLResponse(template.format(title=title, content=content, created_at=created_at, tags=', '.join(tags)))


@api.post(
    '/blog',
    status_code=status.HTTP_201_CREATED,
    summary='Create a new blog post',
    description='Create a new blog post with a unique slug',
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized'
        }
    },
)
async def post_blog(
    slug: Annotated[str, Body(...)],
    title: Annotated[str, Body(...)],
    tags: Annotated[list[str], Body(...)],
    content: Annotated[str, Body(...)],
    authorization: Annotated[str, Body(...)]
):
    if authorization != SECRET_KEY:
        return status.HTTP_401_UNAUTHORIZED

    with sqlite3.connect('blog.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO blog (slug, title, content) VALUES (?, ?, ?)', (slug, title, content))
        for tag in tags:
            cur.execute('INSERT INTO tag (name) VALUES (?) ON CONFLICT DO NOTHING', (tag,))
            cur.execute('INSERT INTO blog_tag (blog_slug, tag_name) VALUES (?, ?)', (slug, tag))
        conn.commit()

    return status.HTTP_201_CREATED


@api.post(
    '/tag',
    status_code=status.HTTP_201_CREATED,
    summary='Create a new tag',
    description='Create a new tag if it does not already exist',
    responses={
        status.HTTP_200_OK: {
            'description': 'Tag already exists'
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized'
        }
    },
)
async def create_tag(
    name: Annotated[str, Body(...)],
    authorization: Annotated[str, Body(...)]
):
    if authorization != SECRET_KEY:
        return status.HTTP_401_UNAUTHORIZED

    with sqlite3.connect('blog.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tag (name) VALUES (?) ON CONFLICT DO NOTHING', (name,))
        conn.commit()

    return status.HTTP_201_CREATED if cur.rowcount else status.HTTP_200_OK


@api.get(
    '/tag',
    summary='List all tags',
    description='List all tags in the database',
)
async def list_tags():
    with sqlite3.connect('blog.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT name FROM tag')
        return [tag[0] for tag in cur.fetchall()]


@api.get(
    '/blog/{slug}',
    summary='Get a blog post',
    description='Get a blog post by its slug',
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Blog post not found'
        }
    },
)
async def get_blog(slug: str):
    with sqlite3.connect('blog.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT title, content, created_at FROM blog WHERE slug = ?', (slug,))
        res = cur.fetchone()
        if not res:
            return status.HTTP_404_NOT_FOUND
        return {'title': res[0], 'content': res[1], 'created_at': res[2]}


app.mount('/api', api)
app.mount('/static', StaticFiles(directory='static'), name='static')

