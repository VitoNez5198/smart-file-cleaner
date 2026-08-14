# Smart File Cleaner 🧹✨

Un organizador automático, portátil e inteligente en Python para limpiar tus carpetas de **Escritorio** y **Descargas**, clasificando archivos sueltos y carpetas de proyectos mediante **patrones de expresiones regulares**, **palabras clave universales**, **reglas personalizadas sin código** y un **asistente interactivo paso a paso**.

---

## 🌟 Características Principales

- **🤖 Asistente Interactivo por Consola (CLI Wizard)**:
  - Ejecuta el programa con un menú interactivo en bucle.
  - Selecciona fácilmente carpetas (Escritorio, Descargas, rutas personalizadas o subcarpetas existentes).
  - **Transición Fluida**: Al terminar la simulación, te ofrece aplicar la migración real inmediatamente sin reiniciar el programa ni cerrar la ventana.

- **➕ Reglas Personalizadas Dinámicas (Opción [6])**:
  - Permite a cualquier usuario (ej: trabajo en COMEX, salud, finanzas, diseño) **crear sus propias carpetas y palabras clave** directamente desde el menú por consola, **sin tocar una sola línea de código Python**.
  - Se guardan automáticamente en `user_rules.json` con prioridad máxima.

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

- **🧹 Limpieza de Carpetas Vacías Secundarias**:
  - Elimina automáticamente subcarpetas temporales que hayan quedado 100% vacías tras mover sus archivos, manteniendo intactas las carpetas principales de categorías.

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
├── config.py           # Configuración de categorías universales y motor de reglas
├── cleaner.py          # Lógica principal de ordenamiento, regex, limpieza profunda y protección
├── main.py             # Menú interactivo y punto de entrada CLI
├── .gitignore          # Exclusión de ejecutables, datos personales y reglas locales
└── README.md           # Documentación profesional del proyecto
```

---

## 🚀 Formas de Uso

### 1. Ejecución mediante Doble Clic (Windows)
- Haz **doble clic en `cleaner.bat`** o en el ejecutable `dist/SmartFileCleaner.exe`.
- Se abrirá la consola interactiva con el menú principal.

```text
📌 PASO 1: ¿Qué tipo de limpieza deseas realizar?
  [1] 🖥️  Limpiar Escritorio
  [2] 📥 Limpiar Descargas
  [3] 📂 Pegar o escribir una ruta personalizada
  [4] 🔄 Re-organizar subcarpeta específica
  [5] 🌐 LIMPIEZA PROFUNDA GLOBAL (Re-clasificar subcarpetas)
  [6] ➕ Crear nueva categoría personalizada (sin tocar código)
  [0] ❌ Salir del programa
```

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

# Limpieza profunda global
python main.py --deep --real

# Escanear e inventariar una carpeta en scan_report.json
python main.py --scan --folder "D:\Descargas"
```

---

## ⚙️ Categorías Universales e Inteligentes

El programa organiza tus archivos de forma limpia y natural. **Solo creará las carpetas que realmente necesites en tu equipo**:

### 📁 Categorías Generales (Por Tipo de Archivo)
- 📄 **`Documentos`**: PDFs, archivos de Word (`.docx`), planillas Excel (`.xlsx`), presentaciones PowerPoint (`.pptx`), textos y notas.
- 🖼️ **`Imagenes`**: Fotos e imágenes (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.avif`).
- ⚙️ **`Instaladores_Software`**: Programas e instaladores (`.exe`, `.msi`, `.dmg`, `.deb`).
- 📦 **`Archivos_Comprimidos`**: Archivos `.zip`, `.rar`, `.7z`, `.iso`.
- 🎥 **`Video`** / 🎵 **`Audio`**: Archivos multimedia (`.mp4`, `.mp3`, `.wav`, `.mkv`).
- 📚 **`Libros_Ebooks`**: Libros electrónicos (`.epub`, `.mobi`, `.azw3`).
- 📁 **`Proyectos_Y_Carpetas`**: Carpetas sueltas de proyectos o laboratorios.

### ➕ Categorías Personalizadas (Creadas por cada usuario)
- **Opción `[6]` del menú**: Cualquier usuario puede crear sus propias carpetas y palabras clave a medida (ej: `Trabajo_COMEX`, `Finanzas`, `Postulaciones_CV`, `Material_Estudio`) sin tocar código.

---

## 🔒 Privacidad y Seguridad

- **100% Local**: No requiere conexión a internet ni envía datos a servidores externos.
- **Git Security**: El archivo de reporte `scan_report.json`, reglas del usuario `user_rules.json`, logs, entorno virtual y compilados `.exe` están estrictamente ignorados en [.gitignore](.gitignore).

---

## 📄 Licencia

MIT License - Desarrollado libremente para la comunidad.
