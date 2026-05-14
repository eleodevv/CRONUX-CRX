#!/usr/bin/env python3
"""
Genera el icono de CRONUX-CRX
Hexágono blanco sobre fondo azul/morado
"""

from PIL import Image, ImageDraw
import math

def create_hexagon_icon(size=256):
    """Crea un icono con hexágono blanco sobre fondo azul"""
    
    # Crear imagen con fondo transparente
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fondo azul/morado redondeado
    corner_radius = int(size * 0.28)  # 28% del tamaño
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill='#667EEA'
    )
    
    # Calcular puntos del hexágono
    center_x = size / 2
    center_y = size / 2
    hex_size = size * 0.35  # 35% del tamaño total
    
    points = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6  # Rotar 30 grados
        x = center_x + hex_size * math.cos(angle)
        y = center_y + hex_size * math.sin(angle)
        points.append((x, y))
    
    # Dibujar hexágono blanco
    draw.polygon(points, fill='#FFFFFF')
    
    return img

def main():
    """Genera los iconos en diferentes tamaños"""
    
    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
    
    print("Generando iconos CRONUX-CRX...")
    
    # Generar PNG en diferentes tamaños
    for size in sizes:
        icon = create_hexagon_icon(size)
        filename = f"cronux_cli/assets/cronux_icon_{size}.png"
        icon.save(filename, 'PNG')
        print(f"✓ Creado: {filename}")
    
    # Crear el icono principal
    icon_main = create_hexagon_icon(256)
    icon_main.save("cronux_cli/assets/cronux_icon.png", 'PNG')
    print(f"✓ Creado: cronux_cli/assets/cronux_icon.png")
    
    # Crear .ico para Windows (múltiples tamaños)
    try:
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icons = [create_hexagon_icon(s[0]) for s in icon_sizes]
        icons[0].save(
            "cronux_cli/assets/cronux_icon.ico",
            format='ICO',
            sizes=icon_sizes
        )
        print(f"✓ Creado: cronux_cli/assets/cronux_icon.ico")
    except Exception as e:
        print(f"⚠ No se pudo crear .ico: {e}")
    
    # Crear .icns para macOS
    try:
        import subprocess
        import os
        
        # Crear iconset
        iconset_dir = "cronux_cli/assets/cronux_icon.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        
        # Tamaños requeridos para macOS
        mac_sizes = [
            (16, "icon_16x16.png"),
            (32, "icon_16x16@2x.png"),
            (32, "icon_32x32.png"),
            (64, "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024, "icon_512x512@2x.png"),
        ]
        
        for size, name in mac_sizes:
            icon = create_hexagon_icon(size)
            icon.save(f"{iconset_dir}/{name}", 'PNG')
        
        # Convertir a .icns (solo en macOS)
        if os.system("which iconutil > /dev/null 2>&1") == 0:
            subprocess.run([
                "iconutil", "-c", "icns",
                iconset_dir,
                "-o", "cronux_cli/assets/cronux_icon.icns"
            ])
            print(f"✓ Creado: cronux_cli/assets/cronux_icon.icns")
        else:
            print(f"⚠ iconutil no disponible (solo macOS)")
            
    except Exception as e:
        print(f"⚠ No se pudo crear .icns: {e}")
    
    print("\n✅ Iconos generados correctamente")

if __name__ == "__main__":
    main()
