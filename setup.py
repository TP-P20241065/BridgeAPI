# setup.py
from cx_Freeze import setup, Executable

# Configuración de la aplicación
setup(
    name="BridgeAPI",
    version="1.0",
    description="Obtención de imagen de YouTube",
    options={
        "build_exe": {
            "packages": [
                "cv2",
                "fastapi",
                "io",
                "starlette",
                "uvicorn",
                "yt_dlp"
            ],
            "build_exe": "dist"
        }
    },
    executables=[Executable("main.py", base=None)]
)
