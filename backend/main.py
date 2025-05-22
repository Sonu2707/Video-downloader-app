from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

# Allow Vercel frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://video-downloader-app-beryl.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str
    format: str  # e.g. "mp3", "mp4", "720p", "1080p"

@app.post("/download/")
async def download(req: DownloadRequest):
    url = req.url
    format = req.format

    # Output folder
    os.makedirs("downloads", exist_ok=True)
    output_template = "downloads/%(title)s.%(ext)s"

    # yt-dlp command
    if format == "mp3":
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output_template,
            url
        ]
    elif format in ["mp4", "720p", "1080p"]:
        cmd = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o", output_template,
            url
        ]
    else:
        raise HTTPException(status_code=400, detail="Invalid format requested.")

    try:
        subprocess.run(cmd, check=True)
        return {"status": "success", "message": f"Download started for {format}"}
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Download failed. Check the URL or format.")
