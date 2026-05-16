# CRONUX-CRX CLI Installer for Windows
# Usage: irm https://raw.githubusercontent.com/eleodevv/CRONUX-CRX/main/cronux_cli/install.ps1 | iex

$ErrorActionPreference = "Stop"

$REPO = "eleodevv/CRONUX-CRX"
$VERSION = "v0.2.3"
$INSTALL_DIR = "$env:ProgramFiles\Cronux-CRX"
$CLI_DIR = "$INSTALL_DIR\cli"

# Colors
function Write-Color {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

Write-Host ""
Write-Color "   ██████╗██████╗  ██████╗ ███╗  ██╗██╗   ██╗██╗  ██╗" "Cyan"
Write-Color "  ██╔════╝██╔══██╗██╔═══██╗████╗ ██║██║   ██║╚██╗██╔╝" "Cyan"
Write-Color "  ██║     ██████╔╝██║   ██║██╔██╗██║██║   ██║ ╚███╔╝ " "Cyan"
Write-Color "  ██║     ██╔══██╗██║   ██║██║╚████║██║   ██║ ██╔██╗ " "Cyan"
Write-Color "  ╚██████╗██║  ██║╚██████╔╝██║ ╚███║╚██████╔╝██╔╝╚██╗" "Cyan"
Write-Color "   ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚══╝ ╚═════╝ ╚═╝  ╚═╝" "Cyan"
Write-Color "              Control de Versiones  $VERSION" "Gray"
Write-Host ""

# Verificar permisos de administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Color "✗ Este script requiere permisos de administrador" "Red"
    Write-Color "  Ejecuta PowerShell como Administrador y vuelve a intentar" "Yellow"
    exit 1
}

Write-Color "  Plataforma: Windows" "Gray"
Write-Color "  Versión:    $VERSION" "Gray"
Write-Color "  Destino:    $INSTALL_DIR" "Gray"
Write-Host ""

# Verificar Python
try {
    $pythonVersion = (python --version 2>&1) -replace "Python ", ""
    Write-Color "  ✓ Python $pythonVersion encontrado" "Green"
} catch {
    Write-Color "✗ Python 3 no encontrado. Instálalo desde python.org" "Red"
    exit 1
}

# Crear directorio de instalación
Write-Color "  → Creando directorio de instalación..." "Gray"
New-Item -ItemType Directory -Force -Path $CLI_DIR | Out-Null

# Descargar archivos del CLI
Write-Color "  → Descargando CRONUX-CRX CLI..." "Gray"

$BASE_URL = "https://raw.githubusercontent.com/$REPO/main/cronux_cli/cli"
$CLI_FILES = @(
    "cronux_cli.py",
    "crear_proyecto.py",
    "guardar_version.py",
    "ver_historial.py",
    "restaurar_versiones.py",
    "eliminar_proyecto.py",
    "info_proyecto.py",
    "funcion_verficar.py"
)

foreach ($file in $CLI_FILES) {
    $url = "$BASE_URL/$file"
    $dest = "$CLI_DIR\$file"
    try {
        Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing | Out-Null
    } catch {
        Write-Color "  ⚠ No se pudo descargar $file" "Yellow"
    }
}

Write-Color "  ✓ Archivos descargados" "Green"

# Crear script batch ejecutable
Write-Color "  → Creando comando 'cronux'..." "Gray"
$batchContent = @"
@echo off
python "$CLI_DIR\cronux_cli.py" %*
"@
$batchPath = "$INSTALL_DIR\cronux.bat"
Set-Content -Path $batchPath -Value $batchContent -Encoding ASCII

# Agregar al PATH del sistema
Write-Color "  → Agregando al PATH del sistema..." "Gray"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($currentPath -notlike "*$INSTALL_DIR*") {
    $newPath = "$currentPath;$INSTALL_DIR"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
    Write-Color "  ✓ Agregado al PATH" "Green"
} else {
    Write-Color "  ✓ Ya está en el PATH" "Green"
}

# Actualizar PATH en la sesión actual
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine")

# Verificar instalación
Write-Host ""
Write-Color "✓ CRONUX-CRX CLI instalado correctamente" "Green" -NoNewline
Write-Host ""
Write-Host ""
Write-Color "  IMPORTANTE: Cierra y abre una nueva terminal" "Yellow"
Write-Color "  Luego ejecuta: " "Gray" -NoNewline
Write-Color "cronux ayuda" "Cyan"
Write-Host ""
