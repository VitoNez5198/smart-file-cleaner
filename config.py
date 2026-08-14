"""
config.py - Configuración inicial para Smart File Cleaner.
Define la estructura de carpetas, extensiones soportadas y reglas por palabras clave.
"""

from pathlib import Path

# Carpeta objetivo por defecto (por ejemplo: Descargas o Escritorio)
# Se puede cambiar según la carpeta que desees organizar.
TARGET_DIR = Path.home() / "Downloads"

# Mapeo de categorías por extensión de archivo
EXTENSION_CATEGORIES = {
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".odt"],
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"],
    "Archivos": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Video": [".mp4", ".mkv", ".avi", ".mov"],
    "Instaladores": [".exe", ".msi", ".dmg"],
    "Codigo": [".py", ".js", ".html", ".css", ".json", ".sql"]
}

# Mapeo de reglas avanzadas por palabras clave en el nombre del archivo
# (Se utilizará en el Paso 3)
KEYWORD_CATEGORIES = {
    "Postulaciones_CV": ["cv", "curriculum", "resume"],
    "AIEP": ["aiep", "tarea", "evaluacion", "clase"],
    "Contratos_Legales": ["contrato", "acuerdo", "firma", "finiquito"]
}

# Carpeta para archivos que no coincidan con ninguna categoría
DEFAULT_CATEGORY = "Otros"
