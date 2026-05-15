"""
Integración entre la UI y las funciones CLI
"""
import sys
from pathlib import Path
import json
from datetime import datetime
import os

# Agregar el directorio cli al path
# Cuando Flet desempaqueta la app, todo está en el mismo nivel
# Buscar en múltiples ubicaciones posibles

# 1. Mismo directorio que este archivo (cuando está desempaquetado por Flet)
cli_mismo_dir = Path(__file__).parent / "cli"

# 2. Carpeta data/cli (cuando está en el bundle de Flet)
cli_data = Path(__file__).parent.parent / "data" / "cli"

# 3. Desarrollo - carpeta padre
cli_parent = Path(__file__).parent.parent / "cli"

print(f"[CLI] Buscando módulos CLI...")
print(f"[CLI] __file__ = {__file__}")
print(f"[CLI] parent = {Path(__file__).parent}")

if cli_mismo_dir.exists():
    sys.path.insert(0, str(cli_mismo_dir))
    print(f"[CLI] ✓ Usando módulos en: {cli_mismo_dir}")
elif cli_data.exists():
    sys.path.insert(0, str(cli_data))
    print(f"[CLI] ✓ Usando módulos en: {cli_data}")
elif cli_parent.exists():
    sys.path.insert(0, str(cli_parent))
    print(f"[CLI] ✓ Usando módulos en: {cli_parent}")
else:
    print(f"[CLI] ⚠️  No se encontraron módulos CLI en:")
    print(f"  - {cli_mismo_dir} (existe: {cli_mismo_dir.exists()})")
    print(f"  - {cli_data} (existe: {cli_data.exists()})")
    print(f"  - {cli_parent} (existe: {cli_parent.exists()})")

try:
    from crear_proyecto import crear_proyecto_cli
    from guardar_version import guardar_version_cli
    from restaurar_versiones import restaurar_version_cli
    from funcion_verficar import verificarCronux, obtener_ruta_cronux
    print("[CLI] ✓ Módulos CLI importados correctamente")
except ImportError as e:
    print(f"[CLI] ❌ Error importando módulos CLI: {e}")
    import traceback
    traceback.print_exc()


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


def escanear_proyectos_sistema():
    """
    Escanea directorios comunes buscando proyectos Cronux (.cronux folder)
    y los agrega a la lista si no están ya
    """
    import os
    from pathlib import Path
    
    # Directorios comunes donde buscar proyectos (solo nivel 1 y 2)
    directorios_busqueda = [
        Path.home() / "Documentos",
        Path.home() / "Documents", 
        Path.home() / "Desktop",
        Path.home() / "Escritorio",
    ]
    
    proyectos_encontrados = []
    rutas_vistas = set()
    
    print("[SCAN] Escaneando sistema en busca de proyectos Cronux...")
    
    for directorio_base in directorios_busqueda:
        if not directorio_base.exists():
            continue
        
        try:
            # Buscar carpetas .cronux (máximo 2 niveles de profundidad)
            for root, dirs, files in os.walk(directorio_base):
                # Limitar profundidad a 2 niveles
                depth = root[len(str(directorio_base)):].count(os.sep)
                if depth >= 2:
                    dirs[:] = []  # No seguir bajando
                    continue
                
                # Ignorar carpetas ocultas y del sistema
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__', 'build', 'dist']]
                
                if ".cronux" in dirs:
                    ruta_proyecto = Path(root)
                    ruta_str = str(ruta_proyecto)
                    
                    # Evitar duplicados
                    if ruta_str not in rutas_vistas:
                        rutas_vistas.add(ruta_str)
                        proyecto_info = leer_info_proyecto(ruta_str)
                        if proyecto_info:
                            proyectos_encontrados.append(proyecto_info)
                            print(f"[SCAN] ✓ Encontrado: {proyecto_info['nombre']} en {ruta_str}")
                    
                    # No buscar dentro de proyectos Cronux
                    dirs.remove(".cronux")
        except (PermissionError, OSError) as e:
            # Ignorar errores de permisos
            continue
    
    print(f"[SCAN] Escaneo completo. Encontrados {len(proyectos_encontrados)} proyectos")
    return proyectos_encontrados


