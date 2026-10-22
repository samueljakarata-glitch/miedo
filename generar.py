
import os
import random
import subprocess
import requests
import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ANCHO, ALTO = 720, 1280
FPS = 24
DURACION = 50

def narrar(texto):
    # Voz de prueba. Luego la cambiaremos por TTS
    # neuronal en español latino.
    os.makedirs("salida", exist_ok=True)
    url = "https://translate.google.com/translate_tts"
    r = requests.get(
        url,
        params={
            "ie": "UTF-8",
            "client": "tw-ob",
            "tl": "es",
            "q": texto
        },
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=60
    )
    r.raise_for_status()
    with open("salida/voz.mp3", "wb") as f:
        f.write(r.content)

def crear_video():
    historia = [
        "En todas las fotografías de mi familia aparecía el mismo hombre.",
        "En la primera foto estaba lejos, al fondo de la calle.",
        "En las fotografías siguientes comenzó a acercarse.",
        "Nadie recordaba haberlo visto en persona.",
        "Hasta que apareció detrás de mi abuela.",
        "La última fotografía fue tomada anoche.",
        "El hombre estaba mirando desde la ventana de nuestra casa.",
        "Pero lo peor es que la fotografía fue tomada desde dentro."
    ]

    narracion = " ".join(historia)
    narrar(narracion)

    # Crear una secuencia visual sencilla para verificar
    # que el sistema genera un MP4 válido.
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    proceso = subprocess.Popen([
        ffmpeg, "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x101018:s={ANCHO}x{ALTO}:r={FPS}:d={DURACION}",
        "-i", "salida/voz.mp3",
        "-vf", "format=yuv420p",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-movflags", "+faststart",
        "salida/video.mp4"
    ])
    proceso.wait()
    if proceso.returncode != 0:
        raise RuntimeError("Falló la creación del video")

    print("Video generado: salida/video.mp4")

if __name__ == "__main__":
    crear_video()
      
