"""
cleaner.py - Lógica principal del organizador de archivos por extensión.
"""

import shutil
from pathlib import Path
import config

def get_category_by_keyword(file_path: Path) -> str | None:
    """
    Busca palabras clave en el nombre del archivo (sin extensión).
    Si encuentra alguna coincidencia, retorna la categoría correspondiente.
    """
    stem_lower = file_path.stem.lower()
    
    for category, keywords in config.KEYWORD_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in stem_lower:
                return category
    return None

def get_category_by_extension(file_path: Path) -> str:
    """
    Retorna la categoría correspondiente según la extensión del archivo.
    """
    ext = file_path.suffix.lower()
    for category, extensions in config.EXTENSION_CATEGORIES.items():
        if ext in extensions:
            return category
    return config.DEFAULT_CATEGORY

def determine_file_category(file_path: Path) -> str:
    """
    Determina la categoría final de un archivo priorizando palabras clave
    sobre la extensión del archivo.
    """
    # 1. Intentar clasificar por palabras clave en el nombre
    keyword_category = get_category_by_keyword(file_path)
    if keyword_category:
        return keyword_category

    # 2. Si no hay coincidencia por palabra clave, clasificar por extensión
    return get_category_by_extension(file_path)

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
    Recorre la carpeta objetivo y organiza los archivos en subcarpetas
    priorizando palabras clave y luego extensiones.
    
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
        
        # Determinar categoría (Palabra Clave > Extensión > Otros)
        category = determine_file_category(item)
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


def export_scan_report(target_dir: Path, output_file: str = "scan_report.json"):
    """
    Escanea la carpeta objetivo y genera un archivo de reporte JSON detallado con el inventario
    de archivos, sus categorías asignadas, extensiones y sugerencias.
    """
    import json

    if not target_dir.exists():
        print(f"[ERROR] La carpeta objetivo no existe: {target_dir}")
        return

    print(f"\n[SCAN] Escaneando e inventariando carpeta: {target_dir}...")

    files_info = []
    category_summary = {}
    unclassified_files = []

    for item in target_dir.iterdir():
        if item.is_dir() or item.name.startswith("."):
            continue

        category = determine_file_category(item)
        ext = item.suffix.lower() if item.suffix else "sin_extension"

        file_data = {
            "name": item.name,
            "category": category,
            "extension": ext,
            "size_kb": round(item.stat().st_size / 1024, 2)
        }
        files_info.append(file_data)

        # Contador por categoría
        category_summary[category] = category_summary.get(category, 0) + 1

        if category == config.DEFAULT_CATEGORY:
            unclassified_files.append(item.name)

    report = {
        "target_directory": str(target_dir),
        "total_files": len(files_info),
        "category_summary": category_summary,
        "unclassified_count": len(unclassified_files),
        "unclassified_files": unclassified_files,
        "files": files_info
    }

    output_path = Path(output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[EXITO] Reporte de escaneo guardado en: {output_path.resolve()}")
    print("-" * 50)
    print(f"Total de archivos escaneados: {len(files_info)}")
    print("Resumen por categorías propuestas:")
    for cat, count in category_summary.items():
        print(f"  - {cat}: {count} archivos")
    print(f"Archivos sin clasificar ('Otros'): {len(unclassified_files)}")
    print("-" * 50)


