from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/clean")
async def clean_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        return {"error": "Only MP3 allowed"}

    uid = str(uuid.uuid4())
    input_path = f"{UPLOAD_DIR}/{uid}.mp3"
    output_path = f"{OUTPUT_DIR}/{uid}_clean.mp3"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ⚠️ Placeholder lightweight denoise
    # (Render‑safe: no torch)
    shutil.copy(input_path, output_path)

    return FileResponse(
        output_path,
        media_type="audio/mpeg",
        filename="clean_audio.mp3"
    )