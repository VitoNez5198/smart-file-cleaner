"""
cleaner.py - Lógica principal del organizador de archivos y carpetas.
"""

import shutil
from pathlib import Path
import config

def get_category_by_keyword(item_path: Path) -> str | None:
    """
    Busca palabras clave en el nombre del archivo o carpeta.
    Si encuentra alguna coincidencia, retorna la categoría correspondiente.
    """
    stem_lower = item_path.stem.lower()
    
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

def determine_item_category(item_path: Path) -> str:
    """
    Determina la categoría final de un archivo o carpeta.
    """
    # 1. Intentar clasificar por palabras clave en el nombre
    keyword_category = get_category_by_keyword(item_path)
    if keyword_category:
        return keyword_category

    # 2. Si es una carpeta y no tuvo palabra clave, asignar a Proyectos_Y_Carpetas
    if item_path.is_dir():
        return getattr(config, "DEFAULT_FOLDER_CATEGORY", "Proyectos_Y_Carpetas")

    # 3. Si es un archivo sin palabra clave, clasificar por extensión
    return get_category_by_extension(item_path)

def determine_file_category(file_path: Path) -> str:
    """
    Mantiene compatibilidad hacia atrás para archivos.
    """
    return determine_item_category(file_path)

def get_unique_destination(dest_dir: Path, item_name: str) -> Path:
    """
    Genera un nombre único si ya existe un archivo o carpeta con el mismo nombre en la categoría de destino.
    Ejemplo: proyecto -> proyecto (1)
    """
    dest_path = dest_dir / item_name
    if not dest_path.exists():
        return dest_path
    
    path_obj = Path(item_name)
    stem = path_obj.stem
    suffix = path_obj.suffix
    counter = 1
    
    while dest_path.exists():
        if suffix:
            dest_path = dest_dir / f"{stem} ({counter}){suffix}"
        else:
            dest_path = dest_dir / f"{item_name} ({counter})"
        counter += 1
        
    return dest_path

def is_protected_item(item: Path, target_dir: Path, dest_dir: Path) -> bool:
    """
    Verifica si un elemento está protegido o debe ser ignorado.
    """
    name_lower = item.name.lower()
    
    # 1. Archivos ocultos o de sistema (ej: .git, .ds_store)
    if name_lower.startswith("."):
        return True
        
    # 2. Nombres protegidos explícitamente en config
    protected = getattr(config, "PROTECTED_NAMES", {"smart-file-cleaner", "smart_file_cleaner", "desktop.ini", "$recycle.bin", ".git"})
    if name_lower in protected:
        return True

    # 3. Extensiones ignoradas (ej: accesos directos .lnk)
    ignored_exts = getattr(config, "IGNORED_EXTENSIONS", {".lnk", ".url", ".sys", ".ini"})
    if item.is_file() and item.suffix.lower() in ignored_exts:
        return True

    # 4. Evitar mover la carpeta de destino o carpetas creadas dentro del destino
    try:
        if item.resolve() == target_dir.resolve() or item.resolve() == dest_dir.resolve():
            return True
        # Si el item es una carpeta en la raíz del destino que coincide con nuestras categorías conocidas
        all_categories = set(config.EXTENSION_CATEGORIES.keys()).union(config.KEYWORD_CATEGORIES.keys())
        all_categories.add(config.DEFAULT_CATEGORY)
        all_categories.add(getattr(config, "DEFAULT_FOLDER_CATEGORY", "Proyectos_Y_Carpetas"))
        
        if item.is_dir() and item.name in all_categories and (item.parent.resolve() == dest_dir.resolve() or item.parent.resolve() == target_dir.resolve()):
            return True
    except Exception:
        pass

    return False

def organize_folder(
    target_dir: Path, 
    dest_dir: Path = None, 
    dry_run: bool = True,
    include_files: bool = True,
    include_folders: bool = False
):
    """
    Recorre la carpeta objetivo y organiza archivos y/o carpetas enviándolos
    a la carpeta de destino especificada.
    
    :param target_dir: Ruta de la carpeta a limpiar (origen).
    :param dest_dir: Ruta de la carpeta donde se crearán las subcarpetas organizadas (destino). Si es None, usa target_dir.
    :param dry_run: Si es True, solo muestra simulación.
    :param include_files: Si debe mover archivos sueltos.
    :param include_folders: Si debe mover carpetas sueltas / proyectos.
    """
    if not target_dir.exists():
        print(f"[ERROR] La carpeta origen no existe: {target_dir}")
        return

    if dest_dir is None:
        dest_dir = target_dir

    mode_label = "[MODO SIMULACIÓN - DRY RUN]" if dry_run else "[MODO REAL]"
    print(f"\n{mode_label} Origen: {target_dir} ➔ Destino: {dest_dir}\n" + "-" * 60)

    moved_count = 0

    for item in target_dir.iterdir():
        # Filtro de protección
        if is_protected_item(item, target_dir, dest_dir):
            continue

        # Filtrar por tipo (archivos / carpetas)
        if item.is_file() and not include_files:
            continue
        if item.is_dir() and not include_folders:
            continue

        # Determinar categoría
        category = determine_item_category(item)
        target_category_folder = dest_dir / category
        dest_item_path = get_unique_destination(target_category_folder, item.name)

        item_type_label = "📁 [CARPETA]" if item.is_dir() else "📄 [ARCHIVO]"

        if dry_run:
            print(f"[SIMULACIÓN] {item_type_label} {item.name} ➔ {category}/{dest_item_path.name}")
        else:
            target_category_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(dest_item_path))
            print(f"[MOVIDO] {item_type_label} {item.name} ➔ {category}/{dest_item_path.name}")

        moved_count += 1

    print("-" * 60)
    print(f"Proceso finalizado. Total de elementos procesados: {moved_count}\n")


def export_scan_report(target_dir: Path, output_file: str = "scan_report.json"):
    """
    Escanea la carpeta objetivo y genera un archivo de reporte JSON detallado.
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

        category = determine_item_category(item)
        ext = item.suffix.lower() if item.suffix else "sin_extension"

        file_data = {
            "name": item.name,
            "category": category,
            "extension": ext,
            "size_kb": round(item.stat().st_size / 1024, 2)
        }
        files_info.append(file_data)

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
    print("-" * 60)
    print(f"Total de archivos escaneados: {len(files_info)}")
    print("Resumen por categorías propuestas:")
    for cat, count in category_summary.items():
        print(f"  - {cat}: {count} archivos")
    print(f"Archivos sin clasificar ('Otros'): {len(unclassified_files)}")
    print("-" * 60)