def sincronizar_proyectos():
    """
    Sincroniza la lista de proyectos guardada con los proyectos encontrados en el sistema.
    Agrega nuevos proyectos encontrados y elimina los que ya no existen.
    """
    # Cargar lista actual
    proyectos_guardados = cargar_lista_proyectos()
    rutas_guardadas = {p["ruta"] for p in proyectos_guardados}
    
    # Escanear sistema
    proyectos_escaneados = escanear_proyectos_sistema()
    rutas_escaneadas = {p["ruta"] for p in proyectos_escaneados}
    
    # Combinar: mantener guardados que existen + agregar nuevos escaneados
    proyectos_finales = []
    rutas_finales = set()
    
    # Primero agregar los guardados que aún existen
    for p in proyectos_guardados:
        ruta = p["ruta"]
        if Path(ruta).exists() and (Path(ruta) / ".cronux").exists():
            proyectos_finales.append(p)
            rutas_finales.add(ruta)
    
    # Luego agregar los nuevos encontrados
    for p in proyectos_escaneados:
        if p["ruta"] not in rutas_finales:
            proyectos_finales.append(p)
            rutas_finales.add(p["ruta"])
    
    # Guardar lista actualizada
    if len(proyectos_finales) != len(proyectos_guardados):
        print(f"[SYNC] Sincronizados {len(proyectos_finales)} proyectos (antes: {len(proyectos_guardados)})")
        guardar_lista_proyectos(proyectos_finales)
    
    return proyectos_finales


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
    """Guarda una versión desde la UI y la marca como actual"""
    import os
    
    # Cambiar al directorio del proyecto
    os.chdir(ruta_proyecto)
    
    # Guardar versión con CLI
    exito = guardar_version_cli(mensaje, callback_progreso)
    
    if exito:
        # Obtener el número de la nueva versión (la más reciente)
        carpeta_cronux = Path(ruta_proyecto) / ".cronux"
        carpeta_versiones = carpeta_cronux / "versiones"
        
        if carpeta_versiones.exists():
            versiones = []
            for carpeta in carpeta_versiones.iterdir():
                if carpeta.is_dir() and carpeta.name.startswith("version_"):
                    try:
                        num_str = carpeta.name.replace("version_", "")
                        # Convertir a int (formato nuevo)
                        num = int(float(num_str))
                        versiones.append(num)
                    except ValueError:
                        continue
            
            if versiones:
                nueva_version = max(versiones)
                
                # Actualizar version_actual en proyecto.json
                archivo_proyecto = carpeta_cronux / "proyecto.json"
                if archivo_proyecto.exists():
                    try:
                        with open(archivo_proyecto, "r") as f:
                            datos_proyecto = json.load(f)
                        
                        datos_proyecto["version_actual"] = nueva_version
                        
                        with open(archivo_proyecto, "w") as f:
                            json.dump(datos_proyecto, f, indent=2)
                    except Exception as e:
                        print(f"[WARN] No se pudo actualizar version_actual: {e}")
        
        # Leer información actualizada del proyecto
        proyecto_info = leer_info_proyecto(ruta_proyecto)
        return proyecto_info
    
    return None


