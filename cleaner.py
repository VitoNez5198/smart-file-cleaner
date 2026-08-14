"""
cleaner.py - Lógica principal del organizador de archivos por extensión.
"""

import shutil
from pathlib import Path
import config

def get_category_by_extension(file_path: Path) -> str:
    """
    Retorna la categoría correspondiente según la extensión del archivo.
    """
    ext = file_path.suffix.lower()
    for category, extensions in config.EXTENSION_CATEGORIES.items():
        if ext in extensions:
            return category
    return config.DEFAULT_CATEGORY

def get_unique_destination(dest_dir: Path, file_name: str) -> Path:
    """
    Genera un nombre único si ya existe un archivo con el mismo nombre en la carpeta de destino.
    Ejemplo: archivo.pdf -> archivo (1).pdf
    """
    dest_path = dest_dir / file_name
    if not dest_path.exists():
        return dest_path
    
    stem = dest_path.stem
    suffix = dest_path.suffix
    counter = 1
    
    while dest_path.exists():
        dest_path = dest_dir / f"{stem} ({counter}){suffix}"
        counter += 1
        
    return dest_path

def organize_folder(target_dir: Path, dry_run: bool = True):
    """
    Recorre la carpeta objetivo y organiza los archivos en subcarpetas según su extensión.
    
    :param target_dir: Ruta de la carpeta a limpiar (pathlib.Path)
    :param dry_run: Si es True, solo muestra lo que haría sin mover archivos reales.
    """
    if not target_dir.exists():
        print(f"[ERROR] La carpeta objetivo no existe: {target_dir}")
        return

    mode_label = "[MODO SIMULACIÓN - DRY RUN]" if dry_run else "[MODO REAL]"
    print(f"\n{mode_label} Iniciando organización en: {target_dir}\n" + "-" * 50)

    moved_count = 0

    # Iterar sobre los elementos de la carpeta objetivo
    for item in target_dir.iterdir():
        # Ignorar si es un directorio o un archivo oculto/de sistema (empieza con .)
        if item.is_dir() or item.name.startswith("."):
            continue
        
        # Determinar categoría por extensión
        category = get_category_by_extension(item)
        dest_folder = target_dir / category
        dest_file_path = get_unique_destination(dest_folder, item.name)

        if dry_run:
            print(f"[SIMULACIÓN] {item.name} ➔ {category}/{dest_file_path.name}")
        else:
            # Crear la carpeta de destino si no existe
            dest_folder.mkdir(parents=True, exist_ok=True)
            # Mover el archivo usando shutil.move
            shutil.move(str(item), str(dest_file_path))
            print(f"[MOVIDO] {item.name} ➔ {category}/{dest_file_path.name}")

        moved_count += 1

    print("-" * 50)
    print(f"Proceso finalizado. Total de archivos procesados: {moved_count}\n")

