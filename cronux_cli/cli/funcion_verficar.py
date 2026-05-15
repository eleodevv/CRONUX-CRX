from pathlib import Path
import json

def verificarCronux():
    """Verifica si estamos en un proyecto Cronux"""
    carpeta_cronux = Path.cwd() / ".cronux"
    archivo_proyecto = carpeta_cronux / "proyecto.json"
    return carpeta_cronux.exists() and archivo_proyecto.exists()

def obtener_ruta_cronux():
    """Obtiene la ruta de la carpeta .cronux"""
    return Path.cwd() / ".cronux"

def obtener_ruta_proyecto_json():
    """Obtiene la ruta del archivo proyecto.json"""
    return obtener_ruta_cronux() / "proyecto.json"

def determinar_numero_version():
    """Determina el siguiente número de versión"""
    carpeta_versiones = obtener_ruta_cronux() / "versiones"
    
    if not carpeta_versiones.exists():
        return 1
    
    versiones = list(carpeta_versiones.glob("version_*"))
    
    if not versiones:
        return 1
    
    # Extraer números de versión
    numeros = []
    for version_dir in versiones:
        try:
            numero_str = version_dir.name.replace("version_", "")
            # Convertir a int (ya deberían estar migradas)
            numero = int(float(numero_str))
            numeros.append(numero)
        except (ValueError, TypeError):
            continue
    
    if not numeros:
        return 1
    
    # Retornar el siguiente número
    return max(numeros) + 1


def migrar_versiones_a_enteros(silencioso=False):
    """Migra versiones con decimales (1.0, 1.1, 1.2) a enteros (1, 2, 3)"""
    import shutil
    import json
    import tempfile
    
    carpeta_versiones = obtener_ruta_cronux() / "versiones"
    
    if not carpeta_versiones.exists():
        if not silencioso:
            print("  ⚠  No hay versiones para migrar")
        return False
    
    # Obtener todas las versiones y ordenarlas
    versiones = []
    for v_dir in sorted(carpeta_versiones.glob("version_*")):
        try:
            numero_str = v_dir.name.replace("version_", "")
            numero = float(numero_str)
            versiones.append((numero, v_dir))
        except (ValueError, TypeError):
            continue
    
    if not versiones:
        if not silencioso:
            print("  ⚠  No hay versiones para migrar")
        return False
    
    # Verificar si hay versiones con decimales
    tiene_decimales = any(num != int(num) for num, _ in versiones)
    
    if not tiene_decimales:
        if not silencioso:
            print("  ✓  Las versiones ya están en formato entero")
        return False  # Ya están en formato entero
    
    if not silencioso:
        print()
        print(f"  ⚙  Migrando versiones al nuevo formato...")
        print(f"  📊 Versiones encontradas: {len(versiones)}")
    
    # Ordenar por número
    versiones.sort(key=lambda x: x[0])
    
    # Usar directorio temporal
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        # Mover todas a temporal con nuevo número
        for nuevo_num, (viejo_num, v_dir) in enumerate(versiones, start=1):
            if not silencioso:
                print(f"  → v{viejo_num} → v{nuevo_num}")
            
            temp_path = temp_dir / f"version_{nuevo_num}"
            shutil.move(str(v_dir), str(temp_path))
            
            # Actualizar metadata
            meta_file = temp_path / "metadatos.json"
            if meta_file.exists():
                with open(meta_file) as f:
                    meta = json.load(f)
                meta["version"] = nuevo_num
                with open(meta_file, "w") as f:
                    json.dump(meta, f, indent=2)
        
        # Mover de temporal a destino
        for nuevo_num in range(1, len(versiones) + 1):
            temp_path = temp_dir / f"version_{nuevo_num}"
            dest_path = carpeta_versiones / f"version_{nuevo_num}"
            shutil.move(str(temp_path), str(dest_path))
        
        # Actualizar version_actual en proyecto.json
        proyecto_json = obtener_ruta_cronux() / "proyecto.json"
        if proyecto_json.exists():
            with open(proyecto_json) as f:
                datos = json.load(f)
            
            # Convertir version_actual a entero
            if "version_actual" in datos:
                try:
                    version_actual_vieja = float(datos["version_actual"])
                    # Encontrar el índice de esta versión en la lista ordenada
                    for nuevo_num, (viejo_num, _) in enumerate(versiones, start=1):
                        if abs(viejo_num - version_actual_vieja) < 0.01:  # Comparación con tolerancia
                            datos["version_actual"] = nuevo_num
                            if not silencioso:
                                print(f"  ✓  Versión actual: v{version_actual_vieja} → v{nuevo_num}")
                            break
                except:
                    datos["version_actual"] = len(versiones)  # Última versión por defecto
            
            with open(proyecto_json, "w") as f:
                json.dump(datos, f, indent=2)
        
        if not silencioso:
            print()
            print(f"  ✓  Migración completada: {len(versiones)} versiones convertidas")
            print()
        
        return True
        
    except Exception as e:
        if not silencioso:
            print(f"  ✗  Error durante la migración: {e}")
        return False
        
    finally:
        # Limpiar directorio temporal
        if temp_dir.exists():
            shutil.rmtree(temp_dir)