def restaurar_version_ui(ruta_proyecto, numero_version, callback_progreso=None):
    """Restaura una versión desde la UI (sin confirmación interactiva)"""
    import os
    
    # Cambiar al directorio del proyecto
    os.chdir(ruta_proyecto)
    
    # Convertir numero_version a int si es necesario
    try:
        numero_version = int(float(numero_version))
    except (ValueError, TypeError):
        pass
    
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
                
                # Actualizar versión actual (como entero)
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
    
    # Validación estricta: debe existir la carpeta .cronux Y el archivo proyecto.json
    if not carpeta_cronux.exists() or not carpeta_cronux.is_dir():
        return None
    
    # Leer datos del proyecto
    archivo_proyecto = carpeta_cronux / "proyecto.json"
    if not archivo_proyecto.exists() or not archivo_proyecto.is_file():
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
                    
                    # Convertir versión a entero (formato nuevo)
                    numero_version = metadatos["version"]
                    try:
                        # Si es float, convertir a int
                        numero_version = int(float(numero_version))
                    except (ValueError, TypeError):
                        numero_version = metadatos["version"]
                    
                    versiones.append({
                        "numero": numero_version,
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
    try:
        # Convertir a entero (formato nuevo)
        version_actual = int(float(version_actual))
    except (ValueError, TypeError):
        version_actual = 1
    
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
    
    if not carpeta_cronux.exists():
        print(f"[WARN] Carpeta .cronux no existe en {ruta}")
        # Aún así, eliminar de la lista
        proyectos = cargar_lista_proyectos()
        proyectos = [p for p in proyectos if p["ruta"] != str(ruta)]
        guardar_lista_proyectos(proyectos)
        return True
    
    try:
        # Eliminar carpeta .cronux
        print(f"[DELETE] Eliminando {carpeta_cronux}")
        shutil.rmtree(carpeta_cronux)
        print(f"[DELETE] ✓ Carpeta .cronux eliminada")
        
        # Eliminar de la lista guardada
        proyectos = cargar_lista_proyectos()
        proyectos_antes = len(proyectos)
        proyectos = [p for p in proyectos if p["ruta"] != str(ruta)]
        proyectos_despues = len(proyectos)
        guardar_lista_proyectos(proyectos)
        print(f"[DELETE] ✓ Eliminado de la lista ({proyectos_antes} -> {proyectos_despues})")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error eliminando proyecto: {e}")
        import traceback
        traceback.print_exc()
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
                        # Validar que sea un proyecto válido (debe tener proyecto.json)
                        archivo_proyecto = item / "proyecto.json"
                        if not archivo_proyecto.exists():
                            print(f"      Carpeta .cronux sin proyecto.json - ignorando")
                            continue
                        
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


def eliminar_version_ui(ruta_proyecto, numero_version):
    """
    Elimina una versión y reorganiza los números de versión.
    La versión 1 (original) no se puede eliminar.
    """
    import shutil
    
    try:
        # Protección: No permitir eliminar la versión 1
        if numero_version == 1 or numero_version == "1":
            print("[ERROR] No se puede eliminar la versión original (v1)")
            return False
        
        carpeta_cronux = Path(ruta_proyecto) / ".cronux"
        carpeta_versiones = carpeta_cronux / "versiones"
        
        if not carpeta_versiones.exists():
            return False
        
        # Obtener todas las versiones ordenadas
        versiones = []
        for carpeta in sorted(carpeta_versiones.iterdir()):
            if carpeta.is_dir() and carpeta.name.startswith("version_"):
                try:
                    num = carpeta.name.replace("version_", "")
                    versiones.append((float(num), carpeta))
                except ValueError:
                    continue
        
        # Buscar la versión a eliminar
        version_a_eliminar = None
        indice_eliminar = -1
        
        for i, (num, carpeta) in enumerate(versiones):
            if num == float(numero_version):
                version_a_eliminar = carpeta
                indice_eliminar = i
                break
        
        if not version_a_eliminar or not version_a_eliminar.exists():
            print(f"[ERROR] La versión {numero_version} no existe")
            return False
        
        # Eliminar la carpeta de la versión
        shutil.rmtree(version_a_eliminar)
        print(f"[INFO] Versión {numero_version} eliminada")
        
        # Reorganizar las versiones posteriores
        # Las versiones después de la eliminada se renumeran
        for i in range(indice_eliminar + 1, len(versiones)):
            num_actual, carpeta_actual = versiones[i]
            nuevo_numero = num_actual - 0.1  # Decrementar en 0.1
            
            # Renombrar la carpeta
            nuevo_nombre = f"version_{nuevo_numero:.1f}"
            nueva_ruta = carpeta_versiones / nuevo_nombre
            carpeta_actual.rename(nueva_ruta)
            
            # Actualizar metadatos.json si existe
            archivo_metadatos = nueva_ruta / "metadatos.json"
            if archivo_metadatos.exists():
                try:
                    with open(archivo_metadatos, "r") as f:
                        metadatos = json.load(f)
                    
                    metadatos["version"] = f"{nuevo_numero:.1f}"
                    
                    with open(archivo_metadatos, "w") as f:
                        json.dump(metadatos, f, indent=2)
                except Exception as e:
                    print(f"[WARN] No se pudo actualizar metadatos de {nuevo_nombre}: {e}")
        
        # Actualizar version_actual en proyecto.json si es necesario
        archivo_proyecto = carpeta_cronux / "proyecto.json"
        if archivo_proyecto.exists():
            try:
                with open(archivo_proyecto, "r") as f:
                    datos_proyecto = json.load(f)
                
                version_actual = datos_proyecto.get("version_actual", 1)
                
                # Si la versión actual era la eliminada, cambiar a la anterior
                if float(version_actual) == float(numero_version):
                    # Buscar la versión anterior más cercana
                    versiones_restantes = []
                    for carpeta in sorted(carpeta_versiones.iterdir()):
                        if carpeta.is_dir() and carpeta.name.startswith("version_"):
                            try:
                                num = float(carpeta.name.replace("version_", ""))
                                versiones_restantes.append(num)
                            except ValueError:
                                continue
                    
                    if versiones_restantes:
                        # Usar la versión más reciente
                        datos_proyecto["version_actual"] = max(versiones_restantes)
                    else:
                        datos_proyecto["version_actual"] = 1
                    
                    with open(archivo_proyecto, "w") as f:
                        json.dump(datos_proyecto, f, indent=2)
                
                # Si la versión actual era posterior a la eliminada, decrementar
                elif float(version_actual) > float(numero_version):
                    datos_proyecto["version_actual"] = float(version_actual) - 0.1
                    
                    with open(archivo_proyecto, "w") as f:
                        json.dump(datos_proyecto, f, indent=2)
                        
            except Exception as e:
                print(f"[WARN] No se pudo actualizar version_actual: {e}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error eliminando versión: {e}")
        import traceback
        traceback.print_exc()
        return False
