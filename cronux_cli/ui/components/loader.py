"""
Componente Loader reutilizable - Diseño Git-style timeline
"""
import flet as ft


class LoaderView:
    """Vista de carga con timeline estilo Git"""
    
    def __init__(self, page: ft.Page, title: str, steps: list = None):
        """
        Args:
            page: Página de Flet
            title: Título principal del loader
            steps: Lista de diccionarios con formato:
                   [{"title": "Paso 1", "subtitle": "Descripción", "status": "completed|active|pending"}]
        """
        self.page = page
        self.title = title
        self.steps = steps or [
            {"title": "Iniciando operación", "subtitle": "Preparando archivos", "status": "active"}
        ]
        
        # Contenedor principal que reemplaza toda la vista
        self.container = ft.Container(
            content=ft.Column([
                ft.Container(expand=True),
                
                # Título principal
                ft.Text(
                    title,
                    size=34,
                    weight=ft.FontWeight.W_700,
                    color="#1A202C",
                    text_align=ft.TextAlign.CENTER,
                ),
                
                ft.Container(height=48),
                
                # Timeline estilo Git - centrado
                ft.Row([
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Column(
                            [self._build_step(step, i) for i, step in enumerate(self.steps)],
                            spacing=0,
                        ),
                        width=420,
                    ),
                    ft.Container(expand=True),
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Container(expand=True),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor="#F7FAFC",
            alignment=ft.alignment.Alignment(0, 0),
        )
    
    def _build_step(self, step, index):
        """Construye un paso del timeline"""
        status = step.get("status", "pending")
        is_last = index == len(self.steps) - 1
        
        # Colores según estado
        if status == "completed":
            circle_color = "#48BB78"  # Verde
            icon = ft.Icons.CHECK_ROUNDED
            text_color = "#1A202C"
            line_color = "#48BB78"
        elif status == "active":
            circle_color = "#667EEA"  # Azul
            icon = None  # ProgressRing
            text_color = "#667EEA"
            line_color = "#667EEA"
        else:  # pending
            circle_color = "#CBD5E0"  # Gris
            icon = None
            text_color = "#718096"
            line_color = "#E2E8F0"
        
        return ft.Row([
            # Línea vertical y círculo
            ft.Container(
                content=ft.Column([
                    # Círculo con icono o progress ring
                    ft.Container(
                        width=22,
                        height=22,
                        bgcolor=circle_color,
                        border_radius=50,
                        content=ft.Icon(
                            icon,
                            size=14,
                            color="#FFFFFF",
                        ) if icon else (
                            ft.ProgressRing(
                                width=13,
                                height=13,
                                stroke_width=2.5,
                                color="#FFFFFF",
                            ) if status == "active" else None
                        ),
                        alignment=ft.alignment.Alignment(0, 0),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=18 if status == "active" else 8,
                            color=f"{circle_color}80" if status == "active" else f"{circle_color}4D",
                            offset=ft.Offset(0, 0 if status == "active" else 2),
                        ),
                    ),
                    # Línea vertical (no mostrar en el último paso)
                    ft.Container(
                        width=3,
                        height=45,
                        bgcolor=line_color,
                    ) if not is_last else ft.Container(),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                width=35,
            ),
            
            ft.Container(width=18),
            
            # Texto del paso
            ft.Column([
                ft.Text(
                    step.get("title", ""),
                    size=17,
                    weight=ft.FontWeight.W_600,
                    color=text_color,
                ),
                ft.Container(height=4),
                ft.Text(
                    step.get("subtitle", ""),
                    size=14,
                    color="#718096",
                ),
            ], spacing=0),
        ], spacing=0)
    
    def update_steps(self, steps: list):
        """Actualiza los pasos del timeline"""
        self.steps = steps
        # Reconstruir el timeline
        try:
            # Verificar que el contenedor y sus controles existan
            if not self.container or not hasattr(self.container, 'content'):
                return
            
            if not self.container.content or not hasattr(self.container.content, 'controls'):
                return
            
            # Navegar a la columna del timeline
            timeline_column = self.container.content.controls[2].content.controls[1].content
            if timeline_column and hasattr(timeline_column, 'controls'):
                timeline_column.controls = [self._build_step(step, i) for i, step in enumerate(self.steps)]
                self.page.update()
        except (AttributeError, IndexError, TypeError) as e:
            # Silenciosamente ignorar errores si el diálogo ya se cerró
            pass
    
    def build(self):
        """Retorna el contenedor para ser mostrado"""
        return self.container
