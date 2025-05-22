from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from downloader import download_video
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/download/")
async def download(request: Request):
    data = await request.json()
    url = data["url"]
    quality = data.get("quality", "best")
    filename = f"{uuid.uuid4()}.mp4" if quality != "audio" else f"{uuid.uuid4()}.mp3"
    filepath = download_video(url, quality, filename)
    return FileResponse(path=filepath, filename=filename, media_type='application/octet-stream')