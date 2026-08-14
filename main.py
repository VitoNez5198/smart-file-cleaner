"""
main.py - Punto de entrada interactivo y CLI para Smart File Cleaner.
"""

import sys
import argparse
from pathlib import Path
import config
from cleaner import organize_folder, deep_organize_folder, export_scan_report

def get_default_downloads() -> Path:
    """Retorna la carpeta de descargas del usuario de forma automática y portátil."""
    custom_downloads = Path("D:/Descargas")
    if custom_downloads.exists():
        return custom_downloads
    
    home = Path.home()
    for folder_name in ["Downloads", "Descargas"]:
        p = home / folder_name
        if p.exists():
            return p
            
    return home / "Downloads"

def get_default_desktop() -> Path:
    """Retorna la carpeta del Escritorio del usuario de forma automática y portátil."""
    custom_desktop = Path("D:/Escritorio")
    if custom_desktop.exists():
        return custom_desktop
        
    home = Path.home()
    for folder_name in ["Desktop", "Escritorio"]:
        p = home / folder_name
        if p.exists():
            return p
            
    return home / "Desktop"

def interactive_wizard():
    """
    Asistente interactivo por consola paso a paso con bucle de menú principal.
    """
    while True:
        print("\n" + "=" * 60)
        print("      🧹 SMART FILE CLEANER - MENÚ PRINCIPAL 🚀    ")
        print("=" * 60)

        # PASO 1: Selección de Carpeta Origen
        print("\n📌 PASO 1: ¿Qué tipo de limpieza deseas realizar?")
        print(f"  [1] 🖥️  Limpiar Escritorio ({get_default_desktop()})")
        print(f"  [2] 📥 Limpiar Descargas ({get_default_downloads()})")
        print("  [3] 📂 Pegar o escribir una ruta personalizada")
        print(f"  [4] 🔄 Re-organizar subcarpeta específica (ej: {get_default_downloads() / 'Documentos'})")
        print(f"  [5] 🌐 LIMPIEZA PROFUNDA GLOBAL (Re-clasificar subcarpetas en {get_default_downloads()})")
        print("  [6] ➕ Crear nueva categoría personalizada (sin tocar código)")
        print("  [0] ❌ Salir del programa")

        choice_origin = input("\n👉 Selecciona una opción (0-6) [Por defecto: 1]: ").strip()
        
        if choice_origin == "0":
            print("\n👋 ¡Gracias por usar Smart File Cleaner! Hasta pronto.\n")
            break

        # Opción 6: Crear nueva categoría personalizada
        if choice_origin == "6":
            print("\n" + "=" * 60)
            print("  ➕ CREAR NUEVA CATEGORÍA PERSONALIZADA")
            print("=" * 60)
            cat_name = input("\n👉 Nombre de la carpeta destino (ej: Trabajo_COMEX): ").strip().replace(" ", "_")
            if not cat_name:
                print("\n❌ Nombre de carpeta inválido.")
                input("\nPresiona ENTER para volver al menú principal...")
                continue

            kws_input = input("👉 Palabras clave separadas por comas (ej: comex, factura, embarque, aduana): ").strip()
            keywords = [k.strip().lower() for k in kws_input.split(",") if k.strip()]

            if not keywords:
                print("\n❌ Debes ingresar al menos una palabra clave.")
                input("\nPresiona ENTER para volver al menú principal...")
                continue

            if config.save_user_category(cat_name, keywords):
                print(f"\n✅ ¡Categoría '{cat_name}' guardada con éxito!")
                print(f"📁 Todos los archivos con ({', '.join(keywords)}) se moverán ahora a '{cat_name}'.")

            input("\nPresiona ENTER para volver al menú principal...")
            continue

        # Si elige la Limpieza Profunda Global (Opción 5)
        if choice_origin == "5":
            target_dir = get_default_downloads()
            print("\n📌 Modo seleccionado: 🌐 LIMPIEZA PROFUNDA GLOBAL")
            print("  [1] 🧪 SIMULACIÓN (Previsualizar qué archivos se re-clasificarían)")
            print("  [2] 🚀 EJECUCIÓN REAL (Re-ubicar archivos físicamente)")

            choice_mode = input("\n👉 Selecciona el modo (1-2) [Por defecto: 1]: ").strip()
            dry_run = False if choice_mode == "2" else True

            try:
                deep_organize_folder(target_dir=target_dir, dry_run=dry_run)
            except Exception as e:
                print(f"\n❌ [ERROR] Falló la limpieza profunda: {e}")

            if dry_run:
                print("-" * 60)
                apply_real = input("\n👉 ¿Deseas aplicar la MIGRACIÓN REAL PROFUNDA ahora? (s/n) [n]: ").strip().lower()
                if apply_real == "s":
                    try:
                        deep_organize_folder(target_dir=target_dir, dry_run=False)
                        print("\n✨ ¡Limpieza profunda real completada con éxito!")
                    except Exception as e:
                        print(f"\n❌ [ERROR] Falló la limpieza profunda real: {e}")

            print("\n" + "=" * 60)
            again = input("👉 ¿Deseas realizar otra operación o volver al menú principal? (s/n) [s]: ").strip().lower()
            if again == "n":
                print("\n👋 ¡Gracias por usar Smart File Cleaner! Hasta pronto.\n")
                break
            continue

        if choice_origin == "2":
            target_dir = get_default_downloads()
        elif choice_origin == "3":
            custom_path = input("\n📋 Pega o escribe la ruta completa de la carpeta: ").strip().strip('"').strip("'")
            target_dir = Path(custom_path)
            if not target_dir.exists():
                print(f"\n❌ [ERROR] La ruta especificada no existe: {target_dir}")
                input("\nPresiona ENTER para volver al menú principal...")
                continue
        elif choice_origin == "4":
            sub_folder = input(f"\n📋 Escribe el nombre de la subcarpeta dentro de Descargas (ej: Documentos): ").strip()
            if not sub_folder:
                sub_folder = "Documentos"
            target_dir = get_default_downloads() / sub_folder
            if not target_dir.exists():
                print(f"\n❌ [ERROR] La subcarpeta no existe: {target_dir}")
                input("\nPresiona ENTER para volver al menú principal...")
                continue
        else:
            target_dir = get_default_desktop()

        # PASO 2: Selección de Destino
        default_dest = get_default_downloads()
        print(f"\n📌 PASO 2: ¿Dónde deseas guardar los archivos organizados?")
        print(f"  [1] 🎯 Almacén Central en Descargas ({default_dest}) [Recomendado para Escritorio]")
        print(f"  [2] 📂 Dentro de la misma carpeta origen ({target_dir})")

        choice_dest = input("\n👉 Selecciona el destino (1-2) [Por defecto: 1]: ").strip()
        dest_dir = default_dest if choice_dest != "2" else target_dir

        # PASO 3: Selección del Tipo de Elementos
        print("\n📌 PASO 3: ¿Qué tipo de elementos deseas mover?")
        print("  [1] 📄 Solo archivos sueltos (PDFs, imágenes, instaladores, etc.)")
        print("  [2] 📁 Solo carpetas (proyectos, laboratorios, subcarpetas)")
        print("  [3] 📦 Archivos Y Carpetas (Limpieza completa)")

        choice_type = input("\n👉 Selecciona una opción (1-3) [Por defecto: 3]: ").strip()
        
        if choice_type == "1":
            include_files, include_folders = True, False
        elif choice_type == "2":
            include_files, include_folders = False, True
        else:
            include_files, include_folders = True, True

        # PASO 4: Selección de Modo (Simulación vs Real)
        print("\n📌 PASO 4: Modo de Operación")
        print("  [1] 🧪 SIMULACIÓN (Recomendado: Previsualiza sin mover nada)")
        print("  [2] 🚀 EJECUCIÓN REAL (Moverá físicamente los archivos y carpetas)")

        choice_mode = input("\n👉 Selecciona el modo (1-2) [Por defecto: 1]: ").strip()
        dry_run = False if choice_mode == "2" else True

        # Confirmación y Resumen
        print("\n" + "-" * 60)
        print("📋 RESUMEN DE LA OPERACIÓN:")
        print(f"  • Carpeta Origen:   {target_dir}")
        print(f"  • Carpeta Destino:  {dest_dir}")
        print(f"  • Archivos:         {'Sí' if include_files else 'No'}")
        print(f"  • Carpetas:         {'Sí' if include_folders else 'No'}")
        print(f"  • Modo Inicial:     {'🧪 Simulación (Dry-Run)' if dry_run else '🚀 EJECUCIÓN REAL'}")
        print("-" * 60)

        if not dry_run:
            confirm = input("\n⚠️  ¿Estás seguro de ejecutar los cambios reales? (s/n) [n]: ").strip().lower()
            if confirm != "s":
                print("\n❌ Operación cancelada por el usuario.")
                input("\nPresiona ENTER para volver al menú principal...")
                continue

        # Ejecutar la limpieza / simulación
        try:
            organize_folder(
                target_dir=target_dir,
                dest_dir=dest_dir,
                dry_run=dry_run,
                include_files=include_files,
                include_folders=include_folders
            )
        except Exception as e:
            print(f"\n❌ [ERROR] Ocurrió un fallo durante el proceso: {e}")
            input("\nPresiona ENTER para volver al menú principal...")
            continue

        # Si fue una simulación, preguntar si desea ejecutar la migración real inmediatamente
        if dry_run:
            print("-" * 60)
            apply_real = input("\n👉 ¿Deseas aplicar la MIGRACIÓN REAL ahora con esta misma configuración? (s/n) [n]: ").strip().lower()
            if apply_real == "s":
                print("\n🚀 Iniciando MIGRACIÓN REAL...")
                try:
                    organize_folder(
                        target_dir=target_dir,
                        dest_dir=dest_dir,
                        dry_run=False,
                        include_files=include_files,
                        include_folders=include_folders
                    )
                    print("\n✨ ¡Migración real completada con éxito!")
                except Exception as e:
                    print(f"\n❌ [ERROR] Falló la migración real: {e}")

        # Preguntar si desea continuar o salir
        print("\n" + "=" * 60)
        again = input("👉 ¿Deseas realizar otra operación o volver al menú principal? (s/n) [s]: ").strip().lower()
        if again == "n":
            print("\n👋 ¡Gracias por usar Smart File Cleaner! Hasta pronto.\n")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Smart File Cleaner - Organiza y limpia automáticamente tu Escritorio y Descargas."
    )
    
    parser.add_argument("-i", "--interactive", action="store_true", help="Abrir el asistente interactivo en consola.")
    parser.add_argument("--folder", type=str, help="Ruta de la carpeta específica a organizar.")
    parser.add_argument("--desktop", action="store_true", help="Organizar la carpeta de Escritorio.")
    parser.add_argument("--to-downloads", action="store_true", help="Redireccionar el destino de la limpieza hacia Descargas.")
    parser.add_argument("--scan", action="store_true", help="Escanea la carpeta e inventaria los archivos en scan_report.json")
    parser.add_argument("--deep", action="store_true", help="Ejecutar limpieza profunda global re-clasificando archivos en subcarpetas.")
    parser.add_argument("--include-folders", action="store_true", help="Incluir carpetas y proyectos en la reorganización.")
    parser.add_argument("--real", action="store_true", help="Ejecutar el movimiento real de archivos (desactiva el modo simulación).")

    args = parser.parse_args()

    if len(sys.argv) == 1 or args.interactive:
        interactive_wizard()
        return

    if args.deep:
        target_dir = Path(args.folder) if args.folder else get_default_downloads()
        deep_organize_folder(target_dir=target_dir, dry_run=not args.real)
        return

    if args.desktop:
        target_dir = get_default_desktop()
    elif args.folder:
        target_dir = Path(args.folder)
    else:
        target_dir = get_default_downloads()

    dest_dir = get_default_downloads() if args.to_downloads else target_dir

    if args.scan:
        export_scan_report(target_dir)
        return

    dry_run = not args.real

    organize_folder(
        target_dir=target_dir,
        dest_dir=dest_dir,
        dry_run=dry_run,
        include_files=True,
        include_folders=args.include_folders
    )

if __name__ == "__main__":
    main()
