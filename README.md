# Smart File Cleaner 🧹✨

Un organizador automático, portátil e inteligente en Python para limpiar tus carpetas de **Escritorio** y **Descargas**, clasificando archivos sueltos y carpetas de proyectos mediante **patrones de expresiones regulares**, **palabras clave universales** y un **asistente interactivo paso a paso**.

---

## 🌟 Características Principales

- **🤖 Asistente Interactivo por Consola (CLI Wizard)**:
  - Ejecuta el programa con un menú interactivo en bucle.
  - Selecciona fácilmente carpetas (Escritorio, Descargas, rutas personalizadas o subcarpetas existentes).
  - Permite elegir mover **solo archivos**, **solo carpetas de proyectos** o **todo**.
  - **Transición Fluida**: Al terminar la simulación, te ofrece aplicar la migración real inmediatamente sin reiniciar el programa ni cerrar la ventana.

- **🌐 100% Portátil y Universal (Cero Rutas Fijas)**:
  - Detecta automáticamente las carpetas de usuario en cualquier PC (`C:\Users\NombreUsuario\...` o unidades secundarias `D:\...`).
  - Funciona en sistemas Windows tanto en **español** (`Escritorio`/`Descargas`) como en **inglés** (`Desktop`/`Downloads`).
  - Categorías universales adaptadas a cualquier universidad, colegio, instituto o entorno de trabajo.

- **🔍 Motor de Patrones de Expresiones Regulares (Regex)**:
  - Reconoce automáticamente cualquier código de asignatura o ramo (ej: `PRO402`, `SOO301`, `INF101`, `CS101`, `MAT201`).
  - Clasifica de forma inteligente material de estudio (`semana`, `unidad`, `tema`, `taller`, `guia`, `evaluacion`, `tarea`).

- **📁 Soporte Seguro para Carpetas de Proyectos**:
  - Mueve carpetas completas de proyectos o laboratorios de desarrollo a `Proyectos_Y_Carpetas` o la categoría correspondiente.
  - **Protección Total**: Ignora accesos directos del sistema (`.lnk`, `.url`), la propia carpeta del programa (`smart-file-cleaner`) y archivos protegidos del sistema.

- **🛡️ Tolerancia a Fallos y Archivos en Uso**:
  - Si un archivo o carpeta está abierto en Word, Acrobat u otra aplicación, el programa no se cierra; emite una advertencia, omite el elemento en uso y **continúa procesando todo lo demás**.

- **📦 Ejecutable Autónomo (`.exe`) y Acceso Directo (`.bat`)**:
  - Incluye `cleaner.bat` para doble clic rápido.
  - Incluye la compilación binaria `dist/SmartFileCleaner.exe` ejecutable en cualquier equipo sin necesidad de instalar Python.

---

## 📁 Estructura del Proyecto

```text
smart-file-cleaner/
├── cleaner.bat          # Lanzador directo para la terminal de Windows
├── config.py           # Configuración de categorías universales y palabras clave
├── cleaner.py          # Lógica principal de ordenamiento, regex y protección
├── main.py             # Menú interactivo y punto de entrada CLI
├── .gitignore          # Exclusión de ejecutables, datos personales y temporales
└── README.md           # Documentación profesional del proyecto
```

---

## 🚀 Formas de Uso

### 1. Ejecución mediante Doble Clic (Windows)
- Haz **doble clic en `cleaner.bat`** o en el ejecutable `dist/SmartFileCleaner.exe`.
- Se abrirá la consola interactiva con el menú principal.

### 2. Ejecución Interactiva por Terminal
```bash
python main.py
```

### 3. Opciones por Línea de Comandos (Power Users)
```bash
# Simular limpieza del Escritorio redirigida a Descargas (incluyendo carpetas)
python main.py --desktop --to-downloads --include-folders

# Ejecución real en el Escritorio
python main.py --desktop --to-downloads --include-folders --real

# Escanear e inventariar una carpeta en scan_report.json
python main.py --scan --folder "D:\Descargas"
```

---

## ⚙️ Categorías Universales Configuradas (`config.py`)

- **`Postulaciones_CV`** 💼: Currículums, cartas de presentación, logros, elevator pitch.
- **`Material_Estudio_Cursos`** 🎓: Materiales académicos, guías, tareas, ramos universales (`CS101`, `PRO402`, `SOO301`, etc.).
- **`Credenciales_Cloud`** ☁️: Claves SSH, llaves de nube AWS/Azure/GCP (`.pem`, `.ppk`, `labsuser`, `accesskeys`).
- **`Proyectos_Y_Carpetas`** 📁: Carpetas de proyectos de código, laboratorios y repositorios sueltos.
- **`Documentos`** 📄: Archivos `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.csv`, `.md`.
- **`Imagenes`** 🖼️: Formatos estándar y modernos (`.png`, `.jpg`, `.heic`, `.avif`, `.webp`).
- **`Capturas_Pantalla`** 📸: Screenshots y capturas de pantalla.
- **`Instaladores_Software`** ⚙️: Programas `.exe`, `.msi`, `.dmg`, `.deb`, `.vsix`.
- **`Codigo_Notebooks`** 💻: Scripts `.py`, Notebooks `.ipynb`, schemas `.sql`, `.json`.
- **`Archivos_Comprimidos`** 📦: Archivos `.zip`, `.rar`, `.7z`, `.iso`.
- **`Libros_Ebooks`** 📚: Ebooks `.epub`, `.mobi`, `.azw3`.
- **`Video`** 🎥 / **`Audio`** 🎵 / **`Logs_Temporales`** 📝.

---

## 🔒 Privacidad y Seguridad

- **100% Local**: No requiere conexión a internet ni envía datos a servidores externos.
- **Git Security**: El archivo de reporte `scan_report.json`, logs, entorno virtual y compilados `.exe` están estrictamente ignorados en [.gitignore](file:///d:/Escritorio/smart_file_cleaner/smart-file-cleaner/.gitignore).

---

## 📄 Licencia

MIT License - Desarrollado libremente para la comunidad.
