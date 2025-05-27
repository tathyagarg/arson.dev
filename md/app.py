import re
from typing import Annotated

import fastapi
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import HTMLResponse

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MarkdownObject(BaseModel):
    markdown: str


class HeadingObject(BaseModel):
    level: int
    text: str
    href: str


def to_slug(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()


def heading_maker_factory(level: int):
    def heading_maker(match: re.Match) -> str:
        text = match.group(2)
        slug = to_slug(text)
        return f'<h{level} id="{slug}" style="scroll-margin-top: 4rem">{text}</h{level}>'

    return heading_maker


def make_codeblock(match) -> str:
    lang = match.group(1)
    filename = match.group(2) or ''
    startline = match.group(3) or '1'
    content = match.group(4).strip()
    return f'<pre class="language-{lang} line-numbers" data-start="{startline}" data-filename="{filename}" style="padding-top: {"2.5em"*(filename != '')}"><code>{content}</code></pre>'


@app.get('/status')
async def root():
    return {'message': 'Markdown to HTML converter', 'doc': 'Docs at /docs'}


@app.post(
    '/convert',
    summary='Convert Markdown to HTML',
    description='Converts Markdown text to HTML. Supports headers, text styles, links, images, lists, and code blocks.',
    response_class=HTMLResponse,
    responses={
        200: {
            'description': 'HTML content',
            'content': {
                'text/html': {
                    'example': '<h1>Example</h1><p>This is an example.</p>'
                }
            }
        },
        422: {
            'description': 'Validation error'
        }
    },
)
async def convert(markdown: MarkdownObject):
    html = markdown.markdown

    # Convert headers
    for i in range(6, 0, -1):
        html = re.sub(r'^(#{%d}) (.*)' % i, heading_maker_factory(i), html, flags=re.MULTILINE)


    # Convert text styles
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'~~(.*?)~~', r'<del>\1</del>', html)
    html = re.sub(r'__(.*?)__', r'<u>\1</u>', html)

    # Convert links
    html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img alt="\1" src="\2" />', html)
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

    # Convert lists
    html = re.sub(r'^\- (.*?)\n', r'<ul><li>\1</li></ul>', html, flags=re.MULTILINE)
    html = re.sub(r'</ul><ul>', '', html)

    html = re.sub(r'^(\d+)\. (.*?)\n', r'<ol>\n<li>\2</li>\n</ol>', html, flags=re.MULTILINE)
    html = re.sub(r'</ol><ol>', '', html)

    html = re.sub(r'```([a-z]*?)(?:\{([a-zA-Z0-9\.]+)\})?(?:\{(\d+)\})?\n(.*?)```', make_codeblock, html, flags=re.DOTALL)

    return HTMLResponse(content=html, media_type='text/html')

@app.post(
    '/headings',
    summary='Extract Headings from Markdown',
    description='Extracts headings from Markdown text and returns them as a list of dictionaries with level, text, and href.',
    response_model=list[HeadingObject],
    responses={
        200: {
            'description': 'List of headings',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'level': 1,
                            'text': 'Heading 1',
                            'href': 'heading-1'
                        },
                        {
                            'level': 2,
                            'text': 'Subheading 1.1',
                            'href': 'subheading-1-1'
                        }
                    ]
                }
            }
        },
        422: {
            'description': 'Validation error'
        }
    },
)
async def get_headings(markdown: MarkdownObject):
    headings = []

    for line in markdown.markdown.splitlines():
        if (m := re.match(r'^(#+) (.*)', line)):
            text = m.group(2)
            headings.append(HeadingObject(
                level=len(m.group(1)),
                text=text,
                href=to_slug(text)
            ))

    return headings
