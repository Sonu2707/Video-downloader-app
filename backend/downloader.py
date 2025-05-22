import yt_dlp

def download_video(url, quality, output_filename):
    ydl_opts = {
        'outtmpl': f'/tmp/{output_filename}',
        'quiet': True
    }
    if quality == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif quality == "worst":
        ydl_opts['format'] = 'worst'
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f"/tmp/{output_filename}"