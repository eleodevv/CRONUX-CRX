from pathlib import Path
from funcion_verficar import * 
import json
import shutil
import subprocess
import sys

# Comandos de instalación por tipo de proyecto
COMANDOS_INSTALACION = {
    "nodejs": {
        "comando": "npm install",  # Se sobrescribe dinámicamente
        "archivos_requeridos": ["package.json"],
        "descripcion": "Instalando dependencias de Node.js..."
    },
    "react": {
        "comando": "npm install --legacy-peer-deps",
        "archivos_requeridos": ["package.json"],
        "descripcion": "Instalando dependencias de React..."
    },
    "vue": {
        "comando": "npm install",
        "archivos_requeridos": ["package.json"],
        "descripcion": "Instalando dependencias de Vue.js..."
    },
    "angular": {
        "comando": "npm install",
        "archivos_requeridos": ["package.json"],
        "descripcion": "Instalando dependencias de Angular..."
    },
    "nextjs": {
        "comando": "npm install",
        "archivos_requeridos": ["package.json"],
        "descripcion": "Instalando dependencias de Next.js..."
    },
    "python": {
        "comando": "pip install -r requirements.txt",
        "archivos_requeridos": ["requirements.txt"],
        "descripcion": "Instalando dependencias de Python..."
    },
    "java_maven": {
        "comando": "mvn install",
        "archivos_requeridos": ["pom.xml"],
        "descripcion": "Instalando dependencias de Maven..."
    },
    "java_gradle": {
        "comando": "gradle build",
        "archivos_requeridos": ["build.gradle"],
        "descripcion": "Instalando dependencias de Gradle..."
    },
    "php": {
        "comando": "composer install",
        "archivos_requeridos": ["composer.json"],
        "descripcion": "Instalando dependencias de PHP..."
    },
    "ruby": {
        "comando": "bundle install",
        "archivos_requeridos": ["Gemfile"],
        "descripcion": "Instalando dependencias de Ruby..."
    },
    "dotnet": {
        "comando": "dotnet restore",
        "archivos_requeridos": ["*.csproj", "*.sln"],
        "descripcion": "Restaurando dependencias de .NET..."
    },
    "go": {
        "comando": "go mod download",
        "archivos_requeridos": ["go.mod"],
        "descripcion": "Descargando dependencias de Go..."
    }
}

def instalar_dependencias(tipo_proyecto, callback_progreso=None):
    """Instala las dependencias según el tipo de proyecto"""
    if tipo_proyecto not in COMANDOS_INSTALACION:
        if callback_progreso:
            callback_progreso(f"Tipo de proyecto '{tipo_proyecto}' no requiere instalación de dependencias")
        return True
    
    config = COMANDOS_INSTALACION[tipo_proyecto]
    
    # Verificar si existen los archivos requeridos
    archivos_encontrados = False
    archivo_encontrado_nombre = None
    for archivo_patron in config["archivos_requeridos"]:
        if "*" in archivo_patron:
            # Patrón con wildcard
            archivos = list(Path.cwd().glob(archivo_patron))
            if archivos:
                archivos_encontrados = True
                archivo_encontrado_nombre = archivos[0].name
                break
        else:
            # Archivo específico
            if (Path.cwd() / archivo_patron).exists():
                archivos_encontrados = True
                archivo_encontrado_nombre = archivo_patron
                break
    
    if not archivos_encontrados:
        if callback_progreso:
            callback_progreso(f"⚠ No se encontró {', '.join(config['archivos_requeridos'])} - omitiendo instalación")
        return True
    
    # Para Node.js y frameworks basados en Node (React, Vue, Angular, etc), verificar package-lock.json
    comando_a_usar = config["comando"]
    if tipo_proyecto in ["nodejs", "react", "vue", "angular", "nextjs"]:
        package_lock = Path.cwd() / "package-lock.json"
        # Siempre usar npm install en lugar de npm ci para evitar problemas
        if tipo_proyecto == "react":
            comando_a_usar = "npm install --legacy-peer-deps"
        else:
            comando_a_usar = "npm install --legacy-peer-deps"
        
        if callback_progreso:
            if package_lock.exists():
                callback_progreso("Instalando dependencias con lock file")
            else:
                callback_progreso("Instalando dependencias")
    
    # Ejecutar comando de instalación
    try:
        if callback_progreso:
            callback_progreso(f"🔧 {config['descripcion']}")
            callback_progreso(f"Ejecutando: {comando_a_usar}")
        
        print(f"Ejecutando: {comando_a_usar} en {Path.cwd()}")
        
        resultado = subprocess.run(
            comando_a_usar,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            timeout=600  # 10 minutos timeout
        )
        
        print(f"Return code: {resultado.returncode}")
        if resultado.stdout:
            print(f"STDOUT (primeras 500 chars): {resultado.stdout[:500]}")
            if callback_progreso and resultado.stdout:
                # Mostrar las últimas líneas del output
                lineas = resultado.stdout.strip().split('\n')
                for linea in lineas[-5:]:  # Últimas 5 líneas
                    if linea.strip():
                        callback_progreso(linea.strip()[:100])
        
        if resultado.stderr:
            print(f"STDERR (primeras 500 chars): {resultado.stderr[:500]}")
            # Mostrar warnings importantes
            if callback_progreso and resultado.stderr:
                lineas_stderr = resultado.stderr.strip().split('\n')
                for linea in lineas_stderr[-3:]:
                    if linea.strip() and ('error' in linea.lower() or 'warn' in linea.lower()):
                        callback_progreso(f"⚠ {linea.strip()[:100]}")
        
        if resultado.returncode == 0:
            if callback_progreso:
                callback_progreso("Dependencias instaladas correctamente")
            print("✓ npm install completado exitosamente")
            
            # Pequeña pausa para asegurar que todos los archivos se escribieron
            import time
            time.sleep(2)
            
            return True
        else:
            error_msg = resultado.stderr[:200] if resultado.stderr else "Error desconocido"
            if callback_progreso:
                callback_progreso(f"⚠ Error al instalar dependencias")
                callback_progreso(f"Código de error: {resultado.returncode}")
            print(f"✗ Error instalando dependencias (código {resultado.returncode})")
            print(f"STDERR completo: {resultado.stderr}")
            return False
    except subprocess.TimeoutExpired:
        if callback_progreso:
            callback_progreso("⚠ Timeout: La instalación tardó más de 10 minutos")
        print("✗ Timeout en npm install")
        return False
    except Exception as e:
        if callback_progreso:
            callback_progreso(f"⚠ Error: {str(e)[:100]}")
        print(f"✗ Excepción instalando dependencias: {e}")
        import traceback
        traceback.print_exc()
        return False

