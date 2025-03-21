from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

api = FastAPI()


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

app.mount("/api", api)
