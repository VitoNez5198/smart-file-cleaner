"""
cleaner.py - Lógica principal del organizador de archivos y carpetas.
"""

import shutil
from pathlib import Path
import config
import re

def get_category_by_keyword(item_path: Path) -> str | None:
    """
    Busca palabras clave y patrones en el nombre del archivo o carpeta.
    Normaliza guiones y guiones bajos para búsquedas flexibles.
    """
    stem_raw = item_path.stem.lower()
    stem_normalized = stem_raw.replace("_", " ").replace("-", " ")
    
    # 1. Patrón Regex universal de códigos de asignatura (2 a 4 letras seguidas de 2 a 4 números, ej: CS101, PRO402, MAT2001)
    if re.search(r'[a-zA-Z]{2,4}\d{2,4}', stem_raw):
        return "Material_Estudio_Cursos"

    # 2. Búsqueda por palabras clave explícitas (incluye las reglas personalizadas del usuario)
    keyword_cats = config.get_all_keyword_categories()
    for category, keywords in keyword_cats.items():
        for keyword in keywords:
            kw_lower = keyword.lower()
            if kw_lower in stem_raw or kw_lower in stem_normalized:
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
    """
    if not target_dir.exists():
        print(f"[ERROR] La carpeta origen no existe: {target_dir}")
        return

    if dest_dir is None:
        dest_dir = target_dir

    mode_label = "[MODO SIMULACIÓN - DRY RUN]" if dry_run else "[MODO REAL]"
    print(f"\n{mode_label} Origen: {target_dir} ➔ Destino: {dest_dir}\n" + "-" * 60)

    moved_count = 0
    skipped_count = 0

    try:
        items = list(target_dir.iterdir())
    except Exception as e:
        print(f"[ERROR] No se pudo leer el contenido de la carpeta: {e}")
        return

    for item in items:
        if not item.exists():
            continue

        if is_protected_item(item, target_dir, dest_dir):
            continue

        if item.is_file() and not include_files:
            continue
        if item.is_dir() and not include_folders:
            continue

        category = determine_item_category(item)
        target_category_folder = dest_dir / category
        dest_item_path = get_unique_destination(target_category_folder, item.name)

        item_type_label = "📁 [CARPETA]" if item.is_dir() else "📄 [ARCHIVO]"

        if dry_run:
            print(f"[SIMULACIÓN] {item_type_label} {item.name} ➔ {category}/{dest_item_path.name}")
            moved_count += 1
        else:
            try:
                target_category_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(dest_item_path))
                print(f"[MOVIDO] {item_type_label} {item.name} ➔ {category}/{dest_item_path.name}")
                moved_count += 1
            except Exception as e:
                skipped_count += 1
                print(f"⚠️  [OMITIDO - EN USO O PERMISOS] {item_type_label} {item.name} ({e})")

    print("-" * 60)
    print(f"Proceso finalizado. Éxito: {moved_count} elementos | Omitidos/Errores: {skipped_count}\n")
    
    # Limpieza automática de carpetas temporales que hayan quedado vacías
    cleanup_empty_folders(target_dir, dry_run=dry_run)


def deep_organize_folder(target_dir: Path, dry_run: bool = True):
    """
    Recorre recursivamente las subcarpetas de categorías (ej: Documentos, Otros, etc.)
    y evalúa todos los archivos sueltos en su interior para re-clasificarlos y moverlos
    a su verdadera categoría. Ignora carpetas protegidas de proyectos (Proyectos_Y_Carpetas).
    """
    if not target_dir.exists():
        print(f"[ERROR] La carpeta origen no existe: {target_dir}")
        return

    mode_label = "[MODO SIMULACIÓN - DRY RUN]" if dry_run else "[MODO REAL]"
    print(f"\n{mode_label} 🌐 LIMPIEZA PROFUNDA GLOBAL en: {target_dir}\n" + "-" * 60)

    moved_count = 0
    skipped_count = 0

    protected_folders = {
        getattr(config, "DEFAULT_FOLDER_CATEGORY", "Proyectos_Y_Carpetas"),
        "Proyectos_Y_Carpetas", "smart-file-cleaner", "smart_file_cleaner"
    }

    try:
        subfolders = [f for f in target_dir.iterdir() if f.is_dir() and f.name not in protected_folders and not f.name.startswith(".")]
    except Exception as e:
        print(f"[ERROR] No se pudo leer el contenido de la carpeta: {e}")
        return

    for subfolder in subfolders:
        try:
            # Solo inspeccionar archivos directos dentro de la subcarpeta (profundidad 1)
            files_in_sub = [f for f in subfolder.iterdir() if f.is_file() and not f.name.startswith(".")]
        except Exception:
            continue

            # Extensiones ignoradas
            ignored_exts = getattr(config, "IGNORED_EXTENSIONS", {".lnk", ".url", ".sys", ".ini"})
            if file_item.suffix.lower() in ignored_exts:
                continue

            # Determinar categoría ideal
            new_category = determine_item_category(file_item)

            # Si la categoría actual del archivo ya coincide con donde está guardado, no se mueve
            if file_item.parent.name == new_category:
                continue

            # Si la categoría ideal es diferente, re-ubicamos el archivo
            target_category_folder = target_dir / new_category
            dest_file_path = get_unique_destination(target_category_folder, file_item.name)

            rel_origin = f"{subfolder.name}/{file_item.name}"

            if dry_run:
                print(f"[SIMULACIÓN GLOBAL] 📄 {rel_origin} ➔ {new_category}/{dest_file_path.name}")
                moved_count += 1
            else:
                try:
                    target_category_folder.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file_item), str(dest_file_path))
                    print(f"[RE-UBICADO GLOBAL] 📄 {rel_origin} ➔ {new_category}/{dest_file_path.name}")
                    moved_count += 1
                except Exception as e:
                    skipped_count += 1
                    print(f"⚠️  [OMITIDO] {rel_origin} ({e})")

    print("-" * 60)
    print(f"Limpieza profunda completada. Re-ubicados con éxito: {moved_count} | Omitidos: {skipped_count}\n")
    
    # Limpieza automática de carpetas temporales que hayan quedado vacías
    cleanup_empty_folders(target_dir, dry_run=dry_run)


def remove_readonly(func, path, exc_info):
    """Manejador de permisos en Windows para eliminar carpetas con atributo de solo lectura o en uso previo."""
    import stat, os
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def cleanup_empty_folders(target_dir: Path, dry_run: bool = True):
    """
    Elimina carpetas temporales o secundarias que hayan quedado 100% vacías.
    Conserva intactas las carpetas de categorías principales.
    """
    main_categories = set(config.EXTENSION_CATEGORIES.keys()).union(config.get_all_keyword_categories().keys())
    main_categories.add(config.DEFAULT_CATEGORY)
    main_categories.add(getattr(config, "DEFAULT_FOLDER_CATEGORY", "Proyectos_Y_Carpetas"))

    removed_dirs = 0
    try:
        subfolders = [f for f in target_dir.iterdir() if f.is_dir() and f.name not in main_categories and not f.name.startswith(".")]
    except Exception:
        return

    for folder in subfolders:
        try:
            if not any(folder.iterdir()):
                if dry_run:
                    print(f"[SIMULACIÓN] 🗑️  Carpeta vacía detectada: {folder.name} (se eliminaría)")
                else:
                    shutil.rmtree(str(folder), onerror=remove_readonly)
                    print(f"[ELIMINADA CARPETA VACÍA] 🗑️  {folder.name}")
                removed_dirs += 1
        except Exception as e:
            print(f"⚠️  [OMITIDO CARPETA VACÍA] {folder.name}: {e}")


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
