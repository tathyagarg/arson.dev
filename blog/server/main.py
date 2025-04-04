from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

import os

from .api import api
from .database import connect


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE = 'blog.db' 
INDEX = 'static/html/index.html'
BLOG = 'static/html/blog.html'
NOT_FOUND = 'static/html/404.html'
PUBLISH = 'static/html/publish.html'


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
