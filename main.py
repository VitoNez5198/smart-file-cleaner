"""
main.py - Punto de entrada del script Smart File Cleaner.
"""

from pathlib import Path
import config
from cleaner import organize_folder

def main():
    print("=" * 50)
    print("       SMART FILE CLEANER - ORGANIZADOR        ")
    print("=" * 50)
    
    target = config.TARGET_DIR
    print(f"Carpeta seleccionada: {target}")
    
    # Ejecutamos la función de organización
    organize_folder(target_dir=target, dry_run=True)

if __name__ == "__main__":
    main()
