# Smart File Cleaner 🧹✨

Un script automatizado en Python para organizar y limpiar tus carpetas de **Descargas** y **Escritorio** de forma inteligente, clasificando los archivos por palabras clave, contenido e inventario analítico.

---

## 🌟 Características Principales

- **📊 Análisis e Inventario IA (`--scan`)**: Genera un archivo de reporte JSON (`scan_report.json`) con el inventario completo de tus archivos para analizar patrones y proponer categorías a medida.
- **🎯 Filtrado Inteligente por Palabras Clave**: Detecta patrones en el nombre del archivo (ej: `AIEP`, `labsuser`, `cv`, `contrato`, `captura`) y los agrupa en carpetas específicas prioritarias.
- **📂 Organización por Extensiones y Formatos Modernos**: Clasifica archivos en categorías especializadas (Documentos, Imágenes HEIC/AVIF, Notebooks Jupyter `.ipynb`, Credenciales AWS `.pem`/`.ppk`, Libros `.epub`, etc.).
- **🛡️ Modo Simulación Seguro (Dry-Run por defecto)**: Permite previsualizar los cambios en la consola sin modificar ni mover ningún archivo real.
- **🔁 Manejo Automático de Duplicados**: Si ya existe un archivo con el mismo nombre en la carpeta de destino, le asigna un sufijo numérico (`archivo (1).pdf`) evitando sobreescrituras.
- **🚀 Cero Dependencias Externas**: Desarrollado 100% con la librería estándar de Python (`pathlib`, `shutil`, `argparse`, `json`).

---

## 📁 Estructura del Proyecto

```text
smart-file-cleaner/
├── .gitignore          # Filtro de archivos para evitar subir entornos o datos personales
├── config.py           # Configuración de carpetas, extensiones y palabras clave
├── cleaner.py          # Lógica principal de filtrado, escaneo y movimiento
├── main.py             # Interfaz de línea de comandos (CLI)
└── README.md           # Documentación profesional del proyecto
```

---

## 🚀 Guía de Uso

### 1. Escanear e Inventariar la Carpeta (`--scan`)
Genera un reporte JSON con la distribución propuesta de categorías sin mover nada:

```bash
python main.py --scan --folder "D:\Descargas"
```

### 2. Previsualizar cambios (Modo Simulación)
Revisa la simulación en la consola para confirmar qué se movería y dónde:

```bash
python main.py --folder "D:\Descargas"
```

### 3. Ejecutar movimiento real de archivos
Aplica la organización física de archivos agregando `--real`:

```bash
python main.py --folder "D:\Descargas" --real
```

### 4. Organizar el Escritorio
```bash
# Simular en el Escritorio
python main.py --desktop

# Organizar realmente el Escritorio
python main.py --desktop --real
```

---

## ⚙️ Categorías Configuradas (`config.py`)

- **`AIEP_Material_Estudio`**: Guías, evaluaciones, unidades, semestres, tareas (`soo301`, `pro303`, etc.).
- **`AWS_Cloud_Credenciales`**: Claves `.pem`, `.ppk`, accesos de laboratorio de nube (`labsuser`, `accesskeys`).
- **`Postulaciones_CV`**: Currículums, cartas de presentación y logros.
- **`Codigo_Notebooks`**: Scripts `.py`, Notebooks `.ipynb`, schemas `.sql`, `.json`, etc.
- **`Capturas_Pantalla`**: Screenshots de WhatsApp y capturas de pantalla.
- **`Libros_Ebooks`**: Archivos `.epub`, `.mobi`, `.azw3`.
- **`Imagenes`**: Archivos de imagen estándar y modernos (`.jpg`, `.png`, `.heic`, `.avif`).
- **`Documentos`**, **`Video`**, **`Audio`**, **`Instaladores_Software`**, **`Archivos_Comprimidos`**, etc.

---

## 🔒 Privacidad y Seguridad

- **100% Local**: Funciona totalmente sin internet y sin enviar archivos a servidores externos.
- **Protección Git**: El reporte `scan_report.json` e información sensible se encuentran en [.gitignore](file:///d:/Escritorio/smart_file_cleaner/smart-file-cleaner/.gitignore).

---

## 📄 Licencia

MIT License - Desarrollado libremente para la comunidad.
