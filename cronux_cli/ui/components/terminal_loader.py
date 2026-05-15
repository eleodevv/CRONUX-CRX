"""
Terminal Loader - Loader minimalista estilo Vercel
"""
import flet as ft


class TerminalLoaderView:
    """Loader visual estilo Vercel - minimalista y elegante"""
    
    def __init__(self, page: ft.Page, title: str):
        self.page = page
        self.title = title
        self.messages = []  # TODOS los mensajes
        self.messages_column = None
        self.current_step_text = None
        self.progress_ring = None
        self.success_icon = None
        self.icon_container = None
        
    def build(self):
        """Construye el loader estilo Vercel"""
        # Texto del paso actual (minimalista)
        self.current_step_text = ft.Text(
            "Iniciando...",
            size=13,
            weight=ft.FontWeight.W_400,
            color="#525252",
            font_family="monospace",
        )
        
        # Columna de mensajes (últimos 6)
        self.messages_column = ft.Column(
            controls=[],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        
        # Progress ring minimalista
        self.progress_ring = ft.ProgressRing(
            width=16,
            height=16,
            stroke_width=2,
            color="#171717",
        )
        
        # Icono de éxito (oculto inicialmente)
        self.success_icon = ft.Container(
            content=ft.Icon(
                ft.Icons.CHECK_CIRCLE,
                size=16,
                color="#171717",
            ),
            visible=False,
        )
        
        # Container que alterna entre progress ring e icono
        self.icon_container = ft.Stack([
            self.progress_ring,
            self.success_icon,
        ])
        
        return ft.Container(
            content=ft.Column([
                # Header minimalista con título
                ft.Container(
                    content=ft.Text(
                        self.title,
                        size=15,
                        weight=ft.FontWeight.W_600,
                        color="#171717",
                    ),
                    padding=ft.Padding(left=0, top=0, right=0, bottom=16),
                ),
                
                # Línea separadora sutil
                ft.Container(
                    height=1,
                    bgcolor="#E5E5E5",
                    margin=ft.Margin(left=0, top=0, right=0, bottom=16),
                ),
                
                # Paso actual con icono a la izquierda
                ft.Row([
                    self.icon_container,
                    ft.Container(width=10),
                    ft.Container(
                        content=self.current_step_text,
                        expand=True,
                    ),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Container(height=12),
                
                # Mensajes recientes (estilo logs de Vercel)
                ft.Container(
                    content=self.messages_column,
                    padding=ft.Padding(left=26, top=0, right=0, bottom=0),
                ),
                
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.START, 
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            ),
            width=480,
            padding=ft.Padding.all(28),
            bgcolor="#FFFFFF",
            border_radius=8,
            border=ft.Border(
                top=ft.BorderSide(1, "#E5E5E5"),
                right=ft.BorderSide(1, "#E5E5E5"),
                bottom=ft.BorderSide(1, "#E5E5E5"),
                left=ft.BorderSide(1, "#E5E5E5"),
            ),
        )
    
    def add_message(self, mensaje: str):
        """Agrega un mensaje estilo logs de Vercel"""
        # Actualizar el paso actual
        self.current_step_text.value = mensaje
        
        # Determinar color y prefijo según el tipo de mensaje (minimalista)
        if "completad" in mensaje.lower() or "instalad" in mensaje.lower() or "creado" in mensaje.lower():
            text_color = "#171717"
            prefix = "✓"
            opacity = 1.0
        elif "error" in mensaje.lower():
            text_color = "#DC2626"
            prefix = "✕"
            opacity = 1.0
        elif "warn" in mensaje.lower() or "⚠" in mensaje:
            text_color = "#F59E0B"
            prefix = "⚠"
            opacity = 1.0
        elif "%" in mensaje:
            text_color = "#737373"
            prefix = "→"
            opacity = 0.9
        else:
            text_color = "#737373"
            prefix = "→"
            opacity = 0.85
        
        # Limpiar mensaje de emojis
        mensaje_clean = mensaje.replace("✓", "").replace("✅", "").replace("❌", "").replace("⚠", "").replace("📂", "").replace("🗑️", "").replace("📦", "").replace("🔧", "").strip()
        
        # Crear mensaje estilo Vercel (simple y limpio)
        mensaje_row = ft.Row([
            ft.Text(
                prefix,
                size=11,
                color=text_color,
                weight=ft.FontWeight.W_500,
                font_family="monospace",
                opacity=opacity,
            ),
            ft.Container(width=6),
            ft.Text(
                mensaje_clean,
                size=11,
                color=text_color,
                weight=ft.FontWeight.W_400,
                font_family="monospace",
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
                opacity=opacity,
            ),
        ], spacing=0)
        
        # Agregar a la lista COMPLETA de mensajes
        self.messages.append(mensaje_row)
        
        # Actualizar la visualización con los últimos 6 mensajes
        self._update_visible_messages()
    
    def _update_visible_messages(self):
        """Actualiza los mensajes visibles mostrando los últimos 6"""
        # Siempre mostrar los últimos 6 mensajes
        if len(self.messages) <= 6:
            self.messages_column.controls = self.messages.copy()
        else:
            self.messages_column.controls = self.messages[-6:]
    
    def update_display(self):
        """Actualiza la visualización"""
        try:
            self.page.update()
        except Exception as e:
            print(f"[ERROR] No se pudo actualizar loader: {e}")
    
    def set_completed(self, success=True):
        """Marca el loader como completado estilo Vercel"""
        # Ocultar progress ring y mostrar icono
        self.progress_ring.visible = False
        
        if success:
            # Mostrar check minimalista
            self.success_icon.visible = True
            self.success_icon.content.name = ft.Icons.CHECK_CIRCLE
            self.success_icon.content.color = "#171717"
            
            # Actualizar texto
            self.current_step_text.value = "Completado"
            self.current_step_text.color = "#171717"
            self.current_step_text.weight = ft.FontWeight.W_500
        else:
            # Mostrar error minimalista
            self.success_icon.visible = True
            self.success_icon.content.name = ft.Icons.CANCEL
            self.success_icon.content.color = "#DC2626"
            
            # Actualizar texto
            self.current_step_text.value = "Error"
            self.current_step_text.color = "#DC2626"
            self.current_step_text.weight = ft.FontWeight.W_500
        
        # Actualizar la visualización
        self.update_display()

