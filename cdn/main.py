from fastapi import FastAPI, UploadFile
import argon2
import dotenv

import os
from pathlib import Path

from fastapi.responses import FileResponse

ph = argon2.PasswordHasher()
dotenv.load_dotenv()

FILES_PATH = Path(os.getenv('FILES_PATH', '/var/www/files'))
PASSPHRASE = os.getenv('PASSPHRASE', 'unauthenticated')

app = FastAPI()

@app.post('/upload')
async def upload_file(passphrase: str, file: UploadFile):
    try:
        ph.verify(PASSPHRASE, passphrase)
    except argon2.exceptions.VerifyMismatchError:
        return {"error": "Invalid passphrase"}, 401

    FILES_PATH.mkdir(parents=True, exist_ok=True)

    file_path = FILES_PATH / ((file.filename or '') + os.urandom(8).hex())

    with file_path.open('wb') as f:
        content = await file.read()
        f.write(content)

    return {"filename": file_path.name, "size": len(content), "path": str(file_path)}

@app.get('/files/{filename}')
async def get_file(filename: str):
    file_path = FILES_PATH / filename

    if not file_path.exists():
        return {"error": "File not found"}, 404

    return FileResponse(
        file_path,
        media_type='image/png',
        filename=file_path.name,
        headers={"Content-Disposition": "inline"}
    )


