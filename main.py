from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import subprocess, uuid, os, shutil

app = FastAPI(title="Noise Removal API")

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
TMP_DIR = "tmp"

for d in [UPLOAD_DIR, OUTPUT_DIR, TMP_DIR]:
    os.makedirs(d, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/clean")
async def clean_audio(file: UploadFile = File(...)):
    # 1️⃣ MP3 check
    if not file.filename.lower().endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only MP3 files are supported")

    uid = str(uuid.uuid4())

    mp3_path = f"{UPLOAD_DIR}/{uid}.mp3"
    wav_path = f"{TMP_DIR}/{uid}.wav"
    out_dir = f"{OUTPUT_DIR}/{uid}"

    os.makedirs(out_dir, exist_ok=True)

    # 2️⃣ Save uploaded MP3
    with open(mp3_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # 3️⃣ MP3 → WAV (16k mono)
        subprocess.run([
            "ffmpeg", "-y",
            "-i", mp3_path,
            "-ar", "16000",
            "-ac", "1",
            wav_path
        ], check=True)

        # 4️⃣ DeepFilterNet
        subprocess.run([
            "deepfilter",
            wav_path,
            "-o", out_dir
        ], check=True)

        out_file = os.path.join(out_dir, f"{uid}_DeepFilterNet3.wav")

        if not os.path.exists(out_file):
            raise RuntimeError("Output not generated")

        # 5️⃣ Return file
        return FileResponse(
            out_file,
            media_type="audio/wav",
            filename="clean_audio.wav"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 6️⃣ Cleanup
        for p in [mp3_path, wav_path]:
            if os.path.exists(p):
                os.remove(p)
