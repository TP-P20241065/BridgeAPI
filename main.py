import uvicorn
from fastapi import FastAPI, HTTPException, Query, UploadFile
import yt_dlp as youtube_dl
import cv2
import io
from starlette.responses import StreamingResponse

app = FastAPI()

@app.post("/video")
async def root(current_view: str = Query(...)):
    youtube_url = current_view
    if 'youtube.com' in current_view:
        youtube_url = youtube_url.replace("youtube.com", "invidious.snopyta.org")
    elif 'youtu.be/' in current_view:
        youtube_url = youtube_url.replace("youtu.be/", "invidious.snopyta.org/watch?v=")

    ydl_opts = {
        'format': 'best[height<=480]/best',
        'extractor_args': {'youtube': {'player_client': ['invidious']}},
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.89 Safari/537.36'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        live_url = info['url']

    cap = cv2.VideoCapture(live_url)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise HTTPException(status_code=400, detail="No se pudo capturar la imagen desde la transmisión.")

    # Convertir el fotograma al formato JPG y guardarlo en un buffer en memoria
    _, buffer = cv2.imencode('.jpg', frame)
    image_data = io.BytesIO(buffer.tobytes())
    image_data.name = "boton_panico.jpg"

    # Crear el objeto UploadFile manualmente
    image = UploadFile(
        filename=image_data.name,
        file=image_data
    )

    # Retornar el archivo como respuesta usando StreamingResponse
    return StreamingResponse(image.file, media_type="image/jpeg", headers={
        "Content-Disposition": f"attachment; filename={image.filename}"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000, reload=False)
    input("Presiona Enter para cerrar el servidor...")

