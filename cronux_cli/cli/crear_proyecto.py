from pathlib import Path
import json
from datetime import datetime
from funcion_verficar import verificarCronux
import shutil



def crear_proyecto_cli(nombre_proyecto, tipo_proyecto="general", callback_progreso=None):
    """Versión CLI que recibe el nombre y tipo como parámetros y crea la versión 1 inicial"""
    
    # Verificar si ya existe un proyecto
    if verificarCronux():
        print("ERROR: Ya existe un proyecto Cronux-CRX en esta ubicacion")
        return False
    
    if callback_progreso:
        callback_progreso("Inicializando proyecto")
    
    # Crear carpeta .cronux
    carpeta_cronux = Path.cwd() / ".cronux"
    carpeta_cronux.mkdir(exist_ok=True)
    
    # Crear datos del proyecto
    datos_proyecto = {
        "nombre": nombre_proyecto,
        "tipo": tipo_proyecto,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "autor": "usuario"
    }
    
    # Guardar JSON
    archivo_proyecto = carpeta_cronux / "proyecto.json"
    with open(archivo_proyecto, "w") as f:
        json.dump(datos_proyecto, f, indent=2)
    
    if callback_progreso:
        callback_progreso("Estructura del proyecto creada")
    
    # Crear versión 1 automáticamente con el estado inicial
    carpeta_versiones = carpeta_cronux / "versiones"
    carpeta_versiones.mkdir(exist_ok=True)
    
    carpeta_version_1 = carpeta_versiones / "version_1"
    carpeta_version_1.mkdir(exist_ok=True)
    
    # Copiar archivos existentes (si los hay) a la versión 1
    directorio_actual = Path.cwd()
    archivos_copiados = 0
    archivos_excluidos = 0
    
    # Exclusiones por tipo de proyecto
    exclusiones_base = [".cronux", ".git", ".gitignore"]
    exclusiones_por_tipo = {
        "nodejs": ["node_modules", ".npm", "npm-debug.log", "yarn-error.log"],
        "python": ["__pycache__", "*.pyc", "venv", "env", ".venv", ".env", "ENV", "*.egg-info", "dist", "build"],
        "java_maven": ["target", ".mvn", "*.class", "*.jar", "*.war"],
        "java_gradle": ["build", ".gradle", "*.class", "*.jar", "*.war"],
        "php": ["vendor", "composer.lock"],
        "ruby": ["vendor/bundle", ".bundle", "*.gem"],
        "dotnet": ["bin", "obj", "*.dll", "*.exe", "*.pdb"],
        "go": ["vendor", "*.exe", "*.test"],
    }
    
    exclusiones = exclusiones_base + exclusiones_por_tipo.get(tipo_proyecto, [])
    
    # Contar archivos primero para calcular porcentaje
    items_totales = []
    for item in directorio_actual.iterdir():
        debe_excluir_item = any(item.name == excl or (excl.startswith("*") and item.name.endswith(excl[1:])) for excl in exclusiones)
        if not debe_excluir_item:
            items_totales.append(item)
    
    total_items = len(items_totales)
    
    if callback_progreso:
        callback_progreso(f"Creando versión inicial (0/{total_items})")
    
    for idx, item in enumerate(items_totales, 1):
        porcentaje = int((idx / total_items) * 100) if total_items > 0 else 100
        
        destino = carpeta_version_1 / item.name
        try:
            if callback_progreso:
                callback_progreso(f"{item.name} ({idx}/{total_items} - {porcentaje}%)")
            
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
    
    # Calcular tamaño
    tamaño_bytes = 0
    try:
        for item in carpeta_version_1.rglob('*'):
            if item.is_file():
                tamaño_bytes += item.stat().st_size
    except:
        pass
    
    # Formatear tamaño
    if tamaño_bytes < 1024:
        tamaño_formateado = f"{tamaño_bytes} B"
    elif tamaño_bytes < 1024 * 1024:
        tamaño_formateado = f"{tamaño_bytes / 1024:.1f} KB"
    elif tamaño_bytes < 1024 * 1024 * 1024:
        tamaño_formateado = f"{tamaño_bytes / (1024 * 1024):.1f} MB"
    else:
        tamaño_formateado = f"{tamaño_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    # Crear metadatos de la versión 1
    metadatos = {
        "version": 1,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mensaje": "Versión inicial del proyecto",
        "tipo_proyecto": tipo_proyecto,
        "archivos_guardados": archivos_copiados,
        "archivos_excluidos": archivos_excluidos,
        "tamaño_bytes": tamaño_bytes,
        "tamaño_formateado": tamaño_formateado
    }
    
    with open(carpeta_version_1 / "metadatos.json", "w") as f:
        json.dump(metadatos, f, indent=2)
    
    if callback_progreso:
        callback_progreso("Proyecto creado exitosamente")
    
    print(f"\n  ✓  Proyecto inicializado")
    print(f"  ●  Nombre:   {nombre_proyecto}")
    print(f"  ●  Tipo:     {tipo_proyecto}")
    print(f"  ●  Versión:  v1  ({archivos_copiados} archivos, {tamaño_formateado})")
    print(f"\n  Próximo paso:")
    print(f"  $ cronux guardar \"Versión inicial\"\n")
    
    return True