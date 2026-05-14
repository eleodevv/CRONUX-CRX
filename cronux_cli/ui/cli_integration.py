"""
Integración entre la UI y las funciones CLI
"""
import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar el directorio cli al path
# Primero intentar desde la carpeta local (cuando está empaquetado)
cli_local = Path(__file__).parent / "cli"
cli_parent = Path(__file__).parent.parent / "cli"

if cli_local.exists():
    sys.path.insert(0, str(cli_local))
elif cli_parent.exists():
    sys.path.insert(0, str(cli_parent))
else:
    # Fallback: intentar importar directamente
    pass

from crear_proyecto import crear_proyecto_cli
from guardar_version import guardar_version_cli
from restaurar_versiones import restaurar_version_cli
from funcion_verficar import verificarCronux, obtener_ruta_cronux


# Archivo de configuración para guardar proyectos
CONFIG_DIR = Path.home() / ".cronux-ui"
CONFIG_FILE = CONFIG_DIR / "proyectos.json"
FAVORITES_FILE = CONFIG_DIR / "favoritos.json"


def cargar_favoritos():
    """Carga la lista de rutas favoritas"""
    if not FAVORITES_FILE.exists():
        return set()
    try:
        with open(FAVORITES_FILE, "r") as f:
            data = json.load(f)
        return set(data.get("favoritos", []))
    except Exception:
        return set()


def guardar_favoritos(favoritos):
    """Guarda la lista de rutas favoritas"""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(FAVORITES_FILE, "w") as f:
        json.dump({"favoritos": list(favoritos)}, f, indent=2)


def toggle_favorito(ruta):
    """Agrega o quita un proyecto de favoritos, retorna True si quedó como favorito"""
    favs = cargar_favoritos()
    if ruta in favs:
        favs.discard(ruta)
        es_favorito = False
    else:
        favs.add(ruta)
        es_favorito = True
    guardar_favoritos(favs)
    return es_favorito


def obtener_icono_por_tipo(tipo):
    """Obtiene la ruta del icono según el tipo de proyecto"""
    # Mapeo de tipos a iconos (rutas relativas al assets_dir)
    # Estos son los mismos iconos que se usan en el wizard
    iconos = {
        # Lenguajes de programación
        "python": "python.png",
        "javascript": "javascript.png",
        "java": "java.png",
        "php": "php.png",
        "ruby": "ruby.png",
        "go": "go.png",
        "flutter": "flutter.png",
        "dotnet": ".net.png",
        
        # JavaScript frameworks
        "react": "react.png",
        "vanilla_js": "javascript.png",
        "nodejs": "node.png",
        "general_js": "lanzamiento-del-proyecto.png",
        
        # Documentos
        "word": "word.png",
        "excel": "excel.png",
        "powerpoint": "powerpoint.png",
        "pdf": "pdf.png",
        "latex": "Latex.png",
        "general_doc": "generalDoc.png",
        
        # Imágenes
        "png": "png.png",
        "jpg": "jpg.png",
        "svg": "svg.png",
        "gif": "gif.png",
        "raw": "raw.png",
        "general_img": "generalimagen.png",
        
        # Categorías generales
        "software": "lanzamiento-del-proyecto.png",
        "documentos": "generalDoc.png",
        "imagenes": "generalimagen.png",
        "tareas": None,  # Usar icono de Flet
        "investigacion": None,  # Usar icono de Flet
        "diseno": None,  # Usar icono de Flet
        "general": "lanzamiento-del-proyecto.png",
    }
    
    # Retornar icono o None si no existe (None significa usar icono de Flet)
    return iconos.get(tipo.lower())


def guardar_lista_proyectos(proyectos):
    """Guarda la lista de proyectos en el archivo de configuración"""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    # Guardar solo las rutas de los proyectos (sin iconos)
    proyectos_data = []
    for p in proyectos:
        if isinstance(p, dict):
            proyectos_data.append(str(p.get("ruta", "")))
    
    with open(CONFIG_FILE, "w") as f:
        json.dump({"proyectos": proyectos_data}, f, indent=2)


