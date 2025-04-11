from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

if not os.path.exists("data"):
    os.makedirs("data")

app = FastAPI()
app.mount("/", StaticFiles(directory="data"), name="static")