def restaurar_version_cli(version_elegida, auto_instalar=True, callback_progreso=None):
    """Versión CLI que recibe la versión como parámetro y opcionalmente instala dependencias"""
    if not verificarCronux():
        print("ERROR: No estas en un proyecto Cronux")
        return False
    
    # Limpiar la 'v' si viene incluida
    if version_elegida.startswith('v'):
        version_elegida = version_elegida[1:]
    
    # Verificar que la versión existe
    carpeta_version = obtener_ruta_cronux() / "versiones" / f"version_{version_elegida}"
    
    if not carpeta_version.exists():
        print(f"ERROR: La version '{version_elegida}' no existe")
        print("Usa 'cronux log' para ver las versiones disponibles")
        return False
    
    # Leer metadatos si existen
    tipo_proyecto = "general"
    metadatos_file = carpeta_version / "metadatos.json"
    if metadatos_file.exists():
        try:
            with open(metadatos_file, "r") as f:
                metadatos = json.load(f)
            tipo_proyecto = metadatos.get("tipo_proyecto", "general")
            print(f"Restaurando version {version_elegida}:")
            print(f"Tipo: {tipo_proyecto}")
            print(f"Fecha: {metadatos['fecha']}")
            print(f"Mensaje: {metadatos['mensaje']}")
        except Exception as e:
            print(f"Advertencia: Error leyendo metadatos: {e}")
    
    # Confirmar restauración (solo en modo CLI interactivo)
    # Si hay callback_progreso, significa que se llama desde UI y no debe pedir confirmación
    if callback_progreso is None or not callable(callback_progreso):
        respuesta = input(f"¿Confirmas restaurar la version {version_elegida}? (s/N): ")
        if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
            print("Operación cancelada")
            return False
    
    # Limpiar directorio actual (excepto .cronux)
    directorio_actual = Path.cwd()
    archivos_eliminados = 0
    
    if callback_progreso:
        callback_progreso("Limpiando directorio actual")
    
    for item in directorio_actual.iterdir():
        if item.name != ".cronux" and not item.name.startswith('.git'):
            try:
                if callback_progreso:
                    callback_progreso(f"Eliminando {item.name}")
                
                if item.is_file():
                    item.unlink()
                    archivos_eliminados += 1
                elif item.is_dir():
                    shutil.rmtree(item)
                    archivos_eliminados += 1
            except Exception as e:
                error_msg = f"No se pudo eliminar {item.name}: {e}"
                print(f"Advertencia: {error_msg}")
                if callback_progreso:
                    callback_progreso(f"⚠ {error_msg}")
    
    # Restaurar archivos de la versión
    archivos_restaurados = 0
    
    # Contar total de archivos primero para calcular porcentaje
    total_archivos = sum(1 for item in carpeta_version.iterdir() if item.name != "metadatos.json")
    
    if callback_progreso:
        callback_progreso(f"Restaurando archivos (0/{total_archivos})")
    
    for item in carpeta_version.iterdir():
        if item.name != "metadatos.json":
            destino = directorio_actual / item.name
            try:
                archivos_restaurados += 1
                porcentaje = int((archivos_restaurados / total_archivos) * 100)
                
                if callback_progreso:
                    callback_progreso(f"{item.name} ({archivos_restaurados}/{total_archivos} - {porcentaje}%)")
                
                if item.is_file():
                    shutil.copy2(item, destino)
                elif item.is_dir():
                    shutil.copytree(item, destino)
            except Exception as e:
                error_msg = f"Error restaurando {item.name}: {e}"
                print(error_msg)
                if callback_progreso:
                    callback_progreso(f"⚠ {error_msg}")
    
    print(f"[OK] Version {version_elegida} restaurada")
    print(f"Archivos eliminados: {archivos_eliminados}")
    print(f"Archivos restaurados: {archivos_restaurados}")
    
    # Mostrar instrucciones según el tipo de proyecto
    if tipo_proyecto in ["nodejs", "react", "vue", "angular", "nextjs"]:
        print("\n" + "="*50)
        if tipo_proyecto == "react":
            print("⚛️  PROYECTO REACT RESTAURADO")
        elif tipo_proyecto == "vue":
            print("💚 PROYECTO VUE.JS RESTAURADO")
        elif tipo_proyecto == "angular":
            print("🅰️  PROYECTO ANGULAR RESTAURADO")
        elif tipo_proyecto == "nextjs":
            print("▲ PROYECTO NEXT.JS RESTAURADO")
        else:
            print("📦 PROYECTO NODE.JS RESTAURADO")
        print("="*50)
        print("Para ejecutar el proyecto:")
        print("  1. cd " + str(directorio_actual))
        if tipo_proyecto == "nextjs":
            print("  2. npm run dev")
        else:
            print("  2. npm start")
        print("="*50 + "\n")
    elif tipo_proyecto == "python":
        print("\n" + "="*50)
        print("🐍 PROYECTO PYTHON RESTAURADO")
        print("="*50)
        print("Para ejecutar el proyecto:")
        print("  1. cd " + str(directorio_actual))
        print("  2. python main.py")
        print("="*50 + "\n")
    
    # Instalar dependencias automáticamente
    if auto_instalar and tipo_proyecto != "general":
        print(f"DEBUG: Intentando instalar dependencias para tipo: {tipo_proyecto}")
        
        # Para Node.js y frameworks basados en Node, detener procesos en ejecución primero
        if tipo_proyecto in ["nodejs", "react", "vue", "angular", "nextjs"]:
            if callback_progreso:
                callback_progreso("Deteniendo procesos de Node.js")
            try:
                # Matar procesos de node que estén corriendo en este directorio
                subprocess.run(
                    "pkill -f 'node.*react-scripts' || true",
                    shell=True,
                    capture_output=True,
                    timeout=5
                )
                subprocess.run(
                    "pkill -f 'npm.*start' || true",
                    shell=True,
                    capture_output=True,
                    timeout=5
                )
                if callback_progreso:
                    callback_progreso("Procesos detenidos")
                print("✓ Procesos de Node.js detenidos")
            except Exception as e:
                print(f"⚠ Error deteniendo procesos: {e}")
            
            # Eliminar node_modules
            node_modules = directorio_actual / "node_modules"
            if node_modules.exists():
                if callback_progreso:
                    callback_progreso("Limpiando node_modules anterior")
                try:
                    shutil.rmtree(node_modules)
                    print("✓ node_modules eliminado")
                    if callback_progreso:
                        callback_progreso("node_modules eliminado")
                except Exception as e:
                    print(f"⚠ Error eliminando node_modules: {e}")
            
            # Limpiar cache de npm
            if callback_progreso:
                callback_progreso("Limpiando cache de npm")
            try:
                resultado_cache = subprocess.run(
                    "npm cache clean --force",
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=Path.cwd(),
                    timeout=30
                )
                if resultado_cache.returncode == 0:
                    if callback_progreso:
                        callback_progreso("Cache de npm limpiado")
                    print("✓ Cache de npm limpiado")
            except Exception as e:
                print(f"⚠ Error limpiando cache: {e}")
        
        if callback_progreso:
            callback_progreso(f"Preparando instalación para {tipo_proyecto}")
        resultado_instalacion = instalar_dependencias(tipo_proyecto, callback_progreso)
        if resultado_instalacion:
            print(f"DEBUG: Dependencias instaladas exitosamente")
            if callback_progreso:
                callback_progreso("Restauración completada")
                if tipo_proyecto in ["nodejs", "react", "vue", "angular", "nextjs"]:
                    if tipo_proyecto == "nextjs":
                        callback_progreso("Ejecuta: npm run dev")
                    else:
                        callback_progreso("Ejecuta: npm start")
        else:
            print(f"DEBUG: Falló la instalación de dependencias")
            if callback_progreso:
                callback_progreso("⚠ Error en instalación automática")
                callback_progreso("📝 Ejecuta manualmente: npm install --legacy-peer-deps")
    else:
        print(f"DEBUG: No se instalaron dependencias. auto_instalar={auto_instalar}, tipo={tipo_proyecto}")
    
    return True