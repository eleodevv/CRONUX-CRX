#!/usr/bin/env python3
"""
Script de diagnóstico para verificar imports de CLI
"""
import sys
from pathlib import Path

print("=" * 60)
print("DIAGNÓSTICO DE IMPORTS CLI")
print("=" * 60)

print(f"\n📍 __file__ = {__file__}")
print(f"📍 Path(__file__).parent = {Path(__file__).parent}")
print(f"📍 sys.path actual:")
for p in sys.path[:5]:
    print(f"   - {p}")

# Probar diferentes rutas
cli_mismo_dir = Path(__file__).parent / "cli"
cli_data = Path(__file__).parent.parent / "data" / "cli"
cli_parent = Path(__file__).parent.parent / "cli"

print(f"\n🔍 Buscando módulos CLI:")
print(f"   1. {cli_mismo_dir}")
print(f"      Existe: {cli_mismo_dir.exists()}")
if cli_mismo_dir.exists():
    print(f"      Archivos: {list(cli_mismo_dir.glob('*.py'))[:3]}")

print(f"   2. {cli_data}")
print(f"      Existe: {cli_data.exists()}")
if cli_data.exists():
    print(f"      Archivos: {list(cli_data.glob('*.py'))[:3]}")

print(f"   3. {cli_parent}")
print(f"      Existe: {cli_parent.exists()}")
if cli_parent.exists():
    print(f"      Archivos: {list(cli_parent.glob('*.py'))[:3]}")

# Intentar agregar al path
if cli_mismo_dir.exists():
    sys.path.insert(0, str(cli_mismo_dir))
    print(f"\n✅ Agregado al path: {cli_mismo_dir}")
elif cli_data.exists():
    sys.path.insert(0, str(cli_data))
    print(f"\n✅ Agregado al path: {cli_data}")
elif cli_parent.exists():
    sys.path.insert(0, str(cli_parent))
    print(f"\n✅ Agregado al path: {cli_parent}")

# Intentar importar
print(f"\n🔄 Intentando importar módulos...")
try:
    from crear_proyecto import crear_proyecto_cli
    print("   ✅ crear_proyecto importado")
except ImportError as e:
    print(f"   ❌ Error: {e}")

try:
    from guardar_version import guardar_version_cli
    print("   ✅ guardar_version importado")
except ImportError as e:
    print(f"   ❌ Error: {e}")

try:
    from restaurar_versiones import restaurar_version_cli
    print("   ✅ restaurar_versiones importado")
except ImportError as e:
    print(f"   ❌ Error: {e}")

try:
    from funcion_verficar import verificarCronux
    print("   ✅ funcion_verficar importado")
except ImportError as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)
