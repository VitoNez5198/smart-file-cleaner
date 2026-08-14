"""
main.py - Punto de entrada del script Smart File Cleaner.
"""

import argparse
from pathlib import Path
import config
from cleaner import organize_folder, export_scan_report

def main():
    parser = argparse.ArgumentParser(description="Smart File Cleaner - Organizador automático de archivos")
    parser.add_argument(
        "--folder",
        type=str,
        default=None,
        help="Ruta personalizada de la carpeta a organizar (por defecto: Descargas)"
    )
    parser.add_argument(
        "--desktop",
        action="store_true",
        help="Organizar la carpeta Escritorio en lugar de Descargas"
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Generar un reporte JSON detallado de inventario (scan_report.json) para análisis con IA"
    )
    parser.add_argument(
        "--real",
        action="store_true",
        help="Ejecutar en MODO REAL (mover los archivos). Por defecto corre en modo simulación (dry-run)."
    )

    args = parser.parse_args()

    print("=" * 55)
    print("         🧹 SMART FILE CLEANER - ORGANIZADOR        ")
    print("=" * 55)

    # Determinar la carpeta objetivo
    if args.folder:
        target = Path(args.folder)
    elif args.desktop:
        target = Path.home() / "Desktop"
    else:
        target = config.TARGET_DIR

    # Si se pide --scan, exportamos el informe para análisis
    if args.scan:
        export_scan_report(target_dir=target, output_file="scan_report.json")
        return

    # Si NO se especifica --real, se mantiene dry_run = True por seguridad
    is_dry_run = not args.real

    organize_folder(target_dir=target, dry_run=is_dry_run)


if __name__ == "__main__":
    main()