def cargar_lista_proyectos():
    """Carga la lista de proyectos desde el archivo de configuración, eliminando duplicados"""
    if not CONFIG_FILE.exists():
        return []
    
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        
        proyectos_data = data.get("proyectos", [])
        proyectos = []
        rutas_vistas = set()  # Para evitar duplicados
        
        # Leer información de cada proyecto
        for item in proyectos_data:
            if isinstance(item, str):
                ruta = item
            else:
                ruta = item.get("ruta")
            
            # Saltar duplicados
            if ruta in rutas_vistas:
                continue
            rutas_vistas.add(ruta)
            
            proyecto_info = leer_info_proyecto(ruta)
            if proyecto_info:
                proyectos.append(proyecto_info)
        
        # Si había duplicados, guardar lista limpia
        if len(proyectos) < len(proyectos_data):
            print(f"[CLEAN] Eliminados {len(proyectos_data) - len(proyectos)} duplicados de la lista")
            guardar_lista_proyectos(proyectos)
        
        return proyectos
    except Exception as e:
        print(f"Error cargando proyectos: {e}")
        return []


def agregar_proyecto_a_lista(ruta_proyecto):
    """Agrega un proyecto a la lista guardada"""
    proyectos = cargar_lista_proyectos()
    
    # Verificar que no esté duplicado
    rutas_existentes = [p["ruta"] for p in proyectos]
    if ruta_proyecto not in rutas_existentes:
        proyecto_info = leer_info_proyecto(ruta_proyecto)
        if proyecto_info:
            proyectos.append(proyecto_info)
            guardar_lista_proyectos(proyectos)
            return proyecto_info
    
    return None


def crear_proyecto_ui(nombre, ruta, tipo, callback_progreso=None):
    """Crea un proyecto desde la UI"""
    import os
    
    # Cambiar al directorio del proyecto
    os.chdir(ruta)
    
    # Crear proyecto con CLI
    exito = crear_proyecto_cli(nombre, tipo, callback_progreso)
    
    if exito:
        # Leer información del proyecto creado
        proyecto_info = leer_info_proyecto(ruta)
        
        # Agregar a la lista guardada
        if proyecto_info:
            agregar_proyecto_a_lista(ruta)
        
        return proyecto_info
    
    return None


def guardar_version_ui(ruta_proyecto, mensaje, callback_progreso=None):
    """Guarda una versión desde la UI"""
    import os
    
    # Cambiar al directorio del proyecto
    os.chdir(ruta_proyecto)
    
    # Guardar versión con CLI
    exito = guardar_version_cli(mensaje, callback_progreso)
    
    if exito:
        # Leer información actualizada del proyecto
        proyecto_info = leer_info_proyecto(ruta_proyecto)
        return proyecto_info
    
    return None


def restaurar_version_ui(ruta_proyecto, numero_version, callback_progreso=None):
    """Restaura una versión desde la UI (sin confirmación interactiva)"""
    import os
    
    # Cambiar al directorio del proyecto
    os.chdir(ruta_proyecto)
    
    # Crear callback que imprime en consola si no se proporciona uno
    def progress_callback(msg):
        if callback_progreso and callable(callback_progreso):
            callback_progreso(msg)
        else:
            print(f"[PROGRESS] {msg}")
    
    # Restaurar versión con CLI - pasar callback para evitar input()
    exito = restaurar_version_cli(str(numero_version), auto_instalar=True, callback_progreso=progress_callback)
    
    if exito:
        # Guardar la versión actual en proyecto.json
        carpeta_cronux = Path(ruta_proyecto) / ".cronux"
        archivo_proyecto = carpeta_cronux / "proyecto.json"
        
        if archivo_proyecto.exists():
            try:
                with open(archivo_proyecto, "r") as f:
                    datos_proyecto = json.load(f)
                
                # Actualizar versión actual
                datos_proyecto["version_actual"] = numero_version
                
                with open(archivo_proyecto, "w") as f:
                    json.dump(datos_proyecto, f, indent=2)
            except Exception as e:
                print(f"Error guardando versión actual: {e}")
        
        # Leer información actualizada del proyecto
        proyecto_info = leer_info_proyecto(ruta_proyecto)
        return proyecto_info
    
    return None


