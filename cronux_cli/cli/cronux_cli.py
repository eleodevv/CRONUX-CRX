#!/usr/bin/env python3
"""
Cronux-CRX CLI - Sistema de control de versiones local
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from crear_proyecto import crear_proyecto_cli
    from guardar_version import guardar_version_cli
    from ver_historial import ver_historial_cli
    from restaurar_versiones import restaurar_version_cli
    from info_proyecto import info_proyecto
    from funcion_verficar import verificarCronux
    from eliminar_proyecto import eliminar_proyecto_cli
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    sys.exit(1)


# ─────────────────────────────────────────────
#  Configuración del CLI
# ─────────────────────────────────────────────
CONFIG_DIR = Path.home() / ".cronux"
CONFIG_FILE = CONFIG_DIR / "config.json"

def cargar_config():
    """Carga la configuración del CLI"""
    import json
    
    # Crear directorio si no existe
    CONFIG_DIR.mkdir(exist_ok=True)
    
    # Configuración por defecto
    config_default = {
        "modo": "asistido",  # asistido o manual
        "version": "0.2.0"
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
            # Asegurar que tenga todos los campos
            for key, value in config_default.items():
                if key not in config:
                    config[key] = value
            return config
        except:
            return config_default
    else:
        # Crear archivo de configuración
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_default, f, indent=2)
        return config_default

def guardar_config(config):
    """Guarda la configuración del CLI"""
    import json
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def cambiar_modo():
    """Cambia entre modo asistido y manual"""
    config = cargar_config()
    modo_actual = config.get("modo", "asistido")
    
    if modo_actual == "asistido":
        config["modo"] = "manual"
        guardar_config(config)
        ok("Modo cambiado a: Manual (comandos directos)")
        info("Usa 'cronux ayuda' para ver los comandos disponibles")
    else:
        config["modo"] = "asistido"
        guardar_config(config)
        ok("Modo cambiado a: Asistido (navegación con flechas)")
        info("Ejecuta 'cronux' para usar el modo interactivo")
    print()


# ─────────────────────────────────────────────
#  Colores ANSI
# ─────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[36m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    RED     = "\033[31m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"

def c(color, text):
    return f"{color}{text}{Color.RESET}"


# ─────────────────────────────────────────────
#  Splash screen
# ─────────────────────────────────────────────
SPLASH = f"""
{Color.CYAN}{Color.BOLD}
   ██████╗██████╗  ██████╗ ███╗  ██╗██╗   ██╗██╗  ██╗
  ██╔════╝██╔══██╗██╔═══██╗████╗ ██║██║   ██║╚██╗██╔╝
  ██║     ██████╔╝██║   ██║██╔██╗██║██║   ██║ ╚███╔╝ 
  ██║     ██╔══██╗██║   ██║██║╚████║██║   ██║ ██╔██╗ 
  ╚██████╗██║  ██║╚██████╔╝██║ ╚███║╚██████╔╝██╔╝╚██╗
   ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚══╝ ╚═════╝ ╚═╝  ╚═╝
{Color.RESET}{Color.GRAY}              Control de Versiones  v0.2.0{Color.RESET}
"""

# ─────────────────────────────────────────────
#  Iconos por tipo de proyecto
# ─────────────────────────────────────────────
ICONOS_TIPO = {
    "python":       "🐍",
    "javascript":   "📜",
    "nodejs":       "🟢",
    "react":        "⚛️ ",
    "java":         "☕",
    "go":           "🐹",
    "php":          "🐘",
    "ruby":         "💎",
    "flutter":      "💙",
    "dotnet":       "🔷",
    "word":         "📄",
    "excel":        "📊",
    "powerpoint":   "📑",
    "pdf":          "📕",
    "latex":        "📝",
    "documentos":   "📁",
    "imagenes":     "🖼️ ",
    "tareas":       "✅",
    "investigacion":"🔬",
    "diseno":       "🎨",
    "software":     "💻",
    "general":      "📦",
}

def icono_tipo(tipo):
    return ICONOS_TIPO.get(tipo.lower(), "📦")


# ─────────────────────────────────────────────
#  Helpers visuales
# ─────────────────────────────────────────────
def linea(char="─", ancho=52):
    print(c(Color.GRAY, char * ancho))

def ok(msg):
    print(f"  {c(Color.GREEN, '✓')}  {msg}")

def error(msg):
    print(f"  {c(Color.RED, '✗')}  {msg}")

def info(msg):
    print(f"  {c(Color.CYAN, '●')}  {msg}")

def warn(msg):
    print(f"  {c(Color.YELLOW, '⚠')}  {msg}")

def titulo(msg):
    print(f"\n{c(Color.BOLD, msg)}")
    linea()


# ─────────────────────────────────────────────
#  Ayuda
# ─────────────────────────────────────────────
def mostrar_ayuda():
    config = cargar_config()
    modo_actual = config.get("modo", "asistido")
    
    print(SPLASH)
    titulo("COMANDOS DISPONIBLES")
    
    print(f"  {c(Color.GRAY, 'Modo actual:')} {c(Color.CYAN, modo_actual.upper())}")
    print()

    comandos = [
        ("crear  <nombre>",    "Crear un nuevo proyecto"),
        ("guardar <mensaje>",  "Guardar versión actual"),
        ("historial",          "Ver historial de versiones"),
        ("restaurar <v>",      "Restaurar una versión"),
        ("eliminar-version <v>", "Eliminar una versión específica"),
        ("editar-nombre",      "Cambiar el nombre del proyecto"),
        ("info",               "Ver información del proyecto"),
        ("eliminar",           "Eliminar el proyecto"),
        ("modo",               f"Cambiar a modo {'MANUAL' if modo_actual == 'asistido' else 'ASISTIDO'}"),
        ("ayuda",              "Mostrar esta ayuda"),
        ("--version",          "Ver versión del CLI"),
    ]

    for cmd, desc in comandos:
        print(f"  {c(Color.CYAN, f'cronux {cmd:<22}')}{c(Color.GRAY, desc)}")

    print()
    titulo("EJEMPLOS")
    ejemplos = [
        "cronux crear  \"Mi API\"",
        "cronux guardar \"Agregué autenticación\"",
        "cronux historial",
        "cronux restaurar v1.2",
        "cronux info",
        "cronux modo  # Cambiar entre asistido/manual",
    ]
    for ej in ejemplos:
        print(f"  {c(Color.GRAY, '$')} {c(Color.WHITE, ej)}")
    print()


# ─────────────────────────────────────────────
#  Modo interactivo (sin argumentos)
# ─────────────────────────────────────────────
def modo_interactivo():
    """Modo interactivo con navegación por flechas"""
    import sys
    import tty
    import termios
    
    def getch():
        """Lee una tecla sin esperar Enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # Secuencia de escape
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return f'\x1b[{ch3}'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    while True:  # Loop continuo
        en_proyecto = verificarCronux()
        
        # Obtener info del proyecto si estamos en uno
        if en_proyecto:
            import json
            cronux_dir = Path.cwd() / ".cronux"
            proyecto_json = cronux_dir / "proyecto.json"
            nombre = "Proyecto"
            tipo = "general"
            num_versiones = 0

            if proyecto_json.exists():
                with open(proyecto_json) as f:
                    datos = json.load(f)
                nombre = datos.get("nombre", "Proyecto")
                tipo = datos.get("tipo", "general")

            versiones_dir = cronux_dir / "versiones"
            if versiones_dir.exists():
                num_versiones = len(list(versiones_dir.glob("version_*")))

            opciones = [
                ("💾", "Guardar versión"),
                ("📜", "Ver historial"),
                ("⏮️ ", "Restaurar versión"),
                ("ℹ️ ", "Ver información"),
                ("✏️ ", "Editar nombre"),
                ("🗑️ ", "Eliminar versión"),
                ("🗑️ ", "Eliminar proyecto"),
                ("🚪", "Salir"),
            ]
        else:
            nombre = None
            tipo = None
            num_versiones = 0
            opciones = [
                ("🚀", "Crear nuevo proyecto"),
                ("🚪", "Salir"),
            ]
        
        seleccion = 0
        
        def mostrar_menu():
            """Muestra el menú con la selección actual resaltada"""
            print('\033[H', end='')  # Mover cursor al inicio
            print(SPLASH)
            
            if en_proyecto:
                print(f"  {c(Color.BOLD, 'Proyecto:')}  {icono_tipo(tipo)} {c(Color.CYAN, nombre)}")
                print(f"  {c(Color.BOLD, 'Tipo:')}      {tipo}")
                print(f"  {c(Color.BOLD, 'Versiones:')} {num_versiones}")
                linea()
            else:
                warn("No estás en un proyecto Cronux")
                linea()
            
            print()
            print(f"  {c(Color.GRAY, 'Usa ↑/↓ para navegar, Enter para seleccionar')}")
            print()
            
            for i, (ico, label) in enumerate(opciones):
                if i == seleccion:
                    # Opción seleccionada - resaltada
                    print(f"  {c(Color.CYAN + Color.BOLD, '▶')} {ico}  {c(Color.WHITE + Color.BOLD, label)}")
                else:
                    # Opción no seleccionada - gris
                    print(f"    {c(Color.GRAY, ico)}  {c(Color.GRAY, label)}")
            
            print()
        
        # Limpiar pantalla y mostrar menú inicial
        print('\033[2J', end='')  # Limpiar pantalla
        mostrar_menu()
        
        # Loop de navegación
        while True:
            key = getch()
            
            if key == '\x1b[A':  # Flecha arriba
                seleccion = max(0, seleccion - 1)
                mostrar_menu()
            elif key == '\x1b[B':  # Flecha abajo
                seleccion = min(len(opciones) - 1, seleccion + 1)
                mostrar_menu()
            elif key == '\r' or key == '\n':  # Enter
                break
            elif key == '\x1b' or key == '\x03':  # Esc o Ctrl+C
                print(f"\n  {c(Color.GRAY, '¡Hasta pronto! 👋')}\n")
                return

        print()  # Salto de línea después de seleccionar

        # Variable para controlar si debe salir
        debe_salir = False

        if en_proyecto:
            if seleccion == 0:  # Guardar versión
                _cmd_guardar([])
            elif seleccion == 1:  # Ver historial
                _cmd_historial()
            elif seleccion == 2:  # Restaurar versión
                _cmd_restaurar_interactivo()
            elif seleccion == 3:  # Ver información
                _cmd_info()
            elif seleccion == 4:  # Editar nombre
                _cmd_editar_nombre()
            elif seleccion == 5:  # Eliminar versión
                _cmd_eliminar_version_interactivo()
            elif seleccion == 6:  # Eliminar proyecto
                _cmd_eliminar()
                debe_salir = True
            elif seleccion == 7:  # Salir
                debe_salir = True
        else:
            if seleccion == 0:  # Crear nuevo proyecto
                nombre = input(f"  {c(Color.GRAY, 'Nombre del proyecto:')} ").strip()
                if nombre:
                    _cmd_crear(nombre, [])
            elif seleccion == 1:  # Salir
                debe_salir = True

        if debe_salir:
            print(f"  {c(Color.GRAY, '¡Hasta pronto! 👋')}\n")
            break

        # Pausa antes de volver al menú
        print()
        try:
            input(f"  {c(Color.GRAY, 'Presiona Enter para continuar...')}")
        except (KeyboardInterrupt, EOFError):
            print()
            break

        # Limpiar pantalla
        os.system('clear' if os.name != 'nt' else 'cls')


