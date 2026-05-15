"""
Pantalla de Proyecto V2 - Diseño minimalista con dock de navegación
"""
import flet as ft
import threading
from pathlib import Path
import sys

# Agregar el directorio cli al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cli"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli_integration import guardar_version_ui, restaurar_version_ui, eliminar_proyecto_ui, abrir_carpeta_proyecto, exportar_proyecto_ui
from components.loader import LoaderView


class ProjectScreenV2:
    """Pantalla de proyecto con dock de navegación"""
    
    def __init__(self, page: ft.Page, proyecto, on_back, on_refresh=None):
        self.page = page
        self.proyecto = proyecto
        self.on_back = on_back
        self.on_refresh = on_refresh
        self.current_view = "versiones"  # versiones, estadisticas, configuracion
        self._operation_completed = False  # Flag para indicar que la operación terminó
        self._update_timer = None  # Timer para forzar actualizaciones
    
    def build(self):
        """Construye la pantalla de proyecto"""
        return ft.Container(
            content=ft.Column([
                # Header minimalista
                self._build_header(),
                
                # Contenido principal (cambia según la vista)
                ft.Container(
                    content=self._build_content(),
                    expand=True,
                    bgcolor="#F7FAFC",
                ),
                
                # Dock de navegación
                self._build_dock(),
                
            ], spacing=0),
            expand=True,
            bgcolor="#FFFFFF",
        )
    
    def _build_header(self):
        """Header minimalista sin botones de acción"""
        icono_src = self.proyecto.get("icono")
        tipo = self.proyecto.get("tipo", "general")
        ruta = self.proyecto.get("ruta", "")
        
        # Mapeo de tipos a iconos de Flet cuando no hay PNG
        iconos_flet = {
            "tareas": ft.Icons.ASSIGNMENT_ROUNDED,
            "investigacion": ft.Icons.SCIENCE_ROUNDED,
            "diseno": ft.Icons.PALETTE_ROUNDED,
        }
        
        # Determinar qué icono usar
        if icono_src:
            icono_widget = ft.Image(src=icono_src, width=24, height=24)
        elif tipo.lower() in iconos_flet:
            icono_widget = ft.Icon(iconos_flet[tipo.lower()], size=22, color="#667EEA")
        else:
            icono_widget = ft.Icon(ft.Icons.FOLDER, size=20, color="#667EEA")
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    # Botón volver
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_ROUNDED,
                        icon_color="#718096",
                        icon_size=22,
                        on_click=lambda _: self.on_back(),
                        tooltip="Volver",
                    ),
                    
                    ft.Container(width=8),
                    
                    # Icono y nombre
                    ft.Container(
                        content=icono_widget,
                        width=44,
                        height=44,
                        border_radius=10,
                        bgcolor="#EDF2F7",
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                    
                    ft.Container(width=12),
                    
                    ft.Column([
                        ft.Text(
                            self.proyecto.get("nombre", "Proyecto"),
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#2D3748",
                        ),
                        ft.Row([
                            ft.Icon(ft.Icons.FOLDER_OUTLINED, size=12, color="#A0AEC0"),
                            ft.Container(width=4),
                            ft.Text(
                                ruta,
                                size=11,
                                color="#A0AEC0",
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ], spacing=0),
                    ], spacing=2),
                    
                    ft.Container(expand=True),
                    
                    # Solo botón Guardar Versión (visible en vista de versiones)
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SAVE_OUTLINED, size=16, color="#FFFFFF"),
                            ft.Container(width=6),
                            ft.Text("Guardar", size=13, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                        ], spacing=0),
                        on_click=lambda _: self._save_version(),
                        style=ft.ButtonStyle(
                            bgcolor="#667EEA",
                            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                            shape=ft.RoundedRectangleBorder(radius=8),
                            elevation=0,
                        ),
                    ) if self.current_view == "versiones" else ft.Container(),
                    
                ]),
            ], spacing=0),
            padding=ft.Padding.symmetric(horizontal=20, vertical=16),
            bgcolor="#FFFFFF",
            border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
        )
    
    def _build_content(self):
        """Construye el contenido según la vista actual"""
        if self.current_view == "versiones":
            return self._build_versiones_view()
        elif self.current_view == "estadisticas":
            return self._build_estadisticas_view()
        else:
            # Si por alguna razón se intenta acceder a configuración, mostrar versiones
            return self._build_versiones_view()
    
    def _build_versiones_view(self):
        """Vista de versiones con diseño moderno tipo cards"""
        versiones = self.proyecto.get("versiones", [])
        
        if not versiones:
            # Estado vacío con diseño mejorado
            return ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.LAYERS_ROUNDED, size=64, color="#667EEA"),
                        width=140,
                        height=140,
                        border_radius=70,
                        bgcolor="#EEF2FF",
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                    ft.Container(height=28),
                    ft.Text(
                        "No hay versiones guardadas",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        "Guarda tu primera versión para comenzar a rastrear cambios",
                        size=15,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=32),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SAVE_ROUNDED, size=18, color="#FFFFFF"),
                            ft.Container(width=10),
                            ft.Text("Guardar Primera Versión", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        on_click=lambda _: self._save_version(),
                        style=ft.ButtonStyle(
                            bgcolor="#667EEA",
                            padding=ft.Padding.symmetric(horizontal=28, vertical=16),
                            shape=ft.RoundedRectangleBorder(radius=12),
                            elevation=0,
                        ),
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                alignment=ft.alignment.Alignment(0, 0),
            )
        
        # Grid de versiones con cards modernas
        version_actual_proyecto = self.proyecto.get('version_actual', 1)
        
        return ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                
                # Header con contador
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LAYERS_ROUNDED, size=20, color="#667EEA"),
                        ft.Container(width=10),
                        ft.Text(
                            f"{len(versiones)} Versión{'es' if len(versiones) != 1 else ''}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#1A202C",
                        ),
                    ]),
                    padding=ft.Padding.symmetric(horizontal=32),
                ),
                
                ft.Container(height=24),
                
                # Grid de versiones
                ft.Container(
                    content=ft.Column([
                        self._build_modern_version_card(v, version_actual_proyecto)
                        for v in versiones
                    ], spacing=16),
                    padding=ft.Padding.symmetric(horizontal=32),
                ),
                
                ft.Container(height=100),
                
            ], scroll=ft.ScrollMode.AUTO),
            expand=True,
        )
    
    def _build_modern_version_card(self, version, version_actual):
        """Card moderna para cada versión - más grande y completamente clickable"""
        numero_version = version.get('numero', 1)
        is_current = numero_version == version_actual
        
        # Obtener el número más alto de versión (convertir a int para comparar)
        versiones_numeros = []
        for v in self.proyecto.get("versiones", []):
            try:
                versiones_numeros.append(int(v.get('numero', 0)))
            except (ValueError, TypeError):
                versiones_numeros.append(0)
        
        max_version = max(versiones_numeros) if versiones_numeros else 1
        
        try:
            is_latest = int(numero_version) == max_version
        except (ValueError, TypeError):
            is_latest = False
        
        return ft.Container(
            content=ft.Column([
                # Header de la card
                ft.Row([
                    # Badge de versión más grande
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.TAG_ROUNDED, size=20, color="#667EEA"),
                            ft.Container(width=8),
                            ft.Text(
                                f"v{numero_version}",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#667EEA",
                            ),
                        ]),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                        border_radius=10,
                        bgcolor="#EEF2FF",
                    ),
                    
                    ft.Container(width=12),
                    
                    # Badge ACTUAL
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=16, color="#FFFFFF"),
                            ft.Container(width=6),
                            ft.Text("ACTUAL", size=12, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ]),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        border_radius=8,
                        bgcolor="#EF4444",
                        visible=is_current,
                    ),
                    
                    # Badge ÚLTIMA
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.NEW_RELEASES_ROUNDED, size=16, color="#FFFFFF"),
                            ft.Container(width=6),
                            ft.Text("ÚLTIMA", size=12, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ]),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        border_radius=8,
                        bgcolor="#667EEA",
                        visible=is_latest and not is_current,
                    ),
                    
                    ft.Container(expand=True),
                    
                    # Fecha
                    ft.Row([
                        ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=16, color="#A0AEC0"),
                        ft.Container(width=8),
                        ft.Text(
                            version.get('fecha', 'Hace un momento'),
                            size=14,
                            color="#718096",
                        ),
                    ]),
                ]),
                
                ft.Container(height=20),
                
                # Descripción más grande
                ft.Text(
                    version.get('descripcion', 'Sin descripción'),
                    size=17,
                    color="#1A202C",
                    weight=ft.FontWeight.W_600,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                
                ft.Container(height=24),
                
                # Stats más grandes
                ft.Row([
                    # Archivos
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, size=20, color="#10B981"),
                            ft.Container(width=10),
                            ft.Text(
                                f"{version.get('archivos', 0)} archivo" + ("s" if version.get('archivos', 0) != 1 else ""),
                                size=15,
                                color="#1A202C",
                                weight=ft.FontWeight.W_600,
                            ),
                        ]),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                        border_radius=10,
                        bgcolor="#ECFDF5",
                    ),
                    
                    ft.Container(width=16),
                    
                    # Tamaño
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.FOLDER_ROUNDED, size=20, color="#F59E0B"),
                            ft.Container(width=10),
                            ft.Text(
                                version.get('tamaño', '0 B'),
                                size=15,
                                color="#1A202C",
                                weight=ft.FontWeight.W_600,
                            ),
                        ]),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                        border_radius=10,
                        bgcolor="#FEF3C7",
                    ),
                ]),
                
                ft.Container(height=24),
                
                # Acciones
                ft.Row([
                    # Botón Restaurar
                    ft.Container(
                        content=ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.RESTORE_ROUNDED, size=18, color="#FFFFFF"),
                                ft.Container(width=10),
                                ft.Text("Restaurar", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            on_click=lambda _, v=version: self._restore_version(v),
                            style=ft.ButtonStyle(
                                bgcolor="#667EEA",
                                padding=ft.Padding.symmetric(horizontal=24, vertical=14),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=0,
                            ),
                        ),
                        expand=True,
                    ),
                    
                    ft.Container(width=12),
                    
                    # Botón Abrir Carpeta
                    ft.Container(
                        content=ft.OutlinedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.FOLDER_OPEN_ROUNDED, size=18, color="#10B981"),
                                ft.Container(width=10),
                                ft.Text("Abrir Carpeta", size=15, weight=ft.FontWeight.BOLD, color="#10B981"),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            on_click=lambda _, v=version: self._open_folder(),
                            style=ft.ButtonStyle(
                                side=ft.BorderSide(1.5, "#10B981"),
                                padding=ft.Padding.symmetric(horizontal=24, vertical=14),
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                        expand=True,
                    ),
                    
                    ft.Container(width=12),
                    
                    # Botón Eliminar
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                        icon_color="#EF4444",
                        icon_size=22,
                        on_click=lambda _, v=version: self._delete_version(v),
                        tooltip="Eliminar versión",
                        style=ft.ButtonStyle(
                            bgcolor="#FEF2F2",
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                ]),
                
            ]),
            padding=ft.Padding.all(28),
            border_radius=18,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1.5, "#FCA5A5" if is_current else "#E5E7EB"),
        )
        
        # Guardar referencia para scroll
        self.timeline_scroll = timeline_content
        
        return ft.Container(
            content=timeline_content,
            expand=True,
        )
    
    def _build_version_timeline_item(self, version, index, total):
        """Item de versión en formato timeline simple con puntos conectados usando Canvas"""
        is_latest = index == 0
        is_last = index == total - 1
        numero_version = version.get('numero', 1)
        
        # Detectar versión actual del proyecto (la que está actualmente en uso)
        version_actual_proyecto = self.proyecto.get('version_actual', 1)
        is_current = numero_version == version_actual_proyecto
        
        # Color del nodo: rojo si es actual, azul si es la última, gris si es antigua
        node_color = "#F56565" if is_current else "#667EEA" if is_latest else "#CBD5E0"
        node_bg_color = "#FFF5F5" if is_current else "#EDF2F7"
        
        # Crear la card de versión
        version_card = ft.Container(
            content=ft.Column([
                # Header con número, badge actual y fecha
                ft.Row([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.TAG, size=14, color=node_color),
                            ft.Container(width=6),
                            ft.Text(
                                f"v{numero_version}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=node_color,
                            ),
                        ], spacing=0),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        border_radius=8,
                        bgcolor=node_bg_color,
                    ),
                    
                    ft.Container(width=8),
                    
                    # Badge "ACTUAL" o "ÚLTIMA"
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(
                                ft.Icons.RADIO_BUTTON_CHECKED if is_current else ft.Icons.NEW_RELEASES_OUTLINED,
                                size=12,
                                color=node_color,
                            ),
                            ft.Container(width=4),
                            ft.Text(
                                "ACTUAL" if is_current else "ÚLTIMA",
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=node_color,
                            ),
                        ], spacing=0),
                        padding=ft.Padding.symmetric(horizontal=10, vertical=5),
                        border_radius=6,
                        bgcolor=node_bg_color,
                        border=ft.Border.all(1.5, node_color),
                        visible=is_current or is_latest,
                    ),
                    
                    ft.Container(expand=True),
                    
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME, size=13, color="#A0AEC0"),
                        ft.Container(width=4),
                        ft.Text(
                            version.get("fecha", ""),
                            size=13,
                            color="#718096",
                            weight=ft.FontWeight.W_600,
                        ),
                    ], spacing=0),
                ]),
                
                ft.Container(height=14),
                
                # Descripción
                ft.Text(
                    version.get("descripcion", "Sin descripción"),
                    size=14,
                    color="#1A202C",
                    weight=ft.FontWeight.W_600,
                ),
                
                ft.Container(height=14),
                
                # Metadata con iconos
                ft.Row([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INSERT_DRIVE_FILE_OUTLINED, size=15, color="#667EEA"),
                            ft.Container(width=6),
                            ft.Text(
                                f"{version.get('archivos', 0)} archivo{'s' if version.get('archivos', 0) != 1 else ''}",
                                size=13,
                                color="#2D3748",
                                weight=ft.FontWeight.BOLD,
                            ),
                        ], spacing=0),
                        padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                        border_radius=8,
                        bgcolor="#EDF2F7",
                    ),
                    ft.Container(width=10),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.STORAGE_OUTLINED, size=15, color="#48BB78"),
                            ft.Container(width=6),
                            ft.Text(
                                version.get("tamaño", "0 B"),
                                size=13,
                                color="#2D3748",
                                weight=ft.FontWeight.BOLD,
                            ),
                        ], spacing=0),
                        padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                        border_radius=8,
                        bgcolor="#F0FFF4",
                    ),
                ]),
                
                ft.Container(height=16),
                
                # Acciones
                ft.Row([
                    # Restaurar
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.RESTORE, size=16, color="#FFFFFF"),
                            ft.Container(width=8),
                            ft.Text("Restaurar", size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ], spacing=0),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                        border_radius=10,
                        bgcolor="#667EEA",
                        on_click=lambda _, v=version: self._restore_version(v),
                        ink=True,
                    ),
                    
                    ft.Container(width=10),
                    
                    # Ver detalles
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color="#718096"),
                            ft.Container(width=8),
                            ft.Text("Detalles", size=14, weight=ft.FontWeight.BOLD, color="#718096"),
                        ], spacing=0),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                        border_radius=10,
                        bgcolor="#FFFFFF",
                        border=ft.Border.all(2, "#E2E8F0"),
                        on_click=lambda _, v=version: self._view_details(v),
                        ink=True,
                    ),
                    
                    ft.Container(expand=True),
                    
                    # Eliminar versión
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE_OUTLINE, size=18, color="#F56565"),
                        width=40,
                        height=40,
                        border_radius=10,
                        bgcolor="#FFF5F5",
                        border=ft.Border.all(1.5, "#FED7D7"),
                        alignment=ft.alignment.Alignment(0, 0),
                        on_click=lambda _, v=version: self._delete_version(v),
                        ink=True,
                        tooltip="Eliminar versión",
                    ),
                ]),
                
            ]),
            padding=ft.Padding.all(20),
            border_radius=14,
            bgcolor="#FFFFFF",
            border=ft.Border.all(2 if is_current else 1, node_color if is_current else "#E2E8F0"),
            expand=True,
        )
        
        # Importar canvas
        import flet.canvas as cv
        
        # Contenedor principal con timeline usando Canvas para la línea
        return ft.Container(
            content=ft.Row([
                # Columna de timeline con Canvas para línea + nodo
                ft.Container(
                    content=ft.Stack([
                        # Canvas con línea vertical (si no es el último)
                        cv.Canvas(
                            width=20,
                            height=280,
                            shapes=[
                                cv.Line(
                                    x1=10,  # Centro horizontal
                                    y1=22,  # Después del nodo (8px padding + 14px nodo)
                                    x2=10,  # Centro horizontal
                                    y2=280,  # Hasta el final
                                    paint=ft.Paint(
                                        stroke_width=3,
                                        color=node_color,
                                    ),
                                ),
                            ] if not is_last else [],
                        ),
                        # Nodo encima del canvas
                        ft.Container(
                            content=ft.Container(
                                width=14,
                                height=14,
                                border_radius=7,
                                bgcolor=node_color,
                                border=ft.Border.all(3, "#FFFFFF"),
                            ),
                            margin=ft.Margin(top=8, left=3, right=0, bottom=0),
                        ),
                    ]),
                    width=20,
                ),
                
                ft.Container(width=20),
                
                # Card de versión
                version_card,
                
            ], alignment=ft.CrossAxisAlignment.START),
            margin=ft.Margin(bottom=20, left=0, right=0, top=0),
        )
    
    def _build_estadisticas_view(self):
        """Vista de estadísticas con diseño moderno y minimalista"""
        versiones = self.proyecto.get("versiones", [])
        total_archivos = sum(v.get("archivos", 0) for v in versiones)
        
        return ft.Container(
            content=ft.Column([
                ft.Container(height=32),
                
                # Grid de estadísticas con diseño card moderno
                ft.Row([
                    # Card 1: Versiones
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(ft.Icons.LAYERS_ROUNDED, size=28, color="#667EEA"),
                                width=56,
                                height=56,
                                border_radius=14,
                                bgcolor="#EEF2FF",
                                alignment=ft.alignment.Alignment(0, 0),
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                str(len(versiones)),
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color="#1A202C",
                            ),
                            ft.Container(height=4),
                            ft.Text(
                                "Versiones Guardadas",
                                size=13,
                                color="#718096",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        width=220,
                        padding=ft.Padding.all(28),
                        border_radius=16,
                        bgcolor="#FFFFFF",
                    ),
                    
                    ft.Container(width=24),
                    
                    # Card 2: Archivos
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, size=28, color="#10B981"),
                                width=56,
                                height=56,
                                border_radius=14,
                                bgcolor="#ECFDF5",
                                alignment=ft.alignment.Alignment(0, 0),
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                str(total_archivos),
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color="#1A202C",
                            ),
                            ft.Container(height=4),
                            ft.Text(
                                "Archivos Rastreados",
                                size=13,
                                color="#718096",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        width=220,
                        padding=ft.Padding.all(28),
                        border_radius=16,
                        bgcolor="#FFFFFF",
                    ),
                    
                    ft.Container(width=24),
                    
                    # Card 3: Tamaño
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(ft.Icons.FOLDER_ROUNDED, size=28, color="#F59E0B"),
                                width=56,
                                height=56,
                                border_radius=14,
                                bgcolor="#FEF3C7",
                                alignment=ft.alignment.Alignment(0, 0),
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                self.proyecto.get("tamaño_total", "0 B"),
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color="#1A202C",
                            ),
                            ft.Container(height=4),
                            ft.Text(
                                "Tamaño Total",
                                size=13,
                                color="#718096",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        width=220,
                        padding=ft.Padding.all(28),
                        border_radius=16,
                        bgcolor="#FFFFFF",
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Container(height=48),
                
                # Card de información del proyecto
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Información del Proyecto",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#1A202C",
                        ),
                        ft.Container(height=24),
                        
                        # Info rows con diseño mejorado
                        self._build_modern_info_row("Nombre", self.proyecto.get("nombre", "-"), ft.Icons.LABEL_ROUNDED),
                        self._build_modern_info_row("Tipo", self.proyecto.get("tipo", "-").upper(), ft.Icons.CATEGORY_ROUNDED),
                        self._build_modern_info_row("Ubicación", self.proyecto.get("ruta", "-"), ft.Icons.FOLDER_OPEN_ROUNDED),
                        self._build_modern_info_row("Creado", self.proyecto.get("fecha_creacion", "-"), ft.Icons.CALENDAR_TODAY_ROUNDED),
                    ]),
                    width=720,
                    padding=ft.Padding.all(32),
                    border_radius=16,
                    bgcolor="#FFFFFF",
                ),
                
                ft.Container(height=100),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
            expand=True,
        )
    
    def _build_modern_info_row(self, label, value, icon):
        """Fila de información con diseño moderno"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=18, color="#667EEA"),
                    width=36,
                    height=36,
                    border_radius=8,
                    bgcolor="#EEF2FF",
                    alignment=ft.alignment.Alignment(0, 0),
                ),
                ft.Container(width=16),
                ft.Column([
                    ft.Text(label, size=12, color="#A0AEC0", weight=ft.FontWeight.W_500),
                    ft.Container(height=2),
                    ft.Text(value, size=14, color="#1A202C", weight=ft.FontWeight.W_600),
                ], spacing=0, expand=True),
            ]),
            padding=ft.Padding.all(16),
            border_radius=12,
            bgcolor="#F7FAFC",
            margin=ft.Margin(bottom=12, left=0, right=0, top=0),
        )
    
    def _build_configuracion_view(self):
        """Vista de configuración con diseño moderno y minimalista"""
        return ft.Container(
            content=ft.Column([
                ft.Container(height=48),
                
                # Card principal de configuración
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Configuración del Proyecto",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1A202C",
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Administra las opciones de tu proyecto",
                            size=14,
                            color="#718096",
                        ),
                        
                        ft.Container(height=32),
                        
                        # Opciones con diseño moderno
                        self._build_modern_config_option(
                            "Abrir Carpeta",
                            "Abre la carpeta del proyecto en el explorador",
                            ft.Icons.FOLDER_OPEN_ROUNDED,
                            "#10B981",
                            "#ECFDF5",
                            self._open_folder
                        ),
                        
                        self._build_modern_config_option(
                            "Exportar Proyecto",
                            "Exporta el proyecto completo a un archivo ZIP",
                            ft.Icons.DOWNLOAD_ROUNDED,
                            "#F59E0B",
                            "#FEF3C7",
                            self._export_project
                        ),
                        
                        ft.Container(height=24),
                        
                        # Separador
                        ft.Container(
                            height=1,
                            bgcolor="#E5E7EB",
                        ),
                        
                        ft.Container(height=24),
                        
                        # Zona de peligro
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=18, color="#EF4444"),
                                    ft.Container(width=8),
                                    ft.Text(
                                        "Zona de Peligro",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color="#EF4444",
                                    ),
                                ]),
                                ft.Container(height=16),
                                self._build_modern_config_option(
                                    "Eliminar Proyecto",
                                    "Elimina permanentemente este proyecto y todas sus versiones",
                                    ft.Icons.DELETE_FOREVER_ROUNDED,
                                    "#EF4444",
                                    "#FEF2F2",
                                    self._delete_project,
                                    is_danger=True
                                ),
                            ]),
                            padding=ft.Padding.all(20),
                            border_radius=12,
                            bgcolor="#FEF2F2",
                            border=ft.Border.all(1, "#FEE2E2"),
                        ),
                        
                    ]),
                    width=680,
                    padding=ft.Padding.all(40),
                    border_radius=16,
                    bgcolor="#FFFFFF",
                ),
                
                ft.Container(height=100),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
            expand=True,
        )
    
    def _build_modern_config_option(self, title, description, icon, color, bg_color, on_click, is_danger=False):
        """Opción de configuración con diseño moderno"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=22, color=color),
                    width=48,
                    height=48,
                    border_radius=12,
                    bgcolor=bg_color,
                    alignment=ft.alignment.Alignment(0, 0),
                ),
                ft.Container(width=16),
                ft.Column([
                    ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color="#1A202C"),
                    ft.Container(height=4),
                    ft.Text(description, size=13, color="#718096"),
                ], spacing=0, expand=True),
                ft.Icon(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, size=18, color="#CBD5E0"),
            ]),
            padding=ft.Padding.all(20),
            border_radius=12,
            bgcolor="#FFFFFF" if not is_danger else "#FEF2F2",
            border=ft.Border.all(1, "#E5E7EB" if not is_danger else "#FEE2E2"),
            on_click=lambda _: on_click(),
            ink=True,
            margin=ft.Margin(bottom=12, left=0, right=0, top=0),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _build_dock(self):
        """Dock de navegación - solo Versiones y Estadísticas"""
        return ft.Container(
            content=ft.Row([
                self._build_dock_item("Versiones", ft.Icons.ACCOUNT_TREE_OUTLINED, "versiones"),
                self._build_dock_item("Estadísticas", ft.Icons.BAR_CHART_ROUNDED, "estadisticas"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            bgcolor="#FFFFFF",
            border=ft.Border(top=ft.BorderSide(1, "#E2E8F0")),
        )
    
    def _build_dock_item(self, label, icon, view_name):
        """Item del dock"""
        is_active = self.current_view == view_name
        
        return ft.Container(
            content=ft.Column([
                ft.Icon(
                    icon,
                    size=22,
                    color="#667EEA" if is_active else "#A0AEC0",
                ),
                ft.Container(height=4),
                ft.Text(
                    label,
                    size=11,
                    weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL,
                    color="#667EEA" if is_active else "#718096",
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            width=120,
            padding=ft.Padding.symmetric(horizontal=16, vertical=8),
            border_radius=8,
            bgcolor="#EDF2F7" if is_active else "transparent",
            on_click=lambda _, v=view_name: self._change_view(v),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _change_view(self, view_name):
        """Cambia la vista actual"""
        self.current_view = view_name
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _scroll_to_current_version(self):
        """Hace scroll a la versión actual"""
        versiones = self.proyecto.get("versiones", [])
        version_actual_proyecto = self.proyecto.get('version_actual', 1)
        
        # Encontrar índice de la versión actual
        for i, v in enumerate(versiones):
            if v.get('numero') == version_actual_proyecto:
                # Calcular posición aproximada (cada item ~300px)
                scroll_offset = i * 300
                
                # Hacer scroll usando scroll_to si está disponible
                if hasattr(self.timeline_scroll, 'scroll_to'):
                    self.timeline_scroll.scroll_to(offset=scroll_offset, duration=300)
                    self.page.update()
                break
    
    def _delete_version(self, version):
        """Elimina una versión específica con modal compacto y genial"""
        numero_version = version.get("numero", 1)
        
        def confirmar_eliminacion():
            dialog.open = False
            self.page.update()
            
            # Mostrar loader con timeline async
            self._show_async_progress_dialog("Eliminando versión", "delete_version", numero_version)
        
        # Modal compacto y genial
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    # Icono flotante compacto
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE_FOREVER_ROUNDED, size=48, color="#FFFFFF"),
                        width=80,
                        height=80,
                        border_radius=40,
                        bgcolor="#F56565",
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                    
                    ft.Container(height=20),
                    
                    # Título compacto
                    ft.Text(
                        "Eliminar Versión",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=6),
                    
                    ft.Text(
                        f"¿Eliminar la versión {numero_version}?",
                        size=14,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Info compacta en una sola card
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("v" + str(numero_version), size=16, weight=ft.FontWeight.BOLD, color="#F56565"),
                                    width=45,
                                    height=45,
                                    border_radius=10,
                                    bgcolor="#FFF5F5",
                                    alignment=ft.alignment.Alignment(0, 0),
                                ),
                                ft.Container(width=12),
                                ft.Column([
                                    ft.Text(version.get('fecha', ''), size=13, color="#2D3748", weight=ft.FontWeight.W_600),
                                    ft.Container(height=2),
                                    ft.Text(
                                        version.get('descripcion', 'Sin descripción')[:50] + ("..." if len(version.get('descripcion', '')) > 50 else ""),
                                        size=12,
                                        color="#718096",
                                    ),
                                ], spacing=0, expand=True),
                            ]),
                        ]),
                        padding=ft.Padding.all(14),
                        border_radius=12,
                        bgcolor="#FFF5F5",
                        border=ft.Border.all(1, "#FED7D7"),
                    ),
                    
                    ft.Container(height=8),
                    
                    # Advertencia compacta
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=16, color="#F56565"),
                            ft.Container(width=8),
                            ft.Text(
                                "Esta acción no se puede deshacer",
                                size=12,
                                color="#C53030",
                            ),
                        ]),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                        border_radius=8,
                        bgcolor="#FFF5F5",
                    ),
                    
                    ft.Container(height=24),
                    
                    # Botones grandes
                    ft.Row([
                        ft.Container(
                            content=ft.TextButton(
                                content=ft.Container(
                                    content=ft.Text("Cancelar", size=15, weight=ft.FontWeight.W_600, color="#718096"),
                                    padding=ft.Padding.all(14),
                                    alignment=ft.alignment.Alignment(0, 0),
                                ),
                                on_click=lambda _: self._close_dialog(dialog),
                            ),
                            expand=1,
                            border_radius=10,
                            bgcolor="#F7FAFC",
                            border=ft.Border.all(2, "#E2E8F0"),
                        ),
                        
                        ft.Container(width=10),
                        
                        ft.Container(
                            content=ft.ElevatedButton(
                                content=ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.DELETE_OUTLINE, size=18, color="#FFFFFF"),
                                        ft.Container(width=8),
                                        ft.Text("Eliminar", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    padding=ft.Padding.all(14),
                                ),
                                on_click=lambda _: confirmar_eliminacion(),
                                style=ft.ButtonStyle(
                                    bgcolor="#F56565",
                                    elevation=0,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            expand=2,
                        ),
                    ]),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding.all(28),
                width=480,
                border_radius=20,
                bgcolor="#FFFFFF",
            ),
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _delete_project(self):
        """Elimina el proyecto con confirmación"""
        def confirmar_eliminacion():
            dialog.open = False
            self.page.update()
            
            # Mostrar loader con timeline
            self._show_async_progress_dialog("Eliminando proyecto", "delete")
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar Proyecto", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=48, color="#F56565"),
                    ft.Container(height=16),
                    ft.Text(
                        "¿Estás seguro de eliminar este proyecto?",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color="#2D3748",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "Esta acción eliminará permanentemente todas las versiones guardadas.",
                        size=14,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=12),
                    ft.Container(
                        content=ft.Text(
                            f"Proyecto: {self.proyecto.get('nombre', '')}",
                            size=13,
                            color="#2D3748",
                            weight=ft.FontWeight.W_600,
                        ),
                        padding=ft.Padding.all(12),
                        border_radius=8,
                        bgcolor="#F7FAFC",
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
                width=400,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self._close_dialog(dialog)),
                ft.ElevatedButton(
                    "Eliminar",
                    on_click=lambda _: confirmar_eliminacion(),
                    style=ft.ButtonStyle(
                        bgcolor="#F56565",
                        color="#FFFFFF",
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _open_folder(self):
        """Abre la carpeta del proyecto"""
        exito = abrir_carpeta_proyecto(self.proyecto["ruta"])
        if exito:
            self._show_success_snackbar("✓ Carpeta abierta")
        else:
            self._show_error_snackbar("❌ Error al abrir la carpeta")
    
    def _export_project(self):
        """Exporta el proyecto a ZIP"""
        # Seleccionar carpeta de destino
        try:
            import subprocess
            result = subprocess.run(
                ['zenity', '--file-selection', '--directory', '--title=Seleccionar carpeta de destino'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                ruta_destino = result.stdout.strip()
                
                # Mostrar loader con timeline
                self._show_async_progress_dialog("Exportando proyecto", "export", ruta_destino)
        except:
            self._show_error_snackbar("❌ Error al seleccionar carpeta")
    
    # Métodos de versiones
    def _save_version(self):
        """Guarda una nueva versión con modal compacto y genial"""
        # Crear campo de texto para el mensaje
        mensaje_field = ft.TextField(
            hint_text="Ej: Agregadas nuevas funcionalidades...",
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_radius=10,
            border_color="#E2E8F0",
            focused_border_color="#667EEA",
            text_size=13,
        )
        
        def guardar():
            """Guarda la versión"""
            mensaje = mensaje_field.value or "Sin descripción"
            dialog.open = False
            self.page.update()
            
            # Mostrar loader con timeline async
            self._show_async_progress_dialog("Guardando versión", "save", mensaje)
        
        # Modal compacto y genial
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    # Icono flotante compacto
                    ft.Container(
                        content=ft.Icon(ft.Icons.SAVE_ROUNDED, size=48, color="#FFFFFF"),
                        width=80,
                        height=80,
                        border_radius=40,
                        bgcolor="#667EEA",
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                    
                    ft.Container(height=20),
                    
                    # Título compacto
                    ft.Text(
                        "Guardar Nueva Versión",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=6),
                    
                    ft.Text(
                        "Describe los cambios realizados",
                        size=14,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Campo de texto compacto
                    ft.Container(
                        content=mensaje_field,
                        padding=ft.Padding.all(4),
                        border_radius=12,
                        bgcolor="#F7FAFC",
                    ),
                    
                    ft.Container(height=8),
                    
                    # Tip compacto
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, size=14, color="#667EEA"),
                            ft.Container(width=6),
                            ft.Text(
                                "Sé específico sobre los cambios",
                                size=11,
                                color="#A0AEC0",
                                italic=True,
                            ),
                        ]),
                        padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                        border_radius=8,
                        bgcolor="#EDF2F7",
                    ),
                    
                    ft.Container(height=24),
                    
                    # Botones grandes
                    ft.Row([
                        ft.Container(
                            content=ft.TextButton(
                                content=ft.Container(
                                    content=ft.Text("Cancelar", size=15, weight=ft.FontWeight.W_600, color="#718096"),
                                    padding=ft.Padding.all(14),
                                    alignment=ft.alignment.Alignment(0, 0),
                                ),
                                on_click=lambda _: self._close_dialog(dialog),
                            ),
                            expand=1,
                            border_radius=10,
                            bgcolor="#F7FAFC",
                            border=ft.Border.all(2, "#E2E8F0"),
                        ),
                        
                        ft.Container(width=10),
                        
                        ft.Container(
                            content=ft.ElevatedButton(
                                content=ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=18, color="#FFFFFF"),
                                        ft.Container(width=8),
                                        ft.Text("Guardar", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    padding=ft.Padding.all(14),
                                ),
                                on_click=lambda _: guardar(),
                                style=ft.ButtonStyle(
                                    bgcolor="#667EEA",
                                    elevation=0,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            expand=2,
                        ),
                    ]),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding.all(28),
                width=480,
                border_radius=20,
                bgcolor="#FFFFFF",
            ),
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _restore_version(self, version):
        """Restaura una versión con panel lateral moderno y elegante"""
        numero_version = version.get("numero", 1)
        
        def confirmar():
            # Cerrar panel inmediatamente
            panel_overlay.visible = False
            self.page.update()
            
            # Pequeña pausa para que se vea que se cerró
            import time
            time.sleep(0.1)
            
            # Mostrar loader con timeline async
            self._show_async_progress_dialog("Restaurando versión", "restore", numero_version)
        
        def cerrar_panel(_=None):
            # Animación de salida ultra rápida
            panel_content.opacity = 0
            backdrop.opacity = 0
            self.page.update()
            
            # Esperar animación y cerrar
            import time
            time.sleep(0.1)  # 100ms para coincidir con la animación
            panel_overlay.visible = False
            self.page.update()
        
        # Backdrop con blur y animación ultra rápida
        backdrop = ft.Container(
            bgcolor="#1A202C",
            opacity=0,  # Inicia transparente
            expand=True,
            on_click=cerrar_panel,
            animate_opacity=100,  # Ultra rápido: 100ms
        )
        
        # Panel lateral moderno y elegante
        panel_content = ft.Container(
            content=ft.Column([
                # Header minimalista
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color="#A0AEC0",
                            icon_size=24,
                            on_click=cerrar_panel,
                            tooltip="Cerrar",
                        ),
                    ], alignment=ft.MainAxisAlignment.END),
                    padding=ft.Padding(left=32, right=24, top=20, bottom=0),
                ),
                
                # Contenido principal
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=12),
                        
                        # Icono grande y moderno
                        ft.Container(
                            content=ft.Icon(ft.Icons.RESTORE_ROUNDED, size=56, color="#ED8936"),
                            width=100,
                            height=100,
                            border_radius=50,
                            bgcolor="#FFF5F0",
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                        
                        ft.Container(height=28),
                        
                        # Título grande y bold
                        ft.Text(
                            "Restaurar Versión",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color="#1A202C",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        
                        ft.Container(height=16),
                        
                        # Badge de versión
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.TAG, size=20, color="#667EEA"),
                                ft.Container(width=10),
                                ft.Text(
                                    f"v{numero_version}",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color="#667EEA",
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            padding=ft.Padding.symmetric(horizontal=24, vertical=12),
                            border_radius=12,
                            bgcolor="#EDF2F7",
                        ),
                        
                        ft.Container(height=32),
                        
                        # Solo descripción
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=22, color="#48BB78"),
                                    width=44,
                                    height=44,
                                    border_radius=12,
                                    bgcolor="#F0FFF4",
                                    alignment=ft.alignment.Alignment(0, 0),
                                ),
                                ft.Container(width=16),
                                ft.Column([
                                    ft.Text("Cambios", size=14, color="#718096", weight=ft.FontWeight.W_600),
                                    ft.Container(height=6),
                                    ft.Text(
                                        version.get('descripcion', 'Sin descripción'),
                                        size=17,
                                        color="#1A202C",
                                        weight=ft.FontWeight.BOLD,
                                        max_lines=3,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ], spacing=0, expand=True),
                            ], alignment=ft.CrossAxisAlignment.START),
                            padding=ft.Padding.all(18),
                            border_radius=14,
                            bgcolor="#F7FAFC",
                        ),
                        
                        ft.Container(height=32),
                        
                        # Advertencia moderna
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color="#ED8936"),
                                ft.Container(width=12),
                                ft.Text(
                                    "Los archivos actuales serán reemplazados",
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color="#744210",
                                ),
                            ]),
                            padding=ft.Padding.all(16),
                            border_radius=12,
                            bgcolor="#FFFAF0",
                            border=ft.Border.all(1, "#FED7AA"),
                        ),
                        
                        ft.Container(height=32),
                        
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True,
                    padding=ft.Padding.symmetric(horizontal=36, vertical=0),
                ),
                
                # Footer con botones modernos
                ft.Container(
                    content=ft.Column([
                        # Botón principal grande
                        ft.ElevatedButton(
                            content=ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.RESTORE, size=20, color="#FFFFFF"),
                                    ft.Container(width=12),
                                    ft.Text("Restaurar Versión", size=17, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                padding=ft.Padding.symmetric(horizontal=0, vertical=16),
                                alignment=ft.alignment.Alignment(0, 0),
                            ),
                            on_click=lambda _: confirmar(),
                            style=ft.ButtonStyle(
                                bgcolor="#ED8936",
                                elevation=0,
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                            width=float('inf'),
                        ),
                        
                        ft.Container(height=12),
                        
                        # Botón secundario
                        ft.TextButton(
                            content=ft.Text("Cancelar", size=16, weight=ft.FontWeight.BOLD, color="#718096"),
                            on_click=cerrar_panel,
                            style=ft.ButtonStyle(
                                padding=ft.Padding.symmetric(horizontal=0, vertical=14),
                            ),
                            width=float('inf'),
                        ),
                    ]),
                    padding=ft.Padding(left=36, right=36, top=0, bottom=32),
                ),
                
            ], spacing=0),
            width=600,  # Más ancho: 600px
            bgcolor="#FFFFFF",
            opacity=0,  # Inicia transparente
            animate_opacity=120,  # Ultra rápido: 120ms
        )
        
        # Overlay con backdrop blur y panel
        panel_overlay = ft.Container(
            content=ft.Stack([
                backdrop,
                # Panel lateral alineado a la derecha
                ft.Row([
                    ft.Container(expand=True),
                    panel_content,
                ], spacing=0),
            ]),
            expand=True,
            visible=True,
        )
        
        self.page.overlay.append(panel_overlay)
        self.page.update()
        
        # Trigger animación de entrada rápida
        import threading
        def animar_entrada():
            import time
            time.sleep(0.03)  # Delay más corto
            backdrop.opacity = 0.4
            panel_content.opacity = 1.0
            self.page.update()
        
        thread = threading.Thread(target=animar_entrada, daemon=True)
        thread.start()
    
    def _view_details(self, version):
        """Ver detalles de una versión"""
        numero_version = version.get("numero", 1)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Versión {numero_version}", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    self._build_detail_row("📅 Fecha", version.get("fecha_completa", version.get("fecha", ""))),
                    self._build_detail_row("📝 Descripción", version.get("descripcion", "Sin descripción")),
                    self._build_detail_row("📁 Archivos", str(version.get("archivos", 0))),
                    self._build_detail_row("💾 Tamaño", version.get("tamaño", "0 B")),
                    self._build_detail_row("👤 Autor", version.get("autor", "Usuario")),
                ], tight=True),
                width=400,
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda _: self._close_dialog(dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _build_detail_row(self, label, value):
        """Crea una fila de detalle"""
        return ft.Container(
            content=ft.Row([
                ft.Text(label, size=14, color="#718096", weight=ft.FontWeight.W_600, width=120),
                ft.Text(value, size=14, color="#2D3748", expand=True),
            ]),
            margin=ft.Margin(bottom=12, left=0, right=0, top=0),
        )
    
    def _show_progress_dialog(self, title, func, *args):
        """Muestra un loader con timeline Git-style y ejecuta la operación de forma síncrona"""
        print(f"[DEBUG] _show_progress_dialog: Iniciando loader con título '{title}'")
        
        # Definir pasos según el tipo de operación
        if "Guardando" in title:
            steps = [
                {"title": "Preparando archivos", "subtitle": "Analizando cambios en el proyecto", "status": "active"},
                {"title": "Creando snapshot", "subtitle": "Guardando estado actual", "status": "pending"},
                {"title": "Finalizando", "subtitle": "Actualizando historial", "status": "pending"},
            ]
        elif "Restaurando" in title:
            steps = [
                {"title": "Leyendo versión", "subtitle": "Cargando snapshot guardado", "status": "active"},
                {"title": "Restaurando archivos", "subtitle": "Aplicando cambios al proyecto", "status": "pending"},
                {"title": "Finalizando", "subtitle": "Actualizando estado", "status": "pending"},
            ]
        else:
            steps = [
                {"title": "Procesando", "subtitle": "Ejecutando operación", "status": "active"},
            ]
        
        # Crear loader con timeline
        loader = LoaderView(self.page, title, steps)
        
        # Crear dialog
        self.progress_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=loader.build(),
                width=600,
                height=500,
                padding=ft.Padding.all(0),
            ),
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor="#F7FAFC",
        )
        
        # Guardar referencia al loader para poder actualizarlo
        self.current_loader = loader
        
        # Mostrar dialog
        self.page.overlay.append(self.progress_dialog)
        self.progress_dialog.open = True
        self.page.update()
        print(f"[DEBUG] _show_progress_dialog: Dialog mostrado")
        
        # IMPORTANTE: Dar tiempo para que el loader se renderice
        import time
        time.sleep(0.3)  # Pausa para que se vea el loader
        
        print(f"[DEBUG] _show_progress_dialog: Ejecutando función {func.__name__} de forma síncrona")
        try:
            func(*args)
            print(f"[DEBUG] _show_progress_dialog: Función completada")
        except Exception as e:
            print(f"[DEBUG] _show_progress_dialog: Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Pequeña pausa antes de cerrar para que se vea que terminó
        time.sleep(0.2)
    
    def _update_progress(self, mensaje):
        """Actualiza el progreso del timeline"""
        print(f"[DEBUG] _update_progress: {mensaje}")
        
        if not hasattr(self, 'current_loader'):
            return
        
        # Mapear mensajes a estados del timeline
        if "Guardando" in self.progress_dialog.content.content.content.controls[1].value:
            # Timeline para guardar versión
            if "Preparando" in mensaje or "Analizando" in mensaje:
                steps = [
                    {"title": "Preparando archivos", "subtitle": "Analizando cambios en el proyecto", "status": "active"},
                    {"title": "Creando snapshot", "subtitle": "Guardando estado actual", "status": "pending"},
                    {"title": "Finalizando", "subtitle": "Actualizando historial", "status": "pending"},
                ]
            elif "Copiando" in mensaje or "Guardando" in mensaje:
                steps = [
                    {"title": "Preparando archivos", "subtitle": "Analizando cambios en el proyecto", "status": "completed"},
                    {"title": "Creando snapshot", "subtitle": "Guardando estado actual", "status": "active"},
                    {"title": "Finalizando", "subtitle": "Actualizando historial", "status": "pending"},
                ]
            else:  # Finalizando
                steps = [
                    {"title": "Preparando archivos", "subtitle": "Analizando cambios en el proyecto", "status": "completed"},
                    {"title": "Creando snapshot", "subtitle": "Guardando estado actual", "status": "completed"},
                    {"title": "Finalizando", "subtitle": "Actualizando historial", "status": "active"},
                ]
        elif "Restaurando" in self.progress_dialog.content.content.content.controls[1].value:
            # Timeline para restaurar versión
            if "Leyendo" in mensaje or "Cargando" in mensaje:
                steps = [
                    {"title": "Leyendo versión", "subtitle": "Cargando snapshot guardado", "status": "active"},
                    {"title": "Restaurando archivos", "subtitle": "Aplicando cambios al proyecto", "status": "pending"},
                    {"title": "Finalizando", "subtitle": "Actualizando estado", "status": "pending"},
                ]
            elif "Restaurando" in mensaje or "Copiando" in mensaje:
                steps = [
                    {"title": "Leyendo versión", "subtitle": "Cargando snapshot guardado", "status": "completed"},
                    {"title": "Restaurando archivos", "subtitle": "Aplicando cambios al proyecto", "status": "active"},
                    {"title": "Finalizando", "subtitle": "Actualizando estado", "status": "pending"},
                ]
            else:  # Finalizando
                steps = [
                    {"title": "Leyendo versión", "subtitle": "Cargando snapshot guardado", "status": "completed"},
                    {"title": "Restaurando archivos", "subtitle": "Aplicando cambios al proyecto", "status": "completed"},
                    {"title": "Finalizando", "subtitle": "Actualizando estado", "status": "active"},
                ]
        else:
            return
        
        try:
            self.current_loader.update_steps(steps)
        except Exception as e:
            print(f"[DEBUG] _update_progress: Error actualizando steps: {e}")
    
    def _close_progress_dialog(self):
        """Cierra el loader"""
        print(f"[DEBUG] _close_progress_dialog: Cerrando dialog")
        
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.open = False
            self.page.update()
            print(f"[DEBUG] _close_progress_dialog: Dialog cerrado")
    
    def _close_bottom_sheet(self, bottom_sheet):
        """Cierra un bottom sheet"""
        bottom_sheet.open = False
        self.page.update()
    
    def _close_dialog(self, dialog):
        """Cierra un diálogo"""
        dialog.open = False
        self.page.update()
    
    def _show_success_snackbar(self, mensaje):
        """Muestra un snackbar de éxito"""
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor="#48BB78",
            duration=2000,  # 2 segundos
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()
    
    def _show_error_snackbar(self, mensaje):
        """Muestra un snackbar de error"""
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor="#F56565",
            duration=2000,  # 2 segundos
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()

    def _show_async_progress_dialog(self, title, operation_type, *args):
            """Muestra un loader y ejecuta la operación de forma SÍNCRONA (como el original)"""
            # Ejecutar operación directamente de forma síncrona
            try:
                resultado = None
                
                if operation_type == "save":
                    mensaje = args[0] if args else "Versión guardada"
                    resultado = guardar_version_ui(self.proyecto["ruta"], mensaje, None)
                elif operation_type == "restore":
                    numero_version = args[0] if args else 1
                    resultado = restaurar_version_ui(self.proyecto["ruta"], numero_version)
                elif operation_type == "delete":
                    resultado = eliminar_proyecto_ui(self.proyecto["ruta"])
                elif operation_type == "export":
                    ruta_destino = args[0] if args else ""
                    resultado = exportar_proyecto_ui(self.proyecto["ruta"], ruta_destino)
                elif operation_type == "delete_version":
                    numero_version = args[0] if args else 1
                    from cli_integration import eliminar_version_ui
                    resultado = eliminar_version_ui(self.proyecto["ruta"], numero_version)
                else:
                    resultado = True

                # Manejar resultado inmediatamente
                if resultado:
                    if operation_type == "save":
                        self.proyecto = resultado
                        if self.on_refresh:
                            self.on_refresh(self.proyecto["ruta"])
                        self.page.controls.clear()
                        self.page.add(self.build())
                        self.page.update()
                        self._show_success_snackbar("✓ Versión guardada exitosamente")
                    elif operation_type == "restore":
                        self.proyecto = resultado
                        if self.on_refresh:
                            self.on_refresh(self.proyecto["ruta"])
                        self.page.controls.clear()
                        self.page.add(self.build())
                        self.page.update()
                        self._show_success_snackbar("✓ Versión restaurada exitosamente")
                    elif operation_type == "delete":
                        self._show_success_snackbar("✓ Proyecto eliminado exitosamente")
                        self.on_back()
                    elif operation_type == "export":
                        self._show_success_snackbar(f"✓ Proyecto exportado: {Path(resultado).name}")
                    elif operation_type == "delete_version":
                        from cli_integration import leer_info_proyecto
                        self.proyecto = leer_info_proyecto(self.proyecto["ruta"])
                        if self.on_refresh:
                            self.on_refresh(self.proyecto["ruta"])
                        self.page.controls.clear()
                        self.page.add(self.build())
                        self.page.update()
                        self._show_success_snackbar("✓ Versión eliminada exitosamente")
                else:
                    self._show_error_snackbar("❌ Error en la operación")

            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                print(f"Error en operación: {error_detail}")
                self._show_error_snackbar(f"Error: {str(e)}")
