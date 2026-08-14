"""
main.py - Punto de entrada interactivo y CLI para Smart File Cleaner.
"""

import sys
import argparse
from pathlib import Path
import config
from cleaner import organize_folder, export_scan_report

def get_default_downloads() -> Path:
    """Retorna la carpeta de descargas del usuario de forma automática y portátil."""
    # 1. Probar unidad secundaria D:\Descargas si existe
    custom_downloads = Path("D:/Descargas")
    if custom_downloads.exists():
        return custom_downloads
    
    # 2. Buscar en la carpeta del usuario actual (soporta Windows en español/inglés)
    home = Path.home()
    for folder_name in ["Downloads", "Descargas"]:
        p = home / folder_name
        if p.exists():
            return p
            
    return home / "Downloads"

def get_default_desktop() -> Path:
    """Retorna la carpeta del Escritorio del usuario de forma automática y portátil."""
    # 1. Probar unidad secundaria D:\Escritorio si existe
    custom_desktop = Path("D:/Escritorio")
    if custom_desktop.exists():
        return custom_desktop
        
    # 2. Buscar en la carpeta del usuario actual (soporta Windows en español/inglés)
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
        print("\n📌 PASO 1: ¿Qué carpeta deseas limpiar u organizar?")
        print(f"  [1] 🖥️  Escritorio ({get_default_desktop()})")
        print(f"  [2] 📥 Descargas ({get_default_downloads()})")
        print("  [3] 📂 Pegar o escribir una ruta personalizada")
        print("  [0] ❌ Salir del programa")

        choice_origin = input("\n👉 Selecciona una opción (0-3) [Por defecto: 1]: ").strip()
        
        if choice_origin == "0":
            print("\n👋 ¡Gracias por usar Smart File Cleaner! Hasta pronto.\n")
            break

        if choice_origin == "2":
            target_dir = get_default_downloads()
        elif choice_origin == "3":
            custom_path = input("\n📋 Pega o escribe la ruta completa de la carpeta: ").strip().strip('"').strip("'")
            target_dir = Path(custom_path)
            if not target_dir.exists():
                print(f"\n❌ [ERROR] La ruta especificada no existe: {target_dir}")
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
    parser.add_argument("--include-folders", action="store_true", help="Incluir carpetas y proyectos en la reorganización.")
    parser.add_argument("--real", action="store_true", help="Ejecutar el movimiento real de archivos (desactiva el modo simulación).")

    args = parser.parse_args()

    # Si se invoca sin argumentos o con -i, lanzamos el asistente interactivo
    if len(sys.argv) == 1 or args.interactive:
        interactive_wizard()
        return

    # Determinar la carpeta a procesar por CLI
    if args.desktop:
        target_dir = get_default_desktop()
    elif args.folder:
        target_dir = Path(args.folder)
    else:
        target_dir = get_default_downloads()

    # Determinar el destino
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
