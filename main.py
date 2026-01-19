from fastapi import FastAPI, UploadFile, File, HTTPException
from df.enhance import enhance, init_df
import torchaudio
import uuid, os

app = FastAPI(title="Audio Denoise API")

model, df_state, _ = init_df()

@app.post("/clean")
async def clean_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only MP3 supported")

    uid = str(uuid.uuid4())
    inp = f"/tmp/{uid}.mp3"
    out = f"/tmp/{uid}.wav"

    with open(inp, "wb") as f:
        f.write(await file.read())

    audio, sr = torchaudio.load(inp)
    enhanced = enhance(model, df_state, audio, sr)
    torchaudio.save(out, enhanced, sr)

    return {
        "status": "success",
        "output": out
    }