def leer_info_proyecto(ruta_proyecto):
    """Lee la información completa de un proyecto"""
    ruta = Path(ruta_proyecto)
    carpeta_cronux = ruta / ".cronux"
    
    if not carpeta_cronux.exists():
        return None
    
    # Leer datos del proyecto
    archivo_proyecto = carpeta_cronux / "proyecto.json"
    if not archivo_proyecto.exists():
        return None
    
    try:
        with open(archivo_proyecto, "r") as f:
            datos_proyecto = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error leyendo proyecto.json en {ruta_proyecto}: {e}")
        print(f"  El archivo puede estar corrupto. Intenta eliminarlo y crear el proyecto de nuevo.")
        return None
    except Exception as e:
        print(f"Error inesperado leyendo proyecto en {ruta_proyecto}: {e}")
        return None
    
    # Obtener tipo y generar icono dinámicamente
    tipo = datos_proyecto.get("tipo", "general")
    icono = obtener_icono_por_tipo(tipo)
    
    # Leer versiones
    versiones = []
    carpeta_versiones = carpeta_cronux / "versiones"
    
    if carpeta_versiones.exists():
        for carpeta_version in sorted(carpeta_versiones.iterdir()):
            if carpeta_version.is_dir() and carpeta_version.name.startswith("version_"):
                metadatos_file = carpeta_version / "metadatos.json"
                if metadatos_file.exists():
                    with open(metadatos_file, "r") as f:
                        metadatos = json.load(f)
                    
                    # Formatear fecha relativa
                    try:
                        fecha_dt = datetime.strptime(metadatos["fecha"], "%Y-%m-%d %H:%M:%S")
                        ahora = datetime.now()
                        diff = ahora - fecha_dt
                        
                        if diff.days == 0:
                            if diff.seconds < 60:
                                fecha_relativa = "Ahora"
                            elif diff.seconds < 3600:
                                minutos = diff.seconds // 60
                                fecha_relativa = f"Hace {minutos} min"
                            else:
                                horas = diff.seconds // 3600
                                fecha_relativa = f"Hace {horas}h"
                        elif diff.days == 1:
                            fecha_relativa = "Ayer"
                        elif diff.days < 7:
                            fecha_relativa = f"Hace {diff.days} días"
                        elif diff.days < 30:
                            semanas = diff.days // 7
                            fecha_relativa = f"Hace {semanas} semanas"
                        else:
                            meses = diff.days // 30
                            fecha_relativa = f"Hace {meses} meses"
                    except:
                        fecha_relativa = metadatos["fecha"]
                    
                    versiones.append({
                        "numero": metadatos["version"],
                        "fecha": fecha_relativa,
                        "fecha_completa": metadatos["fecha"],
                        "descripcion": metadatos.get("mensaje", "Sin descripción"),
                        "archivos": metadatos.get("archivos_guardados", 0),
                        "tamaño": metadatos.get("tamaño_formateado", "0 B"),
                        "autor": "Usuario",
                    })
    
    # Calcular tamaño total del proyecto
    tamaño_total_bytes = 0
    for version in versiones:
        # Leer metadatos para obtener tamaño en bytes
        num_version = version["numero"]
        metadatos_file = carpeta_versiones / f"version_{num_version}" / "metadatos.json"
        if metadatos_file.exists():
            with open(metadatos_file, "r") as f:
                metadatos = json.load(f)
                tamaño_total_bytes += metadatos.get("tamaño_bytes", 0)
    
    # Formatear tamaño total
    if tamaño_total_bytes < 1024:
        tamaño_total = f"{tamaño_total_bytes} B"
    elif tamaño_total_bytes < 1024 * 1024:
        tamaño_total = f"{tamaño_total_bytes / 1024:.1f} KB"
    elif tamaño_total_bytes < 1024 * 1024 * 1024:
        tamaño_total = f"{tamaño_total_bytes / (1024 * 1024):.1f} MB"
    else:
        tamaño_total = f"{tamaño_total_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    # Leer versión actual del proyecto (la que está en uso)
    version_actual = datos_proyecto.get("version_actual", 1)  # Por defecto v1
    
    return {
        "nombre": datos_proyecto["nombre"],
        "tipo": datos_proyecto["tipo"],
        "ruta": str(ruta),
        "fecha_creacion": datos_proyecto.get("fecha_creacion", ""),
        "icono": icono,  # Icono generado dinámicamente según el tipo
        "versiones": versiones,
        "tamaño_total": tamaño_total,
        "version_actual": version_actual,  # Versión actualmente en uso
    }


