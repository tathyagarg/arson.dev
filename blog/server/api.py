from typing import Annotated
import os
import re
from sqlite3 import IntegrityError

from fastapi import FastAPI, status, Body
import dotenv

from .database import connect

dotenv.load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE = 'blog.db' 

api = FastAPI()

def make_html_from_blog(title: str, markdown: str) -> tuple[str, str]:
    tree = f'''<h1>
        <a href="#head">{title}</a>
    </h1>'''

    final_content = ''

    ol = False
    ul = False

    figure_count = 0

    for i, line in enumerate(markdown.split('\n')):
        if line.startswith('#'):
            if ol:
                final_content += '</ol>'
                ol = False
            elif ul:
                final_content += '</ul>'
                ul = False

            hashes = len(line.split(' ')[0])
            tree += f'''<h{hashes + 1}>
                <a href=\"#h{i}\">{line.strip('#')}</a>
            </h{hashes + 1}>'''

            final_content += f'''<div class="head-container">
                <h{hashes + 1}>{line.strip("#")}</h{hashes + 1}>
                <a class="anchor" name="h{i}"></a>
            </div>'''
        else:
            if not ol and not ul:
                if line.startswith('1.'):
                    final_content += '<ol>'
                    ol = True
                elif line.startswith('-'):
                    final_content += '<ul>'
                    ul = True

            if ol and re.match(r'\d+\.', line):
                line_content = re.sub(r'\d+\.', '', line)
                final_content += f'<li>{line_content}</li>'
            elif ul and line.startswith('-'):
                final_content += f'<li>{line.strip("- ")}</li>'
            elif (m := re.match(r'!\[(.*)\]\((.*)\)', line)):
                figure_count += 1
                final_content += f'''<figure>
                    <img src="{m.group(2)}" alt="{m.group(1)}">
                    <figcaption>
                        <i>Figure {figure_count}:</i>
                        {m.group(1)}
                    </figcaption>
                </figure>'''
            else:
                result = re.sub(r'\[(.*)\]\((.*)\)', r'<a href="\2">\1</a>', line)
                final_content += f'<p>{result}</p>'

    return tree, final_content

@api.post(
    '/publish',
    status_code=status.HTTP_201_CREATED,
    summary='Create a new blog post',
    description='Create a new blog post with a unique slug',
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized'
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Slug already exists'
        }
    },
)
async def post_blog_ep(
    slug: Annotated[str, Body(...)],
    title: Annotated[str, Body(...)],
    tags: Annotated[list[str], Body(...)],
    content: Annotated[str, Body(...)],
    banner_url: Annotated[str, Body(...)],
    summary: Annotated[str, Body(...)],
    authorization: Annotated[str, Body(...)]
):
    if authorization != SECRET_KEY:
        return status.HTTP_401_UNAUTHORIZED

    with connect() as conn:
        cur = conn.cursor()
        try:
            tree, html = make_html_from_blog(title, content)
            cur.execute(
                '''INSERT INTO 
                    blog (slug, title, content, html, tree, banner_url, summary) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (slug, title, content, html, tree, banner_url, summary)
            )
        except IntegrityError:
            return status.HTTP_409_CONFLICT

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
async def post_tag_ep(
    name: Annotated[str, Body(...)],
    color: Annotated[str, Body(...)],
    authorization: Annotated[str, Body(...)]
):
    if authorization != SECRET_KEY:
        return status.HTTP_401_UNAUTHORIZED

    with connect() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tag (name, color) VALUES (?, ?) ON CONFLICT DO NOTHING', (name, color))
        conn.commit()

    return status.HTTP_201_CREATED if cur.rowcount else status.HTTP_200_OK


@api.get('/tag')
async def get_tag_ep(name: str):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT color FROM tag WHERE name = ?', (name,))
        res = cur.fetchone()

        if not res:
            return status.HTTP_404_NOT_FOUND

        return res[0]


@api.get(
    '/tags',
    summary='List all tags',
    description='List all tags in the database',
)
async def get_tags_ep():
    with connect() as conn:
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
async def get_blog_slug_ep(slug: str):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT title, content, created_at FROM blog WHERE slug = ?', (slug,))
        res = cur.fetchone()

        if not res:
            return status.HTTP_404_NOT_FOUND

        return {'title': res[0], 'content': res[1], 'created_at': res[2]}


@api.get('/articles')
async def get_articles_ep():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT slug, title, created_at FROM blog')
        return [
            {
                'slug': row[0],
                'title': row[1],
                'created_at': row[2]
            }
            for row in cur.fetchall()
        ]


@api.get('/recent')
async def get_recent_ep():
    result = []
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT slug, title, created_at, banner_url, summary FROM blog ORDER BY created_at DESC LIMIT 5')
        for row in cur.fetchall():
            cur.execute('SELECT tag_name FROM blog_tag WHERE blog_slug = ?', (row[0],))
            tags = [tag[0] for tag in cur.fetchall()]

            result.append({
                'slug': row[0],
                'title': row[1],
                'created_at': row[2],
                'banner_url': row[3],
                'summary': row[4],
                'tags': tags
            })

        return result



