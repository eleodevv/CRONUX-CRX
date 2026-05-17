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

# Verificar Python e instalar si no está
Write-Color "  → Verificando Python..." "Gray"
$pythonOk = $false
try {
    $pythonVersion = (python --version 2>&1) -replace "Python ", ""
    if ($pythonVersion -match "^\d") {
        Write-Color "  ✓ Python $pythonVersion encontrado" "Green"
        $pythonOk = $true
    }
} catch { }

if (-not $pythonOk) {
    Write-Color "  ⚠ Python no encontrado. Instalando automáticamente..." "Yellow"
    
    $pythonInstaller = "$env:TEMP\python_installer.exe"
    $pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
    
    try {
        Write-Color "  → Descargando Python 3.11..." "Gray"
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
        
        Write-Color "  → Instalando Python 3.11 (puede tardar un momento)..." "Gray"
        $proc = Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait -PassThru
        
        if ($proc.ExitCode -eq 0) {
            # Recargar PATH para que python esté disponible
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
            Write-Color "  ✓ Python instalado correctamente" "Green"
        } else {
            Write-Color "✗ Error instalando Python (código $($proc.ExitCode))" "Red"
            Write-Color "  Instálalo manualmente desde https://python.org y vuelve a ejecutar este script" "Yellow"
            exit 1
        }
        
        Remove-Item $pythonInstaller -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Color "✗ No se pudo descargar Python: $_" "Red"
        Write-Color "  Instálalo manualmente desde https://python.org y vuelve a ejecutar este script" "Yellow"
        exit 1
    }
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
Write-Color "✓ CRONUX-CRX CLI instalado correctamente" "Green"
Write-Host ""
Write-Color "  IMPORTANTE: Cierra y abre una nueva terminal" "Yellow"
Write-Color "  Luego ejecuta: cronux ayuda" "Cyan"
Write-Host ""