def eliminar_proyecto_ui(ruta_proyecto):
    """Elimina un proyecto completamente"""
    import shutil
    
    ruta = Path(ruta_proyecto)
    carpeta_cronux = ruta / ".cronux"
    
    if carpeta_cronux.exists():
        try:
            # Eliminar carpeta .cronux
            shutil.rmtree(carpeta_cronux)
            
            # Eliminar de la lista guardada
            proyectos = cargar_lista_proyectos()
            proyectos = [p for p in proyectos if p["ruta"] != str(ruta)]
            guardar_lista_proyectos(proyectos)
            
            return True
        except Exception as e:
            print(f"Error eliminando proyecto: {e}")
            return False
    
    return False


def abrir_carpeta_proyecto(ruta_proyecto):
    """Abre la carpeta del proyecto en el explorador de archivos"""
    import subprocess
    import platform
    
    try:
        sistema = platform.system()
        
        if sistema == "Windows":
            subprocess.run(["explorer", ruta_proyecto])
        elif sistema == "Darwin":  # macOS
            subprocess.run(["open", ruta_proyecto])
        else:  # Linux
            subprocess.run(["xdg-open", ruta_proyecto])
        
        return True
    except Exception as e:
        print(f"Error abriendo carpeta: {e}")
        return False


def exportar_proyecto_ui(ruta_proyecto, ruta_destino):
    """Exporta el proyecto completo a un archivo ZIP"""
    import shutil
    from datetime import datetime
    
    try:
        ruta = Path(ruta_proyecto)
        nombre_proyecto = ruta.name
        
        # Crear nombre del archivo ZIP
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_zip = f"{nombre_proyecto}_{timestamp}"
        
        # Crear ZIP
        archivo_zip = shutil.make_archive(
            str(Path(ruta_destino) / nombre_zip),
            'zip',
            ruta
        )
        
        return archivo_zip
    except Exception as e:
        print(f"Error exportando proyecto: {e}")
        return None


def actualizar_nombre_proyecto(ruta_proyecto, nuevo_nombre):
    """Actualiza el nombre de un proyecto"""
    import json
    
    try:
        carpeta_cronux = Path(ruta_proyecto) / ".cronux"
        archivo_proyecto = carpeta_cronux / "proyecto.json"
        
        if archivo_proyecto.exists():
            with open(archivo_proyecto, "r") as f:
                datos_proyecto = json.load(f)
            
            datos_proyecto["nombre"] = nuevo_nombre
            
            with open(archivo_proyecto, "w") as f:
                json.dump(datos_proyecto, f, indent=2)
            
            # Actualizar en la lista guardada
            proyectos = cargar_lista_proyectos()
            guardar_lista_proyectos(proyectos)
            
            return True
    except Exception as e:
        print(f"Error actualizando nombre: {e}")
        return False
    
    return False


