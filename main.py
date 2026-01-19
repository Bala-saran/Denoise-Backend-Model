from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import uuid, os, subprocess

app = FastAPI(title="Noise Removal API")

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
TMP_DIR = "tmp"

for d in [UPLOAD_DIR, OUTPUT_DIR, TMP_DIR]:
    os.makedirs(d, exist_ok=True)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/clean")
async def clean_audio(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    input_path = f"{UPLOAD_DIR}/{uid}_{file.filename}"
    clean_wav = f"{TMP_DIR}/{uid}_clean.wav"
    output_mp3 = f"{OUTPUT_DIR}/{uid}_clean.mp3"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Convert any format → wav
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000", "-ac", "1",
        clean_wav
    ], check=True)

    # DeepFilter
    subprocess.run([
        "deepfilter", clean_wav, "-o", TMP_DIR
    ], check=True)

    df_out = clean_wav.replace(".wav", "_DeepFilterNet3.wav")

    # Convert to mp3
    subprocess.run([
        "ffmpeg", "-y", "-i", df_out, output_mp3
    ], check=True)

    return FileResponse(
        output_mp3,
        media_type="audio/mpeg",
        filename="cleaned.mp3"
    )
