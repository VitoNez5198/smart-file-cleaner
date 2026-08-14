"""
config.py - Configuración personalizada para Smart File Cleaner.
Basada en el análisis del inventario real de 652 archivos del usuario.
"""

from pathlib import Path

# Carpeta objetivo por defecto
TARGET_DIR = Path.home() / "Downloads"

# 1. Categorías por extensión de archivo
EXTENSION_CATEGORIES = {
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".odt", ".csv", ".rtf", ".md"],
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".heic", ".heif", ".ico", ".avif"],
    "Libros_Ebooks": [".epub", ".mobi", ".azw3", ".fb2"],
    "Archivos_Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Instaladores_Software": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".vsix", ".msix"],
    "Codigo_Notebooks": [".py", ".ipynb", ".js", ".html", ".css", ".json", ".sql", ".sh", ".ps1", ".cpp", ".java", ".mdj"],
    "Credenciales_Cloud": [".pem", ".ppk", ".key"],
    "Logs_Temporales": [".log", ".tmp", ".bak"]
}

# 2. Reglas prioritarias por palabras clave (El orden de prioridad importa)
KEYWORD_CATEGORIES = {
    # 1. Prioridad Máxima: Currículums y Postulaciones Laborales
    "Postulaciones_CV": [
        "cv", "curriculum", "resume", "carta de compromiso", "logros", "elevator pitch"
    ],
    # 2. Material de Estudio Universidad AIEP
    "AIEP_Material_Estudio": [
        "aiep", "semana", "unidad", "tema", "pro303", "soo301", "actividad",
        "apunte", "clase", "taller", "orientados-a-objetos", "analisis-de-sistemas",
        "plantilla de entrega", "lab -", "demostración"
    ],
    # 3. Credenciales Cloud AWS
    "AWS_Cloud_Credenciales": [
        "labsuser", "accesskeys", "amazon", "aws", "clave1"
    ],
    # 4. Capturas de Pantalla
    "Capturas_Pantalla": [
        "whatsapp", "captura", "pantalla", "screenshot"
    ]
}

# Carpeta por defecto
DEFAULT_CATEGORY = "Otros"
