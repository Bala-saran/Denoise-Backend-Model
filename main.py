from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import uuid, os
from pydub import AudioSegment
from df.enhance import enhance, init_df

app = FastAPI(title="Noise Removal API")

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

model, df_state = init_df()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/clean")
async def clean_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only MP3 supported")

    uid = str(uuid.uuid4())

    mp3_path = f"{UPLOAD_DIR}/{uid}.mp3"
    wav_path = f"{UPLOAD_DIR}/{uid}.wav"
    out_wav = f"{OUTPUT_DIR}/{uid}_clean.wav"
    out_mp3 = f"{OUTPUT_DIR}/{uid}_clean.mp3"

    # save upload
    with open(mp3_path, "wb") as f:
        f.write(await file.read())

    # mp3 → wav
    AudioSegment.from_mp3(mp3_path).set_frame_rate(48000).set_channels(1).export(wav_path, format="wav")

    # denoise
    enhance(model, df_state, wav_path, out_wav)

    # wav → mp3
    AudioSegment.from_wav(out_wav).export(out_mp3, format="mp3")

    return FileResponse(out_mp3, media_type="audio/mpeg", filename="cleaned.mp3")
