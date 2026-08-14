# Smart File Cleaner 🧹✨

Un script automatizado en Python para organizar y limpiar tus carpetas de **Descargas** y **Escritorio** de forma inteligente, clasificando los archivos por palabras clave y extensiones.

---

## 🌟 Características Principales

- **🎯 Filtrado Inteligente por Palabras Clave**: Detecta patrones en el nombre del archivo (ejemplo: `cv`, `aiep`, `contrato`) y los agrupa en carpetas prioritarias antes de evaluar la extensión.
- **📂 Organización por Extensiones**: Clasifica los archivos restantes en categorías estándar (Documentos, Imágenes, Instaladores, Código, Audio, Video, etc.).
- **🛡️ Modo Simulación Seguro (Dry-Run por defecto)**: Permite previsualizar los cambios en la consola sin modificar ni mover ningún archivo real.
- **🔁 Manejo Automático de Duplicados**: Si ya existe un archivo con el mismo nombre en la carpeta de destino, le asigna un sufijo numérico (`archivo (1).pdf`) para evitar sobreescrituras accidentales.
- **🚀 Cero Dependencias Externas**: Desarrollado 100% con la librería estándar de Python (`pathlib`, `shutil`, `argparse`).

---

## 📁 Estructura del Proyecto

```text
smart-file-cleaner/
├── .gitignore          # Filtro de archivos para evitar subir entornos o datos personales
├── config.py           # Configuración de carpetas, extensiones y palabras clave
├── cleaner.py          # Lógica principal de filtrado y movimiento de archivos
├── main.py             # Interfaz de línea de comandos (CLI) y ejecutable
└── README.md           # Documentación profesional del proyecto
```

---

## 💻 Requisitos

- **Python 3.8+** (No requiere instalar paquetes adicionales vía `pip`).

---

## 🚀 Guía de Uso

### 1. Previsualizar cambios (Modo Simulación - Recomendado)
Por defecto, el script se ejecuta en **Modo Simulación** para que revises la vista previa sin mover nada:

```bash
python main.py
```

### 2. Ejecutar movimiento real de archivos
Para aplicar la organización real en tu carpeta de Descargas, añade la bandera `--real`:

```bash
python main.py --real
```

### 3. Organizar el Escritorio en lugar de Descargas
Puedes indicar que aplique la limpieza sobre tu Escritorio usando `--desktop`:

```bash
# Simular en el Escritorio
python main.py --desktop

# Mover realmente los archivos del Escritorio
python main.py --desktop --real
```

### 4. Organizar cualquier carpeta personalizada
```bash
python main.py --folder "C:\Ruta\A\Tu\Carpeta" --real
```

---

## ⚙️ Personalización (`config.py`)

Puedes adaptar las categorías a tus necesidades editando `config.py`:

- **Añadir nuevas Palabras Clave**:
  ```python
  KEYWORD_CATEGORIES = {
      "Postulaciones_CV": ["cv", "curriculum", "resume"],
      "AIEP": ["aiep", "tarea", "evaluacion", "clase"],
      "Contratos_Legales": ["contrato", "acuerdo", "firma", "finiquito"],
      "Proyectos_Web": ["portfolio", "wireframe", "diseño"]
  }
  ```

- **Añadir nuevas Extensiones**:
  ```python
  EXTENSION_CATEGORIES = {
      "Documentos": [".pdf", ".docx", ".xlsx", ".epub"],
      "Diseño": [".psd", ".ai", ".fig"]
  }
  ```

---

## 🔒 Privacidad y Seguridad

- **100% Local**: No requiere conexión a internet ni envía datos a servidores externos.
- **Filtros .gitignore**: Diseñado desde el primer paso para proteger archivos locales, registros e información privada.

---

## 📄 Licencia

MIT License - Desarrollado libremente para la comunidad.