# ─────────────────────────────────────────────
#  Implementación de comandos
# ─────────────────────────────────────────────
def _cmd_crear(nombre, args):
    """Wizard interactivo para crear proyecto con navegación por flechas"""
    import sys
    import tty
    import termios
    
    def getch():
        """Lee una tecla sin esperar Enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # Secuencia de escape
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return f'\x1b[{ch3}'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    categorias = [
        ("💻", "Software",      ["python","javascript","nodejs","react","java","go","php","ruby","flutter","dotnet","general"]),
        ("📁", "Documentos",    ["word","excel","powerpoint","pdf","latex","general"]),
        ("🖼️ ", "Imágenes",     ["imagenes","general"]),
        ("✅", "Tareas",        ["tareas","general"]),
        ("🔬", "Investigación", ["investigacion","general"]),
        ("🎨", "Diseño",        ["diseno","general"]),
    ]
    
    # Seleccionar categoría
    seleccion_cat = 0
    
    def mostrar_categorias():
        print('\033[H', end='')
        print(SPLASH)
        titulo(f"Crear Proyecto: {nombre}")
        print(f"  {c(Color.GRAY, 'Usa ↑/↓ para navegar, Enter para seleccionar, Esc para cancelar')}")
        print()
        
        for i, (ico, label, _) in enumerate(categorias):
            if i == seleccion_cat:
                print(f"  {c(Color.CYAN + Color.BOLD, '▶')} {ico}  {c(Color.WHITE + Color.BOLD, label)}")
            else:
                print(f"    {c(Color.GRAY, ico)}  {c(Color.GRAY, label)}")
        print()
    
    print('\033[2J', end='')
    mostrar_categorias()
    
    while True:
        key = getch()
        if key == '\x1b[A':
            seleccion_cat = max(0, seleccion_cat - 1)
            mostrar_categorias()
        elif key == '\x1b[B':
            seleccion_cat = min(len(categorias) - 1, seleccion_cat + 1)
            mostrar_categorias()
        elif key == '\r' or key == '\n':
            break
        elif key == '\x1b' or key == '\x03':
            print(f"\n  {c(Color.GRAY, 'Operación cancelada')}\n")
            return
    
    ico_cat, label_cat, tipos = categorias[seleccion_cat]
    
    # Seleccionar tipo
    seleccion_tipo = 0
    
    def mostrar_tipos():
        print('\033[H', end='')
        print(SPLASH)
        titulo(f"{ico_cat} {label_cat} — Selecciona el tipo")
        print(f"  {c(Color.GRAY, 'Usa ↑/↓ para navegar, Enter para seleccionar, Esc para cancelar')}")
        print()
        
        for i, t in enumerate(tipos):
            if i == seleccion_tipo:
                print(f"  {c(Color.CYAN + Color.BOLD, '▶')} {icono_tipo(t)}  {c(Color.WHITE + Color.BOLD, t)}")
            else:
                print(f"    {c(Color.GRAY, icono_tipo(t))}  {c(Color.GRAY, t)}")
        print()
    
    print('\033[2J', end='')
    mostrar_tipos()
    
    while True:
        key = getch()
        if key == '\x1b[A':
            seleccion_tipo = max(0, seleccion_tipo - 1)
            mostrar_tipos()
        elif key == '\x1b[B':
            seleccion_tipo = min(len(tipos) - 1, seleccion_tipo + 1)
            mostrar_tipos()
        elif key == '\r' or key == '\n':
            break
        elif key == '\x1b' or key == '\x03':
            print(f"\n  {c(Color.GRAY, 'Operación cancelada')}\n")
            return
    
    tipo = tipos[seleccion_tipo]
    
    print()
    linea()
    info(f"Creando proyecto {c(Color.BOLD, nombre)} ({icono_tipo(tipo)} {tipo})...")
    print()

    exito = crear_proyecto_cli(nombre, tipo)

    print()
    if exito:
        ok(f"Proyecto {c(Color.BOLD, nombre)} creado exitosamente")
        print()
        print(f"  {c(Color.GRAY, 'Próximo paso:')}")
        print(f"  {c(Color.GRAY, '$')} {c(Color.WHITE, 'cronux guardar \"Versión inicial\"')}")
    else:
        error("No se pudo crear el proyecto")
    print()


def _cmd_guardar(args):
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        info("Usa 'cronux crear <nombre>' para crear uno")
        return

    # Obtener mensaje
    if args:
        mensaje = " ".join(args)
    else:
        try:
            mensaje = input(f"  {c(Color.GRAY, 'Mensaje de la versión:')} ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return

    if not mensaje:
        mensaje = "Sin mensaje"

    print()
    info(f"Guardando versión...")
    print()

    exito = guardar_version_cli(mensaje)

    print()
    if exito:
        ok(f"Versión guardada: {c(Color.CYAN, mensaje)}")
    else:
        error("No se pudo guardar la versión")
    print()


def _cmd_historial():
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return

    import json
    cronux_dir = Path.cwd() / ".cronux"
    versiones_dir = cronux_dir / "versiones"

    if not versiones_dir.exists():
        warn("No hay versiones guardadas")
        return

    versiones = list(versiones_dir.glob("version_*"))
    if not versiones:
        warn("No hay versiones guardadas")
        return

    # Leer info del proyecto
    nombre = "Proyecto"
    tipo = "general"
    proyecto_json = cronux_dir / "proyecto.json"
    if proyecto_json.exists():
        with open(proyecto_json) as f:
            datos = json.load(f)
        nombre = datos.get("nombre", "Proyecto")
        tipo = datos.get("tipo", "general")

    titulo(f"{icono_tipo(tipo)} {nombre} — Historial")

    # Ordenar versiones
    versiones_data = []
    for vdir in versiones:
        meta_file = vdir / "metadatos.json"
        if meta_file.exists():
            with open(meta_file) as f:
                meta = json.load(f)
            versiones_data.append(meta)

    versiones_data.sort(key=lambda x: float(str(x["version"]).replace(".", "")), reverse=True)

    for meta in versiones_data:
        v = meta["version"]
        fecha = meta.get("fecha", "")[:16]
        msg = meta.get("mensaje", "Sin mensaje")
        archivos = meta.get("archivos_guardados", 0)
        tamaño = meta.get("tamaño_formateado", "")

        print(f"  {c(Color.CYAN, f'v{v}'):<20} {c(Color.GRAY, fecha)}")
        print(f"  {c(Color.WHITE, msg)}")
        print(f"  {c(Color.GRAY, f'{archivos} archivos  {tamaño}')}")
        linea("·", 52)

    print()


def _cmd_restaurar_interactivo():
    """Selector interactivo para restaurar una versión con navegación por flechas"""
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return
    
    import json
    import sys
    import tty
    import termios
    
    cronux_dir = Path.cwd() / ".cronux"
    versiones_dir = cronux_dir / "versiones"
    proyecto_json = cronux_dir / "proyecto.json"
    
    if not versiones_dir.exists():
        error("No hay versiones guardadas")
        return
    
    # Obtener todas las versiones
    versiones = []
    for v_dir in sorted(versiones_dir.glob("version_*")):
        try:
            num = float(v_dir.name.replace("version_", ""))
            meta_file = v_dir / "metadatos.json"
            if meta_file.exists():
                with open(meta_file) as f:
                    meta = json.load(f)
                versiones.append((num, meta))
        except:
            continue
    
    if not versiones:
        error("No hay versiones guardadas")
        return
    
    # Leer versión actual
    version_actual = 1
    try:
        with open(proyecto_json) as f:
            datos = json.load(f)
        version_actual = float(datos.get("version_actual", 1))
    except:
        pass
    
    print()
    titulo("Selecciona la versión a restaurar")
    print(f"  {c(Color.GRAY, 'Usa ↑/↓ para navegar, Enter para seleccionar, Esc para cancelar')}")
    print()
    
    seleccion = 0
    
    def getch():
        """Lee una tecla sin esperar Enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # Secuencia de escape
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return f'\x1b[{ch3}'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def mostrar_opciones():
        """Muestra las opciones con la selección actual resaltada"""
        # Mover cursor al inicio
        print('\033[H', end='')
        
        print(SPLASH)
        titulo("Selecciona la versión a restaurar")
        print(f"  {c(Color.GRAY, 'Usa ↑/↓ para navegar, Enter para seleccionar, Esc para cancelar')}")
        print()
        
        for i, (num, meta) in enumerate(versiones):
            descripcion = meta.get("mensaje", "Sin descripción")
            fecha = meta.get("fecha", "")[:10] if meta.get("fecha") else ""
            es_actual = (num == version_actual)
            
            if i == seleccion:
                # Opción seleccionada - resaltada en cyan
                badge_actual = f" {c(Color.GREEN, '[ACTUAL]')}" if es_actual else ""
                print(f"  {c(Color.CYAN + Color.BOLD, '▶')} {c(Color.CYAN + Color.BOLD, f'v{num}')}{badge_actual}  {c(Color.WHITE, descripcion)}  {c(Color.GRAY, fecha)}")
            else:
                # Opción no seleccionada - gris
                badge_actual = f" {c(Color.DIM, '[ACTUAL]')}" if es_actual else ""
                print(f"    {c(Color.GRAY, f'v{num}')}{badge_actual}  {c(Color.GRAY, descripcion)}  {c(Color.DIM, fecha)}")
        
        print()
    
    # Limpiar pantalla y mostrar opciones iniciales
    print('\033[2J', end='')  # Limpiar pantalla
    mostrar_opciones()
    
    # Loop de navegación
    while True:
        key = getch()
        
        if key == '\x1b[A':  # Flecha arriba
            seleccion = max(0, seleccion - 1)
            mostrar_opciones()
        elif key == '\x1b[B':  # Flecha abajo
            seleccion = min(len(versiones) - 1, seleccion + 1)
            mostrar_opciones()
        elif key == '\r' or key == '\n':  # Enter
            break
        elif key == '\x1b' or key == '\x03':  # Esc o Ctrl+C
            print(f"\n  {c(Color.GRAY, 'Operación cancelada')}\n")
            return
    
    # Versión seleccionada
    numero_version, meta = versiones[seleccion]
    
    print()
    warn(f"Restaurar versión {c(Color.BOLD, f'v{numero_version}')} reemplazará los archivos actuales")
    print()
    
    try:
        confirmar = input(f"  {c(Color.GRAY, '¿Confirmar? (s/n):')} ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return
    
    if confirmar != 's':
        info("Operación cancelada")
        return
    
    print()
    info("Restaurando versión...")
    print()
    
    def progreso(msg):
        print(f"  {c(Color.GRAY, '→')} {msg}")
    
    exito = restaurar_version_cli(str(numero_version), auto_instalar=True, callback_progreso=progreso)
    
    print()
    if exito:
        ok(f"Versión {c(Color.CYAN, f'v{numero_version}')} restaurada exitosamente")
    else:
        error("No se pudo restaurar la versión")
    print()


def _cmd_editar_nombre():
    """Editar el nombre del proyecto"""
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return
    
    import json
    
    cronux_dir = Path.cwd() / ".cronux"
    proyecto_json = cronux_dir / "proyecto.json"
    
    if not proyecto_json.exists():
        error("No se encontró el archivo proyecto.json")
        return
    
    try:
        with open(proyecto_json) as f:
            datos = json.load(f)
        
        nombre_actual = datos.get("nombre", "Sin nombre")
        
        print()
        titulo("Editar nombre del proyecto")
        print(f"  {c(Color.GRAY, 'Nombre actual:')} {c(Color.CYAN, nombre_actual)}")
        print()
        
        nuevo_nombre = input(f"  {c(Color.GRAY, 'Nuevo nombre (Enter para cancelar):')} ").strip()
        
        if not nuevo_nombre:
            info("Operación cancelada")
            return
        
        datos["nombre"] = nuevo_nombre
        
        with open(proyecto_json, "w") as f:
            json.dump(datos, f, indent=2)
        
        print()
        ok(f"Nombre actualizado: {c(Color.CYAN, nuevo_nombre)}")
    except Exception as e:
        error(f"Error al editar nombre: {e}")
    print()


def _cmd_restaurar(version):
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return

    # Limpiar 'v' si viene incluida
    version = version.lstrip("v")

    print()
    warn(f"Restaurar versión {c(Color.BOLD, f'v{version}')} reemplazará los archivos actuales")
    print()

    try:
        confirmar = input(f"  {c(Color.GRAY, '¿Confirmas? (s/N):')} ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if confirmar not in ["s", "si", "sí", "y", "yes"]:
        info("Operación cancelada")
        return

    print()
    info("Restaurando versión...")
    print()

    def progreso(msg):
        print(f"  {c(Color.GRAY, '→')} {msg}")

    exito = restaurar_version_cli(version, auto_instalar=True, callback_progreso=progreso)

    print()
    if exito:
        ok(f"Versión {c(Color.CYAN, f'v{version}')} restaurada exitosamente")
    else:
        error("No se pudo restaurar la versión")
    print()


def _cmd_info():
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return

    import json
    cronux_dir = Path.cwd() / ".cronux"
    proyecto_json = cronux_dir / "proyecto.json"

    if not proyecto_json.exists():
        error("No se pudo leer la información del proyecto")
        return

    with open(proyecto_json) as f:
        datos = json.load(f)

    nombre = datos.get("nombre", "Sin nombre")
    tipo = datos.get("tipo", "general")
    fecha = datos.get("fecha_creacion", "Desconocida")

    versiones_dir = cronux_dir / "versiones"
    num_versiones = 0
    ultima = "-"
    if versiones_dir.exists():
        versiones = list(versiones_dir.glob("version_*"))
        num_versiones = len(versiones)
        if versiones:
            nums = []
            for v in versiones:
                try:
                    nums.append(float(v.name.replace("version_", "")))
                except:
                    pass
            if nums:
                ultima = str(max(nums)).rstrip("0").rstrip(".")

    titulo(f"{icono_tipo(tipo)} {nombre}")
    print(f"  {c(Color.GRAY, 'Tipo:')}       {tipo}")
    print(f"  {c(Color.GRAY, 'Ubicación:')}  {Path.cwd()}")
    print(f"  {c(Color.GRAY, 'Creado:')}     {fecha}")
    print(f"  {c(Color.GRAY, 'Versiones:')}  {num_versiones}")
    print(f"  {c(Color.GRAY, 'Última v:')}   v{ultima}")
    print()


def _cmd_eliminar_version_interactivo():
    """Selector interactivo para eliminar una versión con navegación por flechas"""
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return
    
    import json
    import shutil
    import sys
    import tty
    import termios
    
    cronux_dir = Path.cwd() / ".cronux"
    versiones_dir = cronux_dir / "versiones"
    proyecto_json = cronux_dir / "proyecto.json"
    
    if not versiones_dir.exists():
        error("No hay versiones guardadas")
        return
    
    # Obtener todas las versiones excepto la 1
    versiones = []
    for v_dir in sorted(versiones_dir.glob("version_*")):
        try:
            num = float(v_dir.name.replace("version_", ""))
            if num > 1:  # Excluir versión 1
                meta_file = v_dir / "metadatos.json"
                if meta_file.exists():
                    with open(meta_file) as f:
                        meta = json.load(f)
                    versiones.append((num, meta))
        except:
            continue
    
    if not versiones:
        error("No hay versiones disponibles para eliminar (la v1 no se puede eliminar)")
        return
    
    # Leer versión actual
    version_actual = 1
    try:
        with open(proyecto_json) as f:
            datos = json.load(f)
        version_actual = float(datos.get("version_actual", 1))
    except:
        pass
    
    print()
    titulo("Selecciona la versión a eliminar")
    print(f"  {c(Color.GRAY, 'Usa ↑/↓ para navegar, Enter para seleccionar, Esc para cancelar')}")
    print()
    
    seleccion = 0
    
    def getch():
        """Lee una tecla sin esperar Enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # Secuencia de escape
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return f'\x1b[{ch3}'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def mostrar_opciones():
        """Muestra las opciones con la selección actual resaltada"""
        # Mover cursor al inicio
        print('\033[H', end='')
        
        print(SPLASH)
        titulo("Selecciona la versión a eliminar")
        print(f"  {c(Color.GRAY, 'Usa ↑/↓ para navegar, Enter para seleccionar, Esc para cancelar')}")
        print()
        
        for i, (num, meta) in enumerate(versiones):
            descripcion = meta.get("mensaje", "Sin descripción")
            fecha = meta.get("fecha", "")[:10] if meta.get("fecha") else ""
            es_actual = (num == version_actual)
            
            if i == seleccion:
                # Opción seleccionada - resaltada en cyan
                badge_actual = f" {c(Color.RED, '[ACTUAL]')}" if es_actual else ""
                print(f"  {c(Color.CYAN + Color.BOLD, '▶')} {c(Color.CYAN + Color.BOLD, f'v{num}')}{badge_actual}  {c(Color.WHITE, descripcion)}  {c(Color.GRAY, fecha)}")
            else:
                # Opción no seleccionada - gris
                badge_actual = f" {c(Color.DIM, '[ACTUAL]')}" if es_actual else ""
                print(f"    {c(Color.GRAY, f'v{num}')}{badge_actual}  {c(Color.GRAY, descripcion)}  {c(Color.DIM, fecha)}")
        
        print()
    
    # Limpiar pantalla y mostrar opciones iniciales
    print('\033[2J', end='')  # Limpiar pantalla
    mostrar_opciones()
    
    # Loop de navegación
    while True:
        key = getch()
        
        if key == '\x1b[A':  # Flecha arriba
            seleccion = max(0, seleccion - 1)
            mostrar_opciones()
        elif key == '\x1b[B':  # Flecha abajo
            seleccion = min(len(versiones) - 1, seleccion + 1)
            mostrar_opciones()
        elif key == '\r' or key == '\n':  # Enter
            break
        elif key == '\x1b' or key == '\x03':  # Esc o Ctrl+C
            print(f"\n  {c(Color.GRAY, 'Operación cancelada')}\n")
            return
    
    # Versión seleccionada
    numero_version, meta = versiones[seleccion]
    
    print()
    warn(f"Esto eliminará la versión {c(Color.BOLD, f'v{numero_version}')}")
    if numero_version == version_actual:
        warn(f"Esta es la versión {c(Color.RED, 'ACTUAL')} - se restaurará automáticamente la versión anterior")
    warn("Las versiones posteriores se renumerarán automáticamente")
    print()
    
    try:
        confirmar = input(f"  {c(Color.GRAY, '¿Continuar? (s/n):')} ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return
    
    if confirmar != 's':
        info("Operación cancelada")
        return
    
    # Si se elimina la versión actual, restaurar la anterior
    debe_restaurar = (numero_version == version_actual)
    version_a_restaurar = None
    
    if debe_restaurar:
        # Buscar la versión anterior
        versiones_disponibles = sorted([float(v_dir.name.replace("version_", "")) 
                                       for v_dir in versiones_dir.glob("version_*")
                                       if float(v_dir.name.replace("version_", "")) != numero_version])
        if versiones_disponibles:
            version_a_restaurar = versiones_disponibles[-1]  # La más reciente que no sea la actual
        else:
            version_a_restaurar = 1  # Fallback a v1
    
    # Eliminar versión
    try:
        version_dir = versiones_dir / f"version_{numero_version}"
        if version_dir.exists():
            shutil.rmtree(version_dir)
        
        # Renumerar versiones posteriores (decrementar en 1)
        versiones_posteriores = []
        for v_dir in sorted(versiones_dir.glob("version_*")):
            try:
                num = int(float(v_dir.name.replace("version_", "")))
                if num > int(numero_version):
                    versiones_posteriores.append((num, v_dir))
            except:
                continue
        
        # Renumerar usando directorio temporal para evitar conflictos
        import tempfile
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            # Mover a temporal
            temp_mapping = []
            for num_viejo, v_dir in versiones_posteriores:
                temp_path = temp_dir / f"version_{num_viejo}"
                shutil.move(str(v_dir), str(temp_path))
                temp_mapping.append((num_viejo, temp_path))
            
            # Mover de temporal a destino con nuevo número
            for num_viejo, temp_path in temp_mapping:
                num_nuevo = num_viejo - 1
                nuevo_nombre = versiones_dir / f"version_{num_nuevo}"
                shutil.move(str(temp_path), str(nuevo_nombre))
                
                # Actualizar metadata
                meta_file = nuevo_nombre / "metadatos.json"
                if meta_file.exists():
                    with open(meta_file) as f:
                        meta = json.load(f)
                    meta["version"] = num_nuevo
                    with open(meta_file, "w") as f:
                        json.dump(meta, f, indent=2)
        finally:
            # Limpiar directorio temporal
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        
        print()
        ok(f"Versión {c(Color.BOLD, f'v{numero_version}')} eliminada")
        info("Las versiones posteriores han sido renumeradas")
        
        # Restaurar versión anterior si era la actual
        if debe_restaurar and version_a_restaurar:
            print()
            info(f"Restaurando versión {c(Color.CYAN, f'v{version_a_restaurar}')}...")
            print()
            
            def progreso(msg):
                print(f"  {c(Color.GRAY, '→')} {msg}")
            
            exito = restaurar_version_cli(str(version_a_restaurar), auto_instalar=True, callback_progreso=progreso)
            
            if exito:
                print()
                ok(f"Versión {c(Color.CYAN, f'v{version_a_restaurar}')} restaurada como actual")
            else:
                error("No se pudo restaurar la versión anterior")
        
    except Exception as e:
        error(f"Error al eliminar versión: {e}")
    print()


def _cmd_eliminar_version(numero_version_str):
    """Elimina una versión específica (para uso desde línea de comandos)"""
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return
    
    import json
    import shutil
    
    try:
        numero_version = float(numero_version_str.replace("v", "").replace("V", ""))
    except ValueError:
        error(f"Versión inválida: {numero_version_str}")
        return
    
    # Proteger versión 1
    if numero_version == 1:
        error("No se puede eliminar la versión 1 (versión original)")
        return
    
    cronux_dir = Path.cwd() / ".cronux"
    versiones_dir = cronux_dir / "versiones"
    version_dir = versiones_dir / f"version_{numero_version}"
    
    if not version_dir.exists():
        error(f"La versión v{numero_version} no existe")
        return
    
    print()
    warn(f"Esto eliminará la versión {c(Color.BOLD, f'v{numero_version}')}")
    warn("Las versiones posteriores se renumerarán automáticamente")
    print()
    
    try:
        confirmar = input(f"  {c(Color.GRAY, '¿Continuar? (s/n):')} ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return
    
    if confirmar != 's':
        info("Operación cancelada")
        return
    
    try:
        shutil.rmtree(version_dir)
        
        # Renumerar versiones posteriores (decrementar en 1)
        versiones_posteriores = []
        for v_dir in sorted(versiones_dir.glob("version_*")):
            try:
                num = int(float(v_dir.name.replace("version_", "")))
                if num > int(numero_version):
                    versiones_posteriores.append((num, v_dir))
            except:
                continue
        
        # Renumerar usando directorio temporal para evitar conflictos
        import tempfile
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            # Mover a temporal
            temp_mapping = []
            for num_viejo, v_dir in versiones_posteriores:
                temp_path = temp_dir / f"version_{num_viejo}"
                shutil.move(str(v_dir), str(temp_path))
                temp_mapping.append((num_viejo, temp_path))
            
            # Mover de temporal a destino con nuevo número
            for num_viejo, temp_path in temp_mapping:
                num_nuevo = num_viejo - 1
                nuevo_nombre = versiones_dir / f"version_{num_nuevo}"
                shutil.move(str(temp_path), str(nuevo_nombre))
                
                # Actualizar metadata
                meta_file = nuevo_nombre / "metadatos.json"
                if meta_file.exists():
                    with open(meta_file) as f:
                        meta = json.load(f)
                    meta["version"] = num_nuevo
                    with open(meta_file, "w") as f:
                        json.dump(meta, f, indent=2)
        finally:
            # Limpiar directorio temporal
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        
        print()
        ok(f"Versión {c(Color.BOLD, f'v{numero_version}')} eliminada")
        info("Las versiones posteriores han sido renumeradas")
    except Exception as e:
        error(f"Error al eliminar versión: {e}")
    print()
    print()


def _cmd_eliminar():
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return

    import json
    cronux_dir = Path.cwd() / ".cronux"
    proyecto_json = cronux_dir / "proyecto.json"
    nombre = "Proyecto"
    if proyecto_json.exists():
        with open(proyecto_json) as f:
            datos = json.load(f)
        nombre = datos.get("nombre", "Proyecto")

    print()
    warn(f"Esto eliminará {c(Color.BOLD, nombre)} y todas sus versiones")
    warn("Los archivos actuales del proyecto NO se eliminarán")
    print()

    try:
        confirmar = input(f"  {c(Color.GRAY, f'Escribe el nombre del proyecto para confirmar:')} ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if confirmar != nombre:
        error("El nombre no coincide. Operación cancelada")
        return

    import shutil
    try:
        shutil.rmtree(cronux_dir)
        print()
        ok(f"Proyecto {c(Color.BOLD, nombre)} eliminado")
        info("Los archivos del proyecto siguen intactos")
    except Exception as e:
        error(f"Error al eliminar: {e}")
    print()


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
def main():
    # Cargar configuración
    config = cargar_config()
    modo = config.get("modo", "asistido")
    
    if len(sys.argv) < 2:
        # Sin argumentos - verificar modo
        if modo == "asistido":
            modo_interactivo()
        else:
            # Modo manual - mostrar ayuda
            mostrar_ayuda()
        return

    comando = sys.argv[1].lower()
    resto = sys.argv[2:]

    try:
        if comando in ["ayuda", "help", "--help", "-h"]:
            mostrar_ayuda()

        elif comando in ["--version", "-v"]:
            print(f"\n  {c(Color.CYAN, 'Cronux-CRX')} v0.2.0  —  Control de Versiones Local\n")

        elif comando in ["modo", "mode"]:
            cambiar_modo()

        elif comando in ["crear", "iniciar", "new", "init"]:
            if not resto:
                error("Se requiere el nombre del proyecto")
                info("Uso: cronux crear \"Mi Proyecto\"")
                sys.exit(1)
            nombre = " ".join(resto)
            _cmd_crear(nombre, [])

        elif comando in ["guardar", "save", "commit"]:
            _cmd_guardar(resto)

        elif comando in ["historial", "log", "ver"]:
            _cmd_historial()

        elif comando in ["restaurar", "restore", "volver", "checkout"]:
            if not resto:
                error("Se requiere el número de versión")
                info("Uso: cronux restaurar v1.2")
                sys.exit(1)
            _cmd_restaurar(resto[0])

        elif comando in ["eliminar-version", "borrar-version", "delete-version"]:
            if not resto:
                error("Se requiere el número de versión")
                info("Uso: cronux eliminar-version v1.2")
                sys.exit(1)
            _cmd_eliminar_version(resto[0])

        elif comando in ["editar-nombre", "renombrar", "rename"]:
            _cmd_editar_nombre()

        elif comando in ["info", "estado", "status"]:
            _cmd_info()

        elif comando in ["eliminar", "borrar", "delete", "fin"]:
            _cmd_eliminar()

        else:
            error(f"Comando desconocido: '{comando}'")
            info("Usa 'cronux ayuda' para ver los comandos disponibles")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n  {c(Color.GRAY, 'Operación cancelada')}\n")
        sys.exit(0)
    except Exception as e:
        error(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
