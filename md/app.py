import re
from typing import Annotated

import fastapi
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {'message': 'Markdown to HTML converter', 'doc': 'Send a POST request to /convert with markdown text in the body.'}

@app.post('/convert')
async def convert(markdown: Annotated[str, Body(...)]):
    html = markdown

    # Convert headers
    for i in range(6, 0, -1):
        html = re.sub(rf'{"#" * i} (.*?)\n', rf'<h{i}>\1</h{i}>', html)

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

    html = re.sub(r'```(.*?)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)

    return HTMLResponse(content=html, media_type='text/html')
