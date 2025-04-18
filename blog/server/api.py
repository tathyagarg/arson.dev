from typing import Annotated
import os
import re
from sqlite3 import IntegrityError
from enum import Enum

from fastapi import FastAPI, Response, status, Body
import dotenv

from .database import connect

dotenv.load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

class ServerStatus(int, Enum):
    OK = status.HTTP_200_OK 
    MAINTENANCE = status.HTTP_503_SERVICE_UNAVAILABLE

STATUS = ServerStatus.OK

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
    authorization: Annotated[str, Body(...)],
    response: Response
):
    if authorization != SECRET_KEY:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return status.HTTP_401_UNAUTHORIZED

    with connect() as conn:
        cur = conn.cursor()
        try:
            tree, html = make_html_from_blog(title, content)
            cur.execute(
                '''INSERT INTO 
                    blog (slug, title, content, html, tree, banner_url, summary) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (slug, title, content, html, tree, banner_url, summary)
            )
        except IntegrityError:
            response.status_code = status.HTTP_409_CONFLICT
            return {
                'status': status.HTTP_409_CONFLICT,
                'error': 'Slug already exists'
            }

        for tag in tags:
            cur.execute('INSERT INTO tag (name) VALUES (%s) ON CONFLICT DO NOTHING', (tag,))
            cur.execute('INSERT INTO blog_tag (blog_slug, tag_name) VALUES (%s, %s)', (slug, tag))
        conn.commit()

    return {
        'status': status.HTTP_201_CREATED,
        'info': 'Blog post created'
    }


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
    authorization: Annotated[str, Body(...)],
    response: Response
):
    if authorization != SECRET_KEY:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            'status': status.HTTP_401_UNAUTHORIZED,
            'error': 'Unauthorized'
        } 

    with connect() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tag (name, color) VALUES (%s, %s) ON CONFLICT DO NOTHING', (name, color))
        conn.commit()

    status_code = status.HTTP_201_CREATED if cur.rowcount else status.HTTP_200_OK
    response.status_code = status_code

    return {
        'status': status_code,
        'info': 'Tag created' if status_code == status.HTTP_201_CREATED else 'Tag already exists'
    }


@api.get('/tag')
async def get_tag_ep(name: str, response: Response):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT color FROM tag WHERE name = %s', (name,))
        res = cur.fetchone()

        if not res:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                'status': status.HTTP_404_NOT_FOUND,
            }

        return {
            'status': status.HTTP_200_OK,
            'color': res[0]
        }


@api.get(
    '/tags',
    summary='List all tags',
    description='List all tags in the database',
)
async def get_tags_ep():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT name FROM tag')
        return {
            'status': status.HTTP_200_OK,
            'tags': [tag[0] for tag in cur.fetchall()]
        }


@api.get('/recent')
async def get_recent_ep():
    result = []
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT slug, title, created_at, banner_url, summary FROM blog ORDER BY created_at DESC LIMIT 5')
        for row in cur.fetchall():
            cur.execute('''
                SELECT tag.name, tag.dark_color, tag.light_color
                FROM blog_tag
                JOIN tag ON tag.name = blog_tag.tag_name
                WHERE blog_tag.blog_slug = %s
            ''', (row[0],))
            tags = [{
                'name': tag[0],
                'dark_color': tag[1],
                'light_color': tag[2]
            } for tag in cur.fetchall()]

            result.append({
                'slug': row[0],
                'title': row[1],
                'created_at': row[2],
                'banner_url': row[3],
                'summary': row[4],
                'tags': tags
            })

        return {
            'status': status.HTTP_200_OK,
            'articles': result
        }


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

