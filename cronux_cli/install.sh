#!/bin/bash
# CRONUX-CRX CLI Installer for Linux/macOS
# Usage: curl -fsSL https://raw.githubusercontent.com/eleodevv/CRONUX-CRX/main/install.sh | bash

set -e

REPO="eleodevv/CRONUX-CRX"
VERSION="v0.2.3"
INSTALL_DIR="/usr/local/cronux"
BIN_DIR="/usr/local/bin"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
GRAY='\033[0;90m'
BOLD='\033[1m'
RESET='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}"
echo "   ██████╗██████╗  ██████╗ ███╗  ██╗██╗   ██╗██╗  ██╗"
echo "  ██╔════╝██╔══██╗██╔═══██╗████╗ ██║██║   ██║╚██╗██╔╝"
echo "  ██║     ██████╔╝██║   ██║██╔██╗██║██║   ██║ ╚███╔╝ "
echo "  ██║     ██╔══██╗██║   ██║██║╚████║██║   ██║ ██╔██╗ "
echo "  ╚██████╗██║  ██║╚██████╔╝██║ ╚███║╚██████╔╝██╔╝╚██╗"
echo "   ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚══╝ ╚═════╝ ╚═╝  ╚═╝"
echo -e "${RESET}${GRAY}              Control de Versiones  ${VERSION}${RESET}"
echo ""

# Detectar OS
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="Linux" ;;
    Darwin*) PLATFORM="macOS" ;;
    *)       echo -e "${RED}✗ Sistema operativo no soportado: $OS${RESET}"; exit 1 ;;
esac

echo -e "  ${GRAY}Plataforma:${RESET} $PLATFORM"
echo -e "  ${GRAY}Versión:${RESET}    $VERSION"
echo -e "  ${GRAY}Destino:${RESET}    $INSTALL_DIR"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 no encontrado. Instálalo primero.${RESET}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "  ${GREEN}✓${RESET} Python $PYTHON_VERSION encontrado"

# Crear directorio de instalación
echo -e "  ${GRAY}→${RESET} Creando directorio de instalación..."
sudo mkdir -p "$INSTALL_DIR/cli"

# Descargar archivos del CLI
echo -e "  ${GRAY}→${RESET} Descargando CRONUX-CRX CLI..."

BASE_URL="https://raw.githubusercontent.com/${REPO}/main/cronux_cli/cli"
CLI_FILES=(
    "cronux_cli.py"
    "crear_proyecto.py"
    "guardar_version.py"
    "ver_historial.py"
    "restaurar_versiones.py"
    "eliminar_proyecto.py"
    "info_proyecto.py"
    "funcion_verficar.py"
    "guardar_version.py"
)

for f in "${CLI_FILES[@]}"; do
    sudo curl -fsSL "${BASE_URL}/${f}" -o "${INSTALL_DIR}/cli/${f}" 2>/dev/null || true
done

echo -e "  ${GREEN}✓${RESET} Archivos descargados"

# Crear script ejecutable
echo -e "  ${GRAY}→${RESET} Creando comando 'cronux'..."
sudo tee "$INSTALL_DIR/cronux" > /dev/null << EOF
#!/bin/bash
python3 "$INSTALL_DIR/cli/cronux_cli.py" "\$@"
EOF
sudo chmod +x "$INSTALL_DIR/cronux"
sudo ln -sf "$INSTALL_DIR/cronux" "$BIN_DIR/cronux"

echo -e "  ${GREEN}✓${RESET} Comando 'cronux' creado en $BIN_DIR"

# Verificar instalación
echo ""
if command -v cronux &> /dev/null; then
    echo -e "${GREEN}${BOLD}✓ CRONUX-CRX CLI instalado correctamente${RESET}"
    echo ""
    echo -e "  Prueba con: ${CYAN}cronux ayuda${RESET}"
    echo ""
else
    echo -e "${GREEN}✓ Instalación completada${RESET}"
    echo -e "  Reinicia la terminal y ejecuta: ${CYAN}cronux ayuda${RESET}"
    echo ""
fi
