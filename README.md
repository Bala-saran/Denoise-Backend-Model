# Denoise Backend — Noise Removal API 🎙️🔇

> A lightweight, production-deployed FastAPI backend that accepts audio/file uploads and returns denoised output — live on Render.

---

## Overview

This is the backend service for a noise removal application. It exposes a REST API that accepts uploaded files, applies a denoising model, and returns the cleaned output — fully deployed and accessible via a public URL on Render.

---

## 🌐 Live Deployment

| Detail | Value |
|---|---|
| Platform | Render |
| Service | `noise-removal-api` |
| Runtime | Python |
| Server | Uvicorn (ASGI) |
| Status | ✅ Live |

---

## ✨ Features

- 📁 **File Upload Support** — Accepts multipart form-data (audio/image files)
- ⚡ **FastAPI** — High-performance async REST API
- 🚀 **Render Deployed** — One-click cloud deployment via `render.yaml`
- 🔇 **Noise Removal** — Processes uploaded files and returns clean output
- 🌐 **CORS Ready** — Accessible from any frontend client

---

## 🏗️ Architecture

```
Client (Frontend)
      │
      │  POST /denoise
      │  multipart/form-data (audio file)
      ▼
┌─────────────────────┐
│   FastAPI Backend   │  ← noise-removal-api (Render)
│   (main.py)         │
│                     │
│  1. Receive file    │
│  2. Apply denoising │
│  3. Return output   │
└─────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn (ASGI) |
| File Handling | python-multipart |
| Deployment | Render |
| Language | Python |

---

## 📁 Project Structure

```
Denoise-Backend-Model/
├── main.py             # FastAPI app — routes & denoising logic
├── requirements.txt    # Dependencies
├── render.yaml         # Render deployment config
└── runtime.txt         # Python version spec
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install fastapi uvicorn python-multipart
```

### Run Locally

```bash
# Clone the repo
git clone https://github.com/Bala-saran/Denoise-Backend-Model.git
cd Denoise-Backend-Model

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

API will be live at `http://localhost:8000`

Interactive docs at `http://localhost:8000/docs`

---

## 📡 API Usage

### `POST /denoise`

Upload a noisy file and receive the denoised output.

**Request:**
```bash
curl -X POST "https://your-render-url.onrender.com/denoise" \
  -F "file=@noisy_audio.wav"
```

**Response:**
```json
{
  "status": "success",
  "output": "denoised file or URL"
}
```

---

## ☁️ Deployment (Render)

This project includes a `render.yaml` for one-command deployment:

```yaml
services:
  - type: web
    name: noise-removal-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port 10000
```

**Steps:**
1. Push code to GitHub
2. Connect repo to [Render](https://render.com)
3. Render auto-detects `render.yaml` and deploys

---

## 🔗 Related

This backend is part of a larger denoising project. The frontend connects to this API to provide users with an interactive noise removal experience.

---

## 👨‍💻 Author

**Bala-saran** — [@Bala-saran](https://github.com/Bala-saran)

- 🌐 Portfolio: [balasarans-portfolio.netlify.app](https://balasarans-portfolio.netlify.app)
- 💼 LinkedIn: [linkedin.com/in/balasaran-v-380523309](https://linkedin.com/in/balasaran-v-380523309)

---

## 📜 License

Open for learning and personal use.
