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
    print(SPLASH)
    titulo("COMANDOS DISPONIBLES")

    comandos = [
        ("crear  <nombre>",    "Crear un nuevo proyecto"),
        ("guardar <mensaje>",  "Guardar versión actual"),
        ("historial",          "Ver historial de versiones"),
        ("restaurar <v>",      "Restaurar una versión"),
        ("eliminar-version <v>", "Eliminar una versión específica"),
        ("info",               "Ver información del proyecto"),
        ("eliminar",           "Eliminar el proyecto"),
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
    ]
    for ej in ejemplos:
        print(f"  {c(Color.GRAY, '$')} {c(Color.WHITE, ej)}")
    print()


# ─────────────────────────────────────────────
#  Modo interactivo (sin argumentos)
# ─────────────────────────────────────────────
def modo_interactivo():
    while True:  # Loop continuo
        print(SPLASH)

        en_proyecto = verificarCronux()

        if en_proyecto:
            # Leer info del proyecto
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

            print(f"  {c(Color.BOLD, 'Proyecto:')}  {icono_tipo(tipo)} {c(Color.CYAN, nombre)}")
            print(f"  {c(Color.BOLD, 'Tipo:')}      {tipo}")
            print(f"  {c(Color.BOLD, 'Versiones:')} {num_versiones}")
            linea()
            print()

            opciones = [
                ("💾", "Guardar versión"),
                ("📜", "Ver historial"),
                ("⏮️ ", "Restaurar versión"),
                ("ℹ️ ", "Ver información"),
                ("🗑️ ", "Eliminar proyecto"),
                ("🚪", "Salir"),
            ]
        else:
            warn("No estás en un proyecto Cronux")
            print()
            opciones = [
                ("🚀", "Crear nuevo proyecto"),
                ("🚪", "Salir"),
            ]

        for i, (ico, label) in enumerate(opciones, 1):
            print(f"  {c(Color.CYAN, str(i) + '.')} {ico}  {label}")

        print()
        try:
            eleccion = input(f"  {c(Color.GRAY, 'Selecciona una opción:')} ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break  # Salir del loop

        print()

        # Variable para controlar si debe salir
        debe_salir = False

        if en_proyecto:
            if eleccion == "1":
                _cmd_guardar([])
            elif eleccion == "2":
                _cmd_historial()
            elif eleccion == "3":
                version = input(f"  {c(Color.GRAY, 'Número de versión a restaurar:')} ").strip()
                if version:
                    _cmd_restaurar(version)
            elif eleccion == "4":
                _cmd_info()
            elif eleccion == "5":
                _cmd_eliminar()
                # Después de eliminar, salir porque ya no hay proyecto
                debe_salir = True
            elif eleccion == "6":
                debe_salir = True  # Opción "Salir"
        else:
            if eleccion == "1":
                nombre = input(f"  {c(Color.GRAY, 'Nombre del proyecto:')} ").strip()
                if nombre:
                    _cmd_crear(nombre, [])
            elif eleccion == "2":
                debe_salir = True  # Opción "Salir"

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

        # Limpiar pantalla (opcional)
        os.system('clear' if os.name != 'nt' else 'cls')


# ─────────────────────────────────────────────
#  Implementación de comandos
# ─────────────────────────────────────────────
def _cmd_crear(nombre, args):
    """Wizard interactivo para crear proyecto"""
    print(SPLASH)
    titulo(f"Crear Proyecto: {nombre}")

    categorias = [
        ("💻", "Software",      ["python","javascript","nodejs","react","java","go","php","ruby","flutter","dotnet","general"]),
        ("📁", "Documentos",    ["word","excel","powerpoint","pdf","latex","general"]),
        ("🖼️ ", "Imágenes",     ["imagenes","general"]),
        ("✅", "Tareas",        ["tareas","general"]),
        ("🔬", "Investigación", ["investigacion","general"]),
        ("🎨", "Diseño",        ["diseno","general"]),
    ]

    print()
    for i, (ico, label, _) in enumerate(categorias, 1):
        print(f"  {c(Color.CYAN, str(i) + '.')} {ico}  {label}")
    print()

    try:
        cat_input = input(f"  {c(Color.GRAY, 'Categoría [1-6]:')} ").strip()
        cat_idx = int(cat_input) - 1
        if not (0 <= cat_idx < len(categorias)):
            raise ValueError
    except (ValueError, KeyboardInterrupt):
        error("Categoría inválida")
        return

    ico_cat, label_cat, tipos = categorias[cat_idx]
    print()
    titulo(f"{ico_cat} {label_cat} — Selecciona el tipo")

    for i, t in enumerate(tipos, 1):
        print(f"  {c(Color.CYAN, str(i) + '.')} {icono_tipo(t)}  {t}")
    print()

    try:
        tipo_input = input(f"  {c(Color.GRAY, f'Tipo [1-{len(tipos)}]:')} ").strip()
        tipo_idx = int(tipo_input) - 1
        if not (0 <= tipo_idx < len(tipos)):
            raise ValueError
        tipo = tipos[tipo_idx]
    except (ValueError, KeyboardInterrupt):
        error("Tipo inválido")
        return

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


def _cmd_eliminar_version(numero_version_str):
    """Elimina una versión específica y reorganiza las demás"""
    if not verificarCronux():
        error("No estás en un proyecto Cronux")
        return
    
    # Importar la función de cli_integration
    sys.path.insert(0, str(Path(__file__).parent.parent / "ui"))
    try:
        from cli_integration import eliminar_version_ui
    except ImportError:
        error("No se pudo importar la función eliminar_version_ui")
        return
    
    try:
        numero_version = float(numero_version_str.replace("v", "").replace("V", ""))
    except ValueError:
        error(f"Versión inválida: {numero_version_str}")
        return
    
    # Proteger versión 1
    if numero_version == 1:
        error("No se puede eliminar la versión 1 (versión original)")
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
        resultado = eliminar_version_ui(str(Path.cwd()), numero_version)
        if resultado:
            print()
            ok(f"Versión {c(Color.BOLD, f'v{numero_version}')} eliminada")
            info("Las versiones posteriores han sido renumeradas")
        else:
            error("No se pudo eliminar la versión")
    except Exception as e:
        error(f"Error al eliminar versión: {e}")
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
    if len(sys.argv) < 2:
        modo_interactivo()
        return

    comando = sys.argv[1].lower()
    resto = sys.argv[2:]

    try:
        if comando in ["ayuda", "help", "--help", "-h"]:
            mostrar_ayuda()

        elif comando in ["--version", "-v"]:
            print(f"\n  {c(Color.CYAN, 'Cronux-CRX')} v0.2.0  —  Control de Versiones Local\n")

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
