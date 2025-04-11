from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import shutil

if not os.path.exists("data"):
    os.makedirs("data")

app = FastAPI()
app.mount("/retrieve", StaticFiles(directory="data"), name="static")

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    with open(f"data/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}

