"""
config.py - Configuración universal y reutilizable para Smart File Cleaner.
Funciona en cualquier computador (universidades, trabajo, desarrollo o uso personal).
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

# 2. Reglas prioritarias por palabras clave universales (El orden de prioridad importa)
KEYWORD_CATEGORIES = {
    # 1. Prioridad Máxima: Currículums y Postulaciones Laborales
    "Postulaciones_CV": [
        "cv", "curriculum", "resume", "carta de compromiso", "logros", "elevator pitch"
    ],
    # 2. Material de Estudio, Cursos y Asignaturas (Universal para cualquier instituto/universidad/colegio)
    "Material_Estudio_Cursos": [
        "aiep", "semana", "unidad", "tema", "actividad", "evaluacion", "curso",
        "apunte", "clase", "taller", "orientados-a-objetos", "analisis-de-sistemas",
        "plantilla de entrega", "lab -", "demostración", "guia", "tarea", "entrega", "syllabus"
    ],
    # 3. Credenciales Cloud y Claves de Acceso (AWS, Azure, GCP, SSH)
    "Credenciales_Cloud": [
        "labsuser", "accesskeys", "amazon", "aws", "azure", "gcp", "clave1", "ssh_key"
    ],
    # 4. Capturas de Pantalla
    "Capturas_Pantalla": [
        "whatsapp", "captura", "pantalla", "screenshot"
    ]
}

# Categoría por defecto para carpetas sueltas / proyectos no identificados por palabras clave
DEFAULT_FOLDER_CATEGORY = "Proyectos_Y_Carpetas"

# Carpeta por defecto para archivos
DEFAULT_CATEGORY = "Otros"

# Archivos y carpetas protegidos que NUNCA deben ser movidos ni modificados
PROTECTED_NAMES = {
    "smart-file-cleaner", "smart_file_cleaner", "desktop.ini", "$recycle.bin", ".git"
}

# Extensiones ignoradas en el Escritorio (accesos directos y configuración)
IGNORED_EXTENSIONS = {
    ".lnk", ".url", ".sys", ".ini"
}
