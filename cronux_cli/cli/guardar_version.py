from pathlib import Path
from funcion_verficar import *
import json
from datetime import datetime
import shutil

# Exclusiones por tipo de proyecto
EXCLUSIONES_POR_TIPO = {
    "nodejs": [
        "node_modules", ".npm", "npm-debug.log", "yarn-error.log",
        ".pnpm-store", ".yarn"
    ],
    "python": [
        "__pycache__", "*.pyc", "*.pyo", "*.pyd", ".Python",
        "venv", "env", ".venv", ".env", "ENV", "env.bak", "venv.bak",
        "*.egg-info", "dist", "build", ".pytest_cache", ".mypy_cache"
    ],
    "java_maven": [
        "target", ".mvn", "mvnw", "mvnw.cmd", ".classpath", ".project",
        ".settings", "*.class", "*.jar", "*.war"
    ],
    "java_gradle": [
        "build", ".gradle", "gradle", "gradlew", "gradlew.bat",
        ".classpath", ".project", ".settings", "*.class", "*.jar", "*.war"
    ],
    "php": [
        "vendor", "composer.lock", ".phpunit.result.cache"
    ],
    "ruby": [
        "vendor/bundle", ".bundle", "*.gem", ".rspec"
    ],
    "dotnet": [
        "bin", "obj", "*.dll", "*.exe", "*.pdb", ".vs", "packages"
    ],
    "go": [
        "vendor", "*.exe", "*.test", "*.out"
    ],
    "general": []
}

def debe_excluir(item_name, tipo_proyecto):
    """Verifica si un archivo/carpeta debe ser excluido según el tipo de proyecto"""
    exclusiones = EXCLUSIONES_POR_TIPO.get(tipo_proyecto, [])
    
    for patron in exclusiones:
        if patron.startswith("*"):
            # Patrón de extensión
            if item_name.endswith(patron[1:]):
                return True
        else:
            # Nombre exacto
            if item_name == patron:
                return True
    
    return False

def calcular_tamaño_directorio(directorio):
    """Calcula el tamaño total de un directorio en bytes"""
    tamaño_total = 0
    try:
        for item in directorio.rglob('*'):
            if item.is_file():
                tamaño_total += item.stat().st_size
    except Exception:
        pass
    return tamaño_total

def formatear_tamaño(bytes_size):
    """Convierte bytes a formato legible (KB, MB, GB)"""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.1f} KB"
    elif bytes_size < 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_size / (1024 * 1024 * 1024):.1f} GB"

def guardar_version_cli(mensaje, callback_progreso=None):
    """Versión CLI que recibe el mensaje como parámetro y opcionalmente un callback de progreso"""
    # Verificar que estamos en el proyecto cronux
    if not verificarCronux():
        print("ERROR: No estas en un proyecto Cronux")
        return False

    # Leer tipo de proyecto
    tipo_proyecto = "general"
    try:
        with open(obtener_ruta_cronux() / "proyecto.json", "r") as f:
            datos = json.load(f)
            tipo_proyecto = datos.get("tipo", "general")
    except:
        pass

    # Determinar número de la versión
    numero_version = determinar_numero_version()

    # Crear la carpeta de versiones dentro de .cronux
    carpeta_versiones = obtener_ruta_cronux() / "versiones"
    carpeta_versiones.mkdir(exist_ok=True)

    # Crear carpeta específica para esta versión
    carpeta_version = carpeta_versiones / f"version_{numero_version}"
    carpeta_version.mkdir(exist_ok=True)

    # Copiar todos los archivos del directorio actual (excepto .cronux y exclusiones)
    directorio_actual = Path.cwd()
    
    archivos_copiados = 0
    archivos_excluidos = 0
    
    # Contar total de archivos primero (excluyendo .cronux y .git)
    total_archivos = sum(1 for item in directorio_actual.iterdir() 
                        if item.name != ".cronux" and not item.name.startswith('.git') 
                        and not debe_excluir(item.name, tipo_proyecto))
    
    if callback_progreso:
        callback_progreso(f"Analizando archivos del proyecto (0/{total_archivos})")
    
    archivos_procesados = 0
    
    for item in directorio_actual.iterdir():
        if item.name == ".cronux" or item.name.startswith('.git'):
            continue
        
        # Verificar exclusiones por tipo de proyecto
        if debe_excluir(item.name, tipo_proyecto):
            archivos_excluidos += 1
            if callback_progreso:
                callback_progreso(f"  ⊗ Excluyendo: {item.name}")
            continue
        
        destino = carpeta_version / item.name
        try:
            archivos_procesados += 1
            porcentaje = int((archivos_procesados / total_archivos) * 100) if total_archivos > 0 else 100
            
            if callback_progreso:
                callback_progreso(f"{item.name} ({archivos_procesados}/{total_archivos} - {porcentaje}%)")
            
            if item.is_file():
                shutil.copy2(item, destino)
                archivos_copiados += 1
            elif item.is_dir():
                shutil.copytree(item, destino)
                archivos_copiados += 1
        except Exception as e:
            error_msg = f"No se pudo copiar {item.name}: {e}"
            print(f"Advertencia: {error_msg}")
            if callback_progreso:
                callback_progreso(f"⚠ {error_msg}")

    # Calcular tamaño de la versión
    tamaño_bytes = calcular_tamaño_directorio(carpeta_version)
    tamaño_formateado = formatear_tamaño(tamaño_bytes)

    # Crear metadatos de la versión
    metadatos = {
        "version": numero_version,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mensaje": mensaje or "Sin mensaje",
        "tipo_proyecto": tipo_proyecto,
        "archivos_guardados": archivos_copiados,
        "archivos_excluidos": archivos_excluidos,
        "tamaño_bytes": tamaño_bytes,
        "tamaño_formateado": tamaño_formateado
    }

    # Guardar metadatos
    archivo_metadatos = carpeta_version / "metadatos.json"
    with open(archivo_metadatos, "w") as f:
        json.dump(metadatos, f, indent=2)

    # Actualizar versión actual en proyecto.json
    try:
        proyecto_json = obtener_ruta_cronux() / "proyecto.json"
        if proyecto_json.exists():
            with open(proyecto_json, "r") as f:
                datos_proyecto = json.load(f)
            datos_proyecto["version_actual"] = numero_version
            with open(proyecto_json, "w") as f:
                json.dump(datos_proyecto, f, indent=2)
    except Exception as e:
        print(f"Advertencia: No se pudo actualizar version_actual: {e}")

    print(f"\n  ✓  Versión {numero_version} guardada")
    print(f"  ●  Mensaje:  {metadatos['mensaje']}")
    print(f"  ●  Archivos: {archivos_copiados}  |  Tamaño: {tamaño_formateado}\n")
    
    return True