def buscar_proyectos_en_directorio(directorio_base, max_depth=3):
    """Busca proyectos Cronux en un directorio y subdirectorios"""
    proyectos_encontrados = []
    directorio = Path(directorio_base).expanduser()
    
    print(f"  Buscando en: {directorio}")
    
    if not directorio.exists():
        print(f"    Directorio no existe")
        return proyectos_encontrados
    
    def buscar_recursivo(dir_actual, depth):
        if depth > max_depth:
            return
        
        try:
            for item in dir_actual.iterdir():
                # Saltar directorios ocultos excepto .cronux
                if item.name.startswith('.') and item.name != '.cronux':
                    continue
                
                if item.is_dir():
                    # Si encontramos una carpeta .cronux, el padre es un proyecto
                    if item.name == '.cronux':
                        proyecto_dir = item.parent
                        print(f"    ¡Encontrado! {proyecto_dir}")
                        proyecto_info = leer_info_proyecto(str(proyecto_dir))
                        if proyecto_info:
                            proyectos_encontrados.append(proyecto_info)
                            print(f"      Proyecto válido: {proyecto_info.get('nombre')}")
                        else:
                            print(f"      Proyecto inválido (no se pudo leer)")
                    else:
                        # Continuar buscando en subdirectorios
                        buscar_recursivo(item, depth + 1)
        except PermissionError:
            print(f"    Sin permisos para acceder")
            pass
        except Exception as e:
            print(f"    Error: {e}")
            pass
    
    buscar_recursivo(directorio, 0)
    return proyectos_encontrados


def obtener_proyectos_existentes():
    """Busca proyectos Cronux existentes en ubicaciones comunes"""
    proyectos = []
    
    # Buscar en directorios comunes
    directorios_busqueda = [
        Path.home() / "Documentos",
        Path.home() / "Documents",
        Path.home() / "Proyectos",
        Path.home() / "Projects",
        Path.home(),
    ]
    
    for directorio in directorios_busqueda:
        if directorio.exists():
            proyectos.extend(buscar_proyectos_en_directorio(directorio, max_depth=2))
    
    # Eliminar duplicados por ruta
    proyectos_unicos = {}
    for p in proyectos:
        proyectos_unicos[p["ruta"]] = p
    
    return list(proyectos_unicos.values())


def sincronizar_proyectos():
    """Sincroniza proyectos guardados con proyectos encontrados en el sistema"""
    print("=== Iniciando sincronización de proyectos ===")
    
    # Cargar proyectos guardados
    proyectos_guardados = cargar_lista_proyectos()
    print(f"Proyectos guardados: {len(proyectos_guardados)}")
    for p in proyectos_guardados:
        print(f"  - {p.get('nombre')} en {p.get('ruta')}")
    
    rutas_guardadas = {p["ruta"] for p in proyectos_guardados}
    
    # Buscar proyectos en el sistema
    print("\nBuscando proyectos en el sistema...")
    proyectos_encontrados = obtener_proyectos_existentes()
    print(f"Proyectos encontrados: {len(proyectos_encontrados)}")
    for p in proyectos_encontrados:
        print(f"  - {p.get('nombre')} en {p.get('ruta')}")
    
    # Agregar proyectos encontrados que no estén guardados
    nuevos = 0
    for proyecto in proyectos_encontrados:
        if proyecto["ruta"] not in rutas_guardadas:
            print(f"Agregando nuevo proyecto: {proyecto.get('nombre')}")
            proyectos_guardados.append(proyecto)
            nuevos += 1
    
    print(f"\nProyectos nuevos agregados: {nuevos}")
    print(f"Total de proyectos: {len(proyectos_guardados)}")
    
    # Guardar lista actualizada
    if proyectos_guardados:
        guardar_lista_proyectos(proyectos_guardados)
        print("Lista guardada exitosamente")
    
    print("=== Sincronización completada ===\n")
    return proyectos_guardados
