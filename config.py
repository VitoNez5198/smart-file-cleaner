"""
config.py - Configuración universal y reutilizable para Smart File Cleaner.
Funciona en cualquier computador (universidades, trabajo, desarrollo o uso personal).
"""

from pathlib import Path
import json

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

# 2. Reglas predeterminadas por palabras clave universales
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

# Archivo local de reglas personalizadas del usuario
USER_RULES_FILE = Path(__file__).parent / "user_rules.json"

def load_user_categories() -> dict:
    """Carga reglas personalizadas desde user_rules.json si existe."""
    if USER_RULES_FILE.exists():
        try:
            with open(USER_RULES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_user_category(category_name: str, keywords: list[str]) -> bool:
    """Guarda una nueva categoría personalizada en user_rules.json."""
    current_rules = load_user_categories()
    current_rules[category_name] = keywords
    try:
        with open(USER_RULES_FILE, "w", encoding="utf-8") as f:
            json.dump(current_rules, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la regla personalizada: {e}")
        return False

def get_all_keyword_categories() -> dict:
    """Devuelve las categorías combinadas dando prioridad máxima a las reglas del usuario."""
    user_cats = load_user_categories()
    combined = {}
    combined.update(user_cats)
    for cat, kws in KEYWORD_CATEGORIES.items():
        if cat not in combined:
            combined[cat] = kws
    return combined

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
