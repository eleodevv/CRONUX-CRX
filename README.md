# CRONUX-CRX

Sistema de Control de Versiones Local Simple y Poderoso

## Descripción

Cronux-CRX (Cronux Control de Revisiones eXtendido) es un sistema de control de versiones local diseñado para ser simple, rápido y efectivo. Funciona completamente offline, sin necesidad de repositorios remotos o configuraciones complejas.

## Características

- **100% Offline**: Funciona completamente sin conexión a internet
- **Interfaz Gráfica y CLI**: Dos formas de trabajar según tu preferencia
- **Simple y Rápido**: Sin configuraciones complejas
- **Multiplataforma**: Disponible para Windows, macOS y Linux
- **Historial Visual**: Visualiza la evolución de tus proyectos
- **Restauración Fácil**: Vuelve a cualquier versión anterior con un clic

## Instalación

### Instalación Rápida (Linux/macOS)

```bash
# Método 1: Instalación desde la rama principal (recomendado)
curl -fsSL https://raw.githubusercontent.com/eleodevv/CRONUX-CRX/main/cronux_cli/install.sh | bash

# Método 2: Instalación desde tag específico (evita caché)
curl -fsSL https://raw.githubusercontent.com/eleodevv/CRONUX-CRX/v0.2.1/cronux_cli/install.sh | bash

# Verificar instalación
cronux --version
```

**Nota:** Si el instalador muestra una versión anterior (v0.2.0) pero `cronux --version` muestra v0.2.1, es debido al caché de GitHub. Los archivos se instalan correctamente con la versión v0.2.1.

### Desinstalación (Linux/macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/eleodevv/CRONUX-CRX/main/cronux_cli/uninstall.sh | bash
```

### Windows
1. Descarga `CRONUX-CLI-INSTALLER.exe` o `CRONUX-CRX.exe` (GUI)
2. Ejecuta el instalador
3. Sigue las instrucciones en pantalla

### macOS (Alternativa con instalador)
1. Descarga `Cronux-CRX-Installer.pkg` (CLI) o `CRONUX-CRX.dmg` (GUI)
2. Abre el archivo descargado
3. Sigue las instrucciones de instalación

### Linux (Alternativa con .deb)
1. Descarga el archivo `.deb` correspondiente
2. Instala con: `sudo dpkg -i cronux-crx-*.deb`
3. Para CLI: El comando `cronux` estará disponible globalmente
4. Para GUI: Busca "Cronux-CRX" en tu menú de aplicaciones

## Uso Básico

### CLI (Línea de Comandos)

```bash
# Ver ayuda
cronux ayuda

# Modo interactivo (navegación con flechas)
cronux

# Crear un nuevo proyecto
cronux crear "Mi Proyecto"

# Guardar una versión
cronux guardar "Descripción de cambios"

# Ver historial
cronux historial

# Restaurar una versión
cronux restaurar v2

# Eliminar una versión
cronux eliminar-version v3

# Migrar proyecto de v0.1.0 a v0.2.1
cronux migrar

# Ver información del proyecto
cronux info

# Eliminar proyecto
cronux eliminar

# Cambiar entre modo asistido/manual
cronux modo
```

### Características v0.2.1

- ✅ **Versiones con enteros:** 1, 2, 3, 4... (no más 1.0, 1.1, 1.2)
- ✅ **Navegación con flechas:** Menús interactivos sin números
- ✅ **Migración automática:** De v0.1.0 a v0.2.1
- ✅ **Sincronización CLI ↔ UI:** Cambios en tiempo real
- ✅ **File watcher:** Detecta cambios automáticamente

### GUI (Interfaz Gráfica)

1. Abre la aplicación Cronux-CRX
2. Crea un nuevo proyecto o abre uno existente
3. Usa los botones para guardar versiones, ver historial y restaurar
4. **Nuevo:** Botón "Migrar" para actualizar proyectos de v0.1.0

## Estructura del Proyecto

```
CRONUX-CRX/
├── cronux_cli/              # Código fuente de la aplicación
│   ├── cli/                 # Módulos CLI
│   │   ├── cronux_cli.py   # Punto de entrada CLI
│   │   ├── crear_proyecto.py
│   │   ├── guardar_version.py
│   │   ├── restaurar_versiones.py
│   │   ├── ver_historial.py
│   │   ├── info_proyecto.py
│   │   └── eliminar_proyecto.py
│   ├── cronux_gui_v3.py    # Interfaz gráfica
│   ├── build_separated.py   # Script de construcción
│   ├── assets/              # Recursos (iconos, imágenes)
│   ├── uninstall.sh         # Desinstalador Linux/macOS
│   └── uninstall.bat        # Desinstalador Windows
├── cronuxEstatico/          # Sitio web estático
└── README.md
```

## Desarrollo

### Requisitos
- Python 3.8+
- tkinter (incluido en Python)
- Flet
- PyInstaller (para crear ejecutables)

### Construir desde el código fuente

```bash
# Clonar el repositorio
git clone https://github.com/eleowebcoding/CRONUX-CRX.git
cd CRONUX-CRX/cronux_cli

# Instalar dependencias
pip install pyinstaller

# Construir ejecutables
python build_separated.py
```

## Desinstalación

### Windows
```cmd
C:\Program Files\Cronux\uninstall.bat
```

### Linux/macOS
```bash
sudo /usr/local/cronux/uninstall.sh
```

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Sitio Web
https://eleodevv.github.io/cronux/


