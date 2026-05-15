"""
Pantalla Wizard - Selección de categoría y tecnología con diseño limpio
"""
import flet as ft
import subprocess


# Categorías generales
CATEGORIAS = [
    {"id": "software", "nombre": "Software", "icono": ft.Icons.TERMINAL_ROUNDED, "color": "#667EEA", "has_subtypes": True},
    {"id": "documentos", "nombre": "Documentos", "icono": ft.Icons.ARTICLE_ROUNDED, "color": "#48BB78", "has_subtypes": True},
    {"id": "imagenes", "nombre": "Imágenes", "icono": ft.Icons.PHOTO_LIBRARY_ROUNDED, "color": "#ED8936", "has_subtypes": True},
    {"id": "tareas", "nombre": "Tareas", "icono": ft.Icons.TASK_ALT_ROUNDED, "color": "#F56565"},
    {"id": "investigacion", "nombre": "Investigación", "icono": ft.Icons.BIOTECH_ROUNDED, "color": "#38B2AC"},
    {"id": "diseno", "nombre": "Diseño", "icono": ft.Icons.BRUSH_ROUNDED, "color": "#9F7AEA"},
]

# Tecnologías (solo para categoría Software)
TECNOLOGIAS = [
    {
        "id": "javascript",
        "nombre": "JavaScript",
        "icono": "javascript.png",
        "color": "#F7DF1E",
        "bg": "#FFFBEA",
        "has_subtypes": True,
    },
    {
        "id": "python",
        "nombre": "Python",
        "icono": "python.png",
        "color": "#4299E1",
        "bg": "#EBF8FF",
    },
    {
        "id": "java",
        "nombre": "Java",
        "icono": "java.png",
        "color": "#ED8936",
        "bg": "#FFFAF0",
    },
    {
        "id": "php",
        "nombre": "PHP",
        "icono": "php.png",
        "color": "#8892BF",
        "bg": "#F3F4F6",
    },
    {
        "id": "ruby",
        "nombre": "Ruby",
        "icono": "ruby.png",
        "color": "#F56565",
        "bg": "#FFF5F5",
    },
    {
        "id": "go",
        "nombre": "Go",
        "icono": "go.png",
        "color": "#38B2AC",
        "bg": "#E6FFFA",
    },
    {
        "id": "flutter",
        "nombre": "Flutter",
        "icono": "flutter.png",
        "color": "#02569B",
        "bg": "#E3F2FD",
    },
    {
        "id": "dotnet",
        "nombre": ".NET",
        "icono": ".net.png",
        "color": "#9F7AEA",
        "bg": "#FAF5FF",
    },
    {
        "id": "general",
        "nombre": "General",
        "icono": "lanzamiento-del-proyecto.png",
        "color": "#718096",
        "bg": "#F7FAFC",
    }
]

# Sub-tipos de JavaScript
JS_FRAMEWORKS = [
    {
        "id": "react",
        "nombre": "React",
        "icono": "react.png",
        "color": "#0891B2",
        "bg": "#E0F2FE",
    },
    {
        "id": "vanilla_js",
        "nombre": "Vanilla JS",
        "icono": "javascript.png",
        "color": "#F7DF1E",
        "bg": "#FFFBEA",
    },
    {
        "id": "nodejs",
        "nombre": "Node.js",
        "icono": "node.png",
        "color": "#68D391",
        "bg": "#F0FFF4",
    },
    {
        "id": "general_js",
        "nombre": "General",
        "icono": "lanzamiento-del-proyecto.png",
        "color": "#718096",
        "bg": "#F7FAFC",
    },
]

# Sub-tipos de Documentos
DOCUMENT_TYPES = [
    {
        "id": "word",
        "nombre": "Word",
        "icono": "word.png",
        "color": "#2B579A",
        "bg": "#E3F2FD",
    },
    {
        "id": "excel",
        "nombre": "Excel",
        "icono": "excel.png",
        "color": "#217346",
        "bg": "#E8F5E9",
    },
    {
        "id": "powerpoint",
        "nombre": "PowerPoint",
        "icono": "powerpoint.png",
        "color": "#D24726",
        "bg": "#FFEBEE",
    },
    {
        "id": "pdf",
        "nombre": "PDF",
        "icono": "pdf.png",
        "color": "#F40F02",
        "bg": "#FFEBEE",
    },
    {
        "id": "latex",
        "nombre": "LaTeX",
        "icono": "Latex.png",
        "color": "#008080",
        "bg": "#E0F2F1",
    },
    {
        "id": "general_doc",
        "nombre": "General",
        "icono": "generalDoc.png",
        "color": "#718096",
        "bg": "#F7FAFC",
    },
]

# Sub-tipos de Imágenes
IMAGE_TYPES = [
    {
        "id": "png",
        "nombre": "PNG",
        "icono": "png.png",
        "color": "#10B981",
        "bg": "#ECFDF5",
    },
    {
        "id": "jpg",
        "nombre": "JPG",
        "icono": "jpg.png",
        "color": "#F59E0B",
        "bg": "#FEF3C7",
    },
    {
        "id": "svg",
        "nombre": "SVG",
        "icono": "svg.png",
        "color": "#8B5CF6",
        "bg": "#F3E8FF",
    },
    {
        "id": "gif",
        "nombre": "GIF",
        "icono": "gif.png",
        "color": "#EC4899",
        "bg": "#FCE7F3",
    },
    {
        "id": "raw",
        "nombre": "RAW",
        "icono": "raw.png",
        "color": "#6366F1",
        "bg": "#EEF2FF",
    },
    {
        "id": "general_img",
        "nombre": "General",
        "icono": "generalimagen.png",
        "color": "#718096",
        "bg": "#F7FAFC",
    },
]


class WizardScreen:
    """Wizard con diseño limpio y moderno"""
    
    def __init__(self, page: ft.Page, on_close, on_create):
        self.page = page
        self.on_close = on_close
        self.on_create = on_create
        
        # Estado
        self.current_step = 0  # 0: category, 1: tech, 1.5: js_framework (si es JS), 1.6: doc_type (si es Documentos), 1.7: img_type (si es Imágenes), 2: form, 3: success
        self.selected_category = None
        self.selected_tech = None
        self.selected_js_framework = None
        self.selected_doc_type = None
        self.selected_img_type = None
        self.project_name = ""
        self.project_path = ""
        self.create_initial_version = True  # Por defecto crear primera versión
        
        # Campo nombre
        self.name_field = ft.TextField(
            hint_text="mi-proyecto-increible",
            label="Nombre del proyecto",
            border_radius=10,
            height=50,
            text_size=15,
            bgcolor="#FFFFFF",
            border_color="#E2E8F0",
            focused_border_color="#667EEA",
            color="#2D3748",
            on_change=lambda e: setattr(self, 'project_name', e.control.value),
        )
    
    def build(self):
        """Construye la vista según el paso"""
        if self.current_step == 0:
            return self._build_category_selection()
        elif self.current_step == 1:
            return self._build_tech_selection()
        elif self.current_step == 1.5:
            return self._build_js_framework_selection()
        elif self.current_step == 1.6:
            return self._build_document_type_selection()
        elif self.current_step == 1.7:
            return self._build_image_type_selection()
        elif self.current_step == 2:
            return self._build_form()
        else:
            return self._build_success()
    
    def _build_category_selection(self):
        """Paso 0: Selección de categoría"""
        return ft.Container(
            content=ft.Column([
                # Botón volver arriba a la izquierda
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="#718096",
                            icon_size=24,
                            on_click=lambda _: self.on_close(),
                            tooltip="Volver",
                        ),
                    ]),
                    padding=ft.Padding.all(16),
                ),
                
                ft.Container(height=60),
                
                # Contenido centrado con más padding
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "¿Qué tipo de proyecto es?",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color="#1A202C",
                        ),
                        
                        ft.Container(height=48),
                        
                        # Grid simple 3x2 con más espacio
                        ft.Column([
                            ft.Row([
                                self._create_category_card(CATEGORIAS[0]),
                                self._create_category_card(CATEGORIAS[1]),
                                self._create_category_card(CATEGORIAS[2]),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
                            ft.Container(height=28),
                            ft.Row([
                                self._create_category_card(CATEGORIAS[3]),
                                self._create_category_card(CATEGORIAS[4]),
                                self._create_category_card(CATEGORIAS[5]),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
                        ]),
                        
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding.symmetric(horizontal=80),
                ),
                
                ft.Container(expand=True),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor="#FFFFFF",
        )
    
    def _build_js_framework_selection(self):
        """Paso 1.5: Selección de framework JavaScript"""
        return ft.Container(
            content=ft.Column([
                # Botón volver arriba a la izquierda
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="#718096",
                            icon_size=24,
                            on_click=lambda _: self._go_back_to_tech(),
                            tooltip="Volver",
                        ),
                    ]),
                    padding=ft.Padding.all(16),
                ),
                
                ft.Container(expand=True),
                
                # Contenido centrado
                ft.Column([
                    # Icono de JavaScript arriba
                    ft.Container(
                        content=ft.Image(src="javascript.png", width=64, height=64),
                        padding=ft.Padding.all(16),
                        border_radius=20,
                        bgcolor="#FFFBEA",
                        border=ft.Border.all(2, "#F7DF1E"),
                    ),
                    
                    ft.Container(height=24),
                    
                    ft.Text(
                        "¿Qué tipo de proyecto JavaScript?",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=8),
                    
                    ft.Text(
                        "Elige el framework o entorno para tu proyecto",
                        size=15,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=40),
                    
                    # Grid 1x4 para frameworks JS (centrado y más grande)
                    ft.Row([
                        self._create_js_framework_card(JS_FRAMEWORKS[0]),
                        self._create_js_framework_card(JS_FRAMEWORKS[1]),
                        self._create_js_framework_card(JS_FRAMEWORKS[2]),
                        self._create_js_framework_card(JS_FRAMEWORKS[3]),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Container(expand=True),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor="#FFFFFF",
        )
    
    def _build_document_type_selection(self):
        """Paso 1.6: Selección de tipo de documento"""
        return ft.Container(
            content=ft.Column([
                # Botón volver arriba a la izquierda
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="#718096",
                            icon_size=24,
                            on_click=lambda _: self._go_back_to_category(),
                            tooltip="Volver",
                        ),
                    ]),
                    padding=ft.Padding.all(8),
                ),
                
                # Contenido centrado
                ft.Column([
                    # Icono de Documentos arriba
                    ft.Container(
                        content=ft.Icon(ft.Icons.ARTICLE_ROUNDED, size=44, color="#48BB78"),
                        padding=ft.Padding.all(11),
                        border_radius=14,
                        bgcolor="#F0FFF4",
                        border=ft.Border.all(2, "#48BB78"),
                    ),
                    
                    ft.Container(height=12),
                    
                    ft.Text(
                        "¿Qué tipo de documento?",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=4),
                    
                    ft.Text(
                        "Elige el formato de documento para tu proyecto",
                        size=13,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Grid 2x3 para tipos de documento
                    ft.Column([
                        ft.Row([
                            self._create_document_type_card(DOCUMENT_TYPES[0]),
                            self._create_document_type_card(DOCUMENT_TYPES[1]),
                            self._create_document_type_card(DOCUMENT_TYPES[2]),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
                        ft.Container(height=12),
                        ft.Row([
                            self._create_document_type_card(DOCUMENT_TYPES[3]),
                            self._create_document_type_card(DOCUMENT_TYPES[4]),
                            self._create_document_type_card(DOCUMENT_TYPES[5]),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
                    ]),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Container(expand=True),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor="#FFFFFF",
        )
    
    def _build_image_type_selection(self):
        """Paso 1.7: Selección de tipo de imagen"""
        return ft.Container(
            content=ft.Column([
                # Botón volver arriba a la izquierda
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="#718096",
                            icon_size=24,
                            on_click=lambda _: self._go_back_to_category(),
                            tooltip="Volver",
                        ),
                    ]),
                    padding=ft.Padding.all(8),
                ),
                
                # Contenido centrado
                ft.Column([
                    # Icono de Imágenes arriba
                    ft.Container(
                        content=ft.Icon(ft.Icons.PHOTO_LIBRARY_ROUNDED, size=44, color="#ED8936"),
                        padding=ft.Padding.all(11),
                        border_radius=14,
                        bgcolor="#FFF7ED",
                        border=ft.Border.all(2, "#ED8936"),
                    ),
                    
                    ft.Container(height=12),
                    
                    ft.Text(
                        "¿Qué tipo de imagen?",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=4),
                    
                    ft.Text(
                        "Elige el formato de imagen para tu proyecto",
                        size=13,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Grid 2x3 para tipos de imagen
                    ft.Column([
                        ft.Row([
                            self._create_image_type_card(IMAGE_TYPES[0]),
                            self._create_image_type_card(IMAGE_TYPES[1]),
                            self._create_image_type_card(IMAGE_TYPES[2]),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
                        ft.Container(height=12),
                        ft.Row([
                            self._create_image_type_card(IMAGE_TYPES[3]),
                            self._create_image_type_card(IMAGE_TYPES[4]),
                            self._create_image_type_card(IMAGE_TYPES[5]),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
                    ]),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Container(expand=True),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor="#FFFFFF",
        )
    
    def _create_js_framework_card(self, framework):
        """Card para frameworks de JavaScript"""
        is_selected = self.selected_js_framework and self.selected_js_framework["id"] == framework["id"]
        
        return ft.Container(
            content=ft.Column([
                ft.Image(src=framework["icono"], width=48, height=48),
                ft.Container(height=12),
                ft.Text(
                    framework["nombre"],
                    size=15,
                    weight=ft.FontWeight.W_600,
                    color=framework["color"] if is_selected else "#1A202C",
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=180,
            height=130,
            padding=ft.Padding.all(24),
            border_radius=12,
            bgcolor=framework["bg"] if is_selected else "#FFFFFF",
            border=ft.Border.all(2 if is_selected else 1, framework["color"] if is_selected else "#E2E8F0"),
            on_click=lambda _, f=framework: self._select_js_framework(f),
            on_hover=lambda e, f=framework: self._on_js_framework_hover(e, f),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _create_document_type_card(self, doc_type):
        """Card para tipos de documento - diseño grande y mejorado"""
        is_selected = self.selected_doc_type and self.selected_doc_type["id"] == doc_type["id"]
        
        return ft.Container(
            content=ft.Column([
                # Icono grande con fondo
                ft.Container(
                    content=ft.Image(src=doc_type["icono"], width=64, height=64),
                    padding=ft.Padding.all(15),
                    border_radius=14,
                    bgcolor=doc_type["bg"],
                ),
                ft.Container(height=10),
                ft.Text(
                    doc_type["nombre"],
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=doc_type["color"] if is_selected else "#1A202C",
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=190,
            height=175,
            padding=ft.Padding.only(left=20, right=20, top=20, bottom=24),
            border_radius=14,
            bgcolor="#FFFFFF",
            border=ft.Border.all(2 if is_selected else 1, doc_type["color"] if is_selected else "#E2E8F0"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8 if is_selected else 4,
                color=ft.Colors.with_opacity(0.1 if is_selected else 0.05, "#000000"),
                offset=ft.Offset(0, 2),
            ),
            on_click=lambda _, d=doc_type: self._select_document_type(d),
            on_hover=lambda e, d=doc_type: self._on_document_type_hover(e, d),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _on_js_framework_hover(self, e, framework):
        """Efecto hover para frameworks JS"""
        is_selected = self.selected_js_framework and self.selected_js_framework["id"] == framework["id"]
        
        if e.data == "true":  # Mouse entra
            if not is_selected:
                e.control.bgcolor = framework["bg"]
                e.control.border = ft.Border.all(2, framework["color"])
                e.control.update()
        else:  # Mouse sale
            if not is_selected:
                e.control.bgcolor = "#FFFFFF"
                e.control.border = ft.Border.all(1, "#E2E8F0")
                e.control.update()
    
    def _on_document_type_hover(self, e, doc_type):
        """Efecto hover para tipos de documento"""
        is_selected = self.selected_doc_type and self.selected_doc_type["id"] == doc_type["id"]
        
        if e.data == "true":  # Mouse entra
            if not is_selected:
                e.control.bgcolor = doc_type["bg"]
                e.control.border = ft.Border.all(2, doc_type["color"])
                e.control.update()
        else:  # Mouse sale
            if not is_selected:
                e.control.bgcolor = "#FFFFFF"
                e.control.border = ft.Border.all(1, "#E2E8F0")
                e.control.update()
    
    def _select_js_framework(self, framework):
        """Selecciona framework de JavaScript"""
        self.selected_js_framework = framework
        self.page.update()
        
        import time
        time.sleep(0.15)
        
        self.current_step = 2
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _select_document_type(self, doc_type):
        """Selecciona tipo de documento"""
        self.selected_doc_type = doc_type
        self.page.update()
        
        import time
        time.sleep(0.15)
        
        self.current_step = 2
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _create_image_type_card(self, img_type):
        """Card para tipos de imagen"""
        is_selected = self.selected_img_type and self.selected_img_type["id"] == img_type["id"]
        
        return ft.Container(
            content=ft.Column([
                # Icono grande con fondo
                ft.Container(
                    content=ft.Image(src=img_type["icono"], width=64, height=64),
                    padding=ft.Padding.all(15),
                    border_radius=14,
                    bgcolor=img_type["bg"],
                ),
                ft.Container(height=10),
                ft.Text(
                    img_type["nombre"],
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=img_type["color"] if is_selected else "#1A202C",
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=190,
            height=175,
            padding=ft.Padding.only(left=20, right=20, top=20, bottom=24),
            border_radius=14,
            bgcolor="#FFFFFF",
            border=ft.Border.all(2 if is_selected else 1, img_type["color"] if is_selected else "#E2E8F0"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8 if is_selected else 4,
                color=ft.Colors.with_opacity(0.1 if is_selected else 0.05, "#000000"),
                offset=ft.Offset(0, 2),
            ),
            on_click=lambda _, i=img_type: self._select_image_type(i),
            on_hover=lambda e, i=img_type: self._on_image_type_hover(e, i),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _on_image_type_hover(self, e, img_type):
        """Efecto hover para tipos de imagen"""
        is_selected = self.selected_img_type and self.selected_img_type["id"] == img_type["id"]
        
        if e.data == "true":  # Mouse entra
            if not is_selected:
                e.control.bgcolor = img_type["bg"]
                e.control.border = ft.Border.all(2, img_type["color"])
                e.control.update()
        else:  # Mouse sale
            if not is_selected:
                e.control.bgcolor = "#FFFFFF"
                e.control.border = ft.Border.all(1, "#E2E8F0")
                e.control.update()
    
    def _select_image_type(self, img_type):
        """Selecciona tipo de imagen"""
        self.selected_img_type = img_type
        self.page.update()
        
        import time
        time.sleep(0.15)
        
        self.current_step = 2
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _go_back_to_tech(self):
        """Volver a selección de tecnología"""
        self.selected_js_framework = None
        self.current_step = 1
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _build_tech_selection(self):
        """Paso 1: Selección de tecnología (solo si categoría es Software)"""
        return ft.Container(
            content=ft.Column([
                # Botón volver arriba a la izquierda
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="#718096",
                            icon_size=24,
                            on_click=lambda _: self._go_back_to_category(),
                            tooltip="Volver",
                        ),
                    ]),
                    padding=ft.Padding.all(8),
                ),
                
                # Contenido centrado
                ft.Column([
                    # Icono de Software arriba
                    ft.Container(
                        content=ft.Icon(ft.Icons.TERMINAL_ROUNDED, size=40, color="#667EEA"),
                        padding=ft.Padding.all(10),
                        border_radius=12,
                        bgcolor="#EEF2FF",
                        border=ft.Border.all(2, "#667EEA"),
                    ),
                    
                    ft.Container(height=10),
                    
                    ft.Text(
                        "Selecciona tu tecnología",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=3),
                    
                    ft.Text(
                        "Elige la tecnología para tu proyecto de software",
                        size=12,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=16),
                    
                    # Layout con General grande a la derecha
                    ft.Row([
                        # Columna izquierda: 8 tecnologías en grid 4x2
                        ft.Column([
                            ft.Row([
                                self._create_tech_card_simple(TECNOLOGIAS[0]),
                                self._create_tech_card_simple(TECNOLOGIAS[1]),
                                self._create_tech_card_simple(TECNOLOGIAS[2]),
                                self._create_tech_card_simple(TECNOLOGIAS[3]),
                            ], spacing=12),
                            ft.Container(height=10),
                            ft.Row([
                                self._create_tech_card_simple(TECNOLOGIAS[4]),
                                self._create_tech_card_simple(TECNOLOGIAS[5]),
                                self._create_tech_card_simple(TECNOLOGIAS[6]),
                                self._create_tech_card_simple(TECNOLOGIAS[7]),
                            ], spacing=12),
                        ]),
                        
                        ft.Container(width=12),
                        
                        # Card grande de General a la derecha
                        self._create_tech_card_large(TECNOLOGIAS[8]),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Container(expand=True),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor="#FFFFFF",
        )
    
    def _create_category_card(self, category):
        """Card de categoría con efecto hover"""
        is_selected = self.selected_category and self.selected_category["id"] == category["id"]
        
        # Crear referencias a los controles para poder actualizarlos
        icon_ref = ft.Ref[ft.Icon]()
        text_ref = ft.Ref[ft.Text]()
        
        def on_hover(e):
            if e.data == "true":  # Mouse entra
                if not is_selected:
                    e.control.bgcolor = ft.Colors.with_opacity(0.08, category["color"])
                    e.control.border = ft.Border.all(2, category["color"])
                    icon_ref.current.color = category["color"]
                    text_ref.current.color = category["color"]
                    e.control.update()
            else:  # Mouse sale
                if not is_selected:
                    e.control.bgcolor = "#FFFFFF"
                    e.control.border = ft.Border.all(1, "#E2E8F0")
                    icon_ref.current.color = "#718096"
                    text_ref.current.color = "#1A202C"
                    e.control.update()
        
        return ft.Container(
            content=ft.Column([
                ft.Icon(
                    category["icono"],
                    size=48,
                    color=category["color"] if is_selected else "#718096",
                    ref=icon_ref
                ),
                ft.Container(height=12),
                ft.Text(
                    category["nombre"],
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=category["color"] if is_selected else "#1A202C",
                    ref=text_ref
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=200,
            height=140,
            padding=ft.padding.all(24),
            border_radius=12,
            bgcolor="#FFFFFF",
            border=ft.Border.all(2 if is_selected else 1, category["color"] if is_selected else "#E2E8F0"),
            on_click=lambda _, c=category: self._select_category(c),
            on_hover=on_hover,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _create_tech_card_simple(self, tech):
        """Card de tecnología con diseño mejorado"""
        is_selected = self.selected_tech and self.selected_tech["id"] == tech["id"]
        
        return ft.Container(
            content=ft.Column([
                # Icono grande con fondo
                ft.Container(
                    content=ft.Image(src=tech["icono"], width=56, height=56),
                    padding=ft.Padding.all(13),
                    border_radius=12,
                    bgcolor=tech["bg"],
                ),
                ft.Container(height=8),
                ft.Text(
                    tech["nombre"],
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=tech["color"] if is_selected else "#1A202C",
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=175,
            height=155,
            padding=ft.Padding.only(left=18, right=18, top=18, bottom=20),
            border_radius=12,
            bgcolor="#FFFFFF",
            border=ft.Border.all(2 if is_selected else 1, tech["color"] if is_selected else "#E2E8F0"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8 if is_selected else 4,
                color=ft.Colors.with_opacity(0.1 if is_selected else 0.05, "#000000"),
                offset=ft.Offset(0, 2),
            ),
            on_click=lambda _, t=tech: self._select_tech(t),
            on_hover=lambda e, t=tech: self._on_tech_hover(e, t),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _create_tech_card_large(self, tech):
        """Card grande de tecnología (para General)"""
        is_selected = self.selected_tech and self.selected_tech["id"] == tech["id"]
        
        return ft.Container(
            content=ft.Column([
                ft.Container(expand=True),
                # Icono grande con fondo
                ft.Container(
                    content=ft.Image(src=tech["icono"], width=80, height=80),
                    padding=ft.Padding.all(20),
                    border_radius=16,
                    bgcolor=tech["bg"],
                ),
                ft.Container(height=12),
                ft.Text(
                    tech["nombre"],
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=tech["color"] if is_selected else "#1A202C",
                ),
                ft.Container(expand=True),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=200,
            height=320,  # Altura de 2 cards + espacio entre ellas (155*2 + 10)
            padding=ft.Padding.all(24),
            border_radius=14,
            bgcolor="#FFFFFF",
            border=ft.Border.all(2 if is_selected else 1, tech["color"] if is_selected else "#E2E8F0"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10 if is_selected else 6,
                color=ft.Colors.with_opacity(0.12 if is_selected else 0.06, "#000000"),
                offset=ft.Offset(0, 3),
            ),
            on_click=lambda _, t=tech: self._select_tech(t),
            on_hover=lambda e, t=tech: self._on_tech_hover(e, t),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _on_category_hover(self, e, category):
        """Efecto hover que ilumina la card de categoría con su color"""
        is_selected = self.selected_category and self.selected_category["id"] == category["id"]
        
        if e.data == "true":  # Mouse entra
            if not is_selected:
                # Fondo suave del color de la categoría
                e.control.bgcolor = ft.Colors.with_opacity(0.08, category["color"])
                e.control.border = ft.Border.all(2, category["color"])
                e.control.content.controls[0].color = category["color"]
                e.control.content.controls[2].color = category["color"]
        else:  # Mouse sale
            if not is_selected:
                e.control.bgcolor = "#FFFFFF"
                e.control.border = ft.Border.all(1, "#E2E8F0")
                e.control.content.controls[0].color = "#718096"
                e.control.content.controls[2].color = "#1A202C"
        e.control.update()
    
    def _on_tech_hover(self, e, tech):
        """Efecto hover que ilumina la card de tecnología"""
        is_selected = self.selected_tech and self.selected_tech["id"] == tech["id"]
        
        if e.data == "true":  # Mouse entra
            if not is_selected:
                e.control.bgcolor = tech["bg"]
                e.control.border = ft.Border.all(2, tech["color"])
                e.control.update()
        else:  # Mouse sale
            if not is_selected:
                e.control.bgcolor = "#FFFFFF"
                e.control.border = ft.Border.all(1, "#E2E8F0")
                e.control.update()
    
    def _select_category(self, category):
        """Selecciona categoría"""
        self.selected_category = category
        self.page.update()
        
        import time
        time.sleep(0.15)
        
        # Si es Software, ir a selección de tecnología
        if category["id"] == "software":
            self.current_step = 1
        # Si es Documentos, ir a selección de tipo de documento
        elif category["id"] == "documentos":
            self.current_step = 1.6
        # Si es Imágenes, ir a selección de tipo de imagen
        elif category["id"] == "imagenes":
            self.current_step = 1.7
        # Si tiene subtipos, ir al submenú correspondiente
        elif category.get("has_subtypes"):
            self.current_step = 1.6
        else:
            # Para otras categorías, ir directo al formulario
            self.current_step = 2
        
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _select_tech(self, tech):
        """Selecciona tecnología"""
        self.selected_tech = tech
        self.page.update()
        
        import time
        time.sleep(0.15)
        
        # Si es JavaScript, mostrar sub-opciones de frameworks
        if tech.get("has_subtypes"):
            self.current_step = 1.5
        else:
            self.current_step = 2
        
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _build_form(self):
        """Paso 2: Formulario con diseño completamente nuevo"""
        # Determinar color según categoría, tecnología, framework JS, tipo de documento o tipo de imagen
        if self.selected_js_framework:
            color = self.selected_js_framework["color"]
            icon_src = self.selected_js_framework["icono"]
            nombre = self.selected_js_framework["nombre"]
        elif self.selected_doc_type:
            color = self.selected_doc_type["color"]
            icon_src = self.selected_doc_type["icono"]
            nombre = self.selected_doc_type["nombre"]
        elif self.selected_img_type:
            color = self.selected_img_type["color"]
            icon_src = self.selected_img_type["icono"]
            nombre = self.selected_img_type["nombre"]
        elif self.selected_tech:
            color = self.selected_tech["color"]
            icon_src = self.selected_tech["icono"]
            nombre = self.selected_tech["nombre"]
        else:
            color = self.selected_category["color"]
            icon_src = None
            nombre = self.selected_category["nombre"]
        
        return ft.Container(
            content=ft.Row([
                # Columna izquierda - Formulario (responsiva)
                ft.Container(
                    content=ft.Column([
                        # Botón volver en esquina superior izquierda
                        ft.Container(
                            content=ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color="#A0AEC0",
                                    icon_size=22,
                                    on_click=lambda _: self._go_back(),
                                ),
                            ]),
                            padding=ft.Padding.all(16),
                        ),
                        
                        ft.Container(expand=True),
                        
                        # Formulario
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    "Configura tu proyecto",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color="#1A202C",
                                ),
                                
                                ft.Container(height=8),
                                
                                ft.Text(
                                    "Completa los datos para crear tu proyecto",
                                    size=14,
                                    color="#718096",
                                ),
                                
                                ft.Container(height=40),
                                
                                # Campo nombre
                                ft.Column([
                                    ft.Text("Nombre del proyecto", size=13, weight=ft.FontWeight.W_600, color="#2D3748"),
                                    ft.Container(height=8),
                                    ft.TextField(
                                        hint_text="mi-proyecto-increible",
                                        border_radius=10,
                                        text_size=15,
                                        bgcolor="#F7FAFC",
                                        border_color="transparent",
                                        focused_border_color=color,
                                        focused_bgcolor="#F7FAFC",
                                        color="#2D3748",
                                        content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
                                        on_change=lambda e: setattr(self, 'project_name', e.control.value),
                                        expand=True,
                                    ),
                                ], spacing=0),
                                
                                ft.Container(height=24),
                                
                                # Campo carpeta mejorado
                                ft.Column([
                                    ft.Text("Ubicación", size=13, weight=ft.FontWeight.W_600, color="#2D3748"),
                                    ft.Container(height=8),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Icon(ft.Icons.FOLDER_OPEN_ROUNDED, size=20, color=color),
                                                ft.Container(width=12),
                                                ft.Text(
                                                    "Seleccionar carpeta del proyecto",
                                                    size=14,
                                                    color="#2D3748",
                                                    weight=ft.FontWeight.W_500,
                                                ),
                                                ft.Container(expand=True),
                                                ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color="#A0AEC0"),
                                            ]),
                                            # Mostrar ruta si está seleccionada
                                            ft.Container(
                                                content=ft.Row([
                                                    ft.Icon(ft.Icons.FOLDER_OUTLINED, size=14, color="#718096"),
                                                    ft.Container(width=6),
                                                    ft.Text(
                                                        self.project_path,
                                                        size=12,
                                                        color="#718096",
                                                        max_lines=1,
                                                        overflow=ft.TextOverflow.ELLIPSIS,
                                                        expand=True,
                                                    ),
                                                ]),
                                                margin=ft.Margin(top=8, left=0, right=0, bottom=0),
                                                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                                                border_radius=6,
                                                bgcolor="#EDF2F7",
                                            ) if self.project_path else ft.Container(),
                                        ]),
                                        padding=ft.Padding.all(16),
                                        border_radius=10,
                                        bgcolor="#F7FAFC",
                                        on_click=lambda _: self._select_folder(),
                                        ink=True,
                                    ),
                                ], spacing=0),
                                
                                ft.Container(height=24),
                                
                                # Checkbox para crear primera versión
                                ft.Container(
                                    content=ft.Row([
                                        ft.Checkbox(
                                            value=True,
                                            fill_color=color,
                                            check_color="#FFFFFF",
                                            on_change=lambda e: setattr(self, 'create_initial_version', e.control.value),
                                        ),
                                        ft.Column([
                                            ft.Text(
                                                "Crear primera versión automáticamente",
                                                size=14,
                                                weight=ft.FontWeight.W_600,
                                                color="#2D3748",
                                            ),
                                            ft.Text(
                                                "Guarda el estado inicial de tu proyecto",
                                                size=12,
                                                color="#718096",
                                            ),
                                        ], spacing=2),
                                    ], spacing=8),
                                    padding=ft.Padding.all(16),
                                    border_radius=10,
                                    bgcolor="#F7FAFC",
                                ),
                                
                            ], horizontal_alignment=ft.CrossAxisAlignment.START),
                            padding=ft.Padding.symmetric(horizontal=60),
                        ),
                        
                        ft.Container(expand=True),
                        
                    ]),
                    expand=True,
                    bgcolor="#FFFFFF",
                ),
                
                # Columna derecha - Icono, nombre y botón
                ft.Container(
                    content=ft.Column([
                        ft.Container(expand=True),
                        
                        # Icono grande
                        ft.Image(src=icon_src, width=180, height=180) if icon_src else ft.Icon(self.selected_category["icono"], size=180, color=color),
                        
                        ft.Container(height=24),
                        
                        # Nombre
                        ft.Text(nombre, size=36, weight=ft.FontWeight.BOLD, color=color),
                        
                        ft.Container(height=8),
                        
                        ft.Text("Proyecto", size=15, color="#A0AEC0"),
                        
                        ft.Container(height=48),
                        
                        # Botón crear aquí
                        ft.Container(
                            content=ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Text("Crear Proyecto", size=15, weight=ft.FontWeight.W_600),
                                    ft.Container(expand=True),
                                    ft.Icon(ft.Icons.ARROW_FORWARD, size=18),
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                on_click=lambda _: self._continue(),
                                style=ft.ButtonStyle(
                                    bgcolor=color,
                                    color="#FFFFFF",
                                    padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation=0,
                                ),
                                width=280,
                            ),
                        ),
                        
                        ft.Container(expand=True),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=400,
                    bgcolor=ft.Colors.with_opacity(0.03, color),
                ),
                
            ]),
            expand=True,
            bgcolor="#FFFFFF",
        )
    
    def _build_success(self):
        """Paso 3: Éxito"""
        # Determinar color y nombre según lo seleccionado
        if self.selected_js_framework:
            color = self.selected_js_framework["color"]
            nombre = self.selected_js_framework["nombre"]
        elif self.selected_doc_type:
            color = self.selected_doc_type["color"]
            nombre = self.selected_doc_type["nombre"]
        elif self.selected_img_type:
            color = self.selected_img_type["color"]
            nombre = self.selected_img_type["nombre"]
        elif self.selected_tech:
            color = self.selected_tech["color"]
            nombre = self.selected_tech["nombre"]
        else:
            color = self.selected_category["color"]
            nombre = self.selected_category["nombre"]
        
        return ft.Container(
            content=ft.Column([
                ft.Container(height=60),
                
                # Check animado
                ft.Container(
                    content=ft.Stack([
                        ft.Container(
                            width=100,
                            height=100,
                            border_radius=50,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.Alignment(-1, -1),
                                end=ft.alignment.Alignment(1, 1),
                                colors=[color, ft.Colors.with_opacity(0.8, color)],
                            ),
                        ),
                        ft.Container(
                            content=ft.Icon(ft.Icons.CHECK_ROUNDED, size=50, color="#FFFFFF"),
                            width=100,
                            height=100,
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                    ]),
                    animate_scale=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT),
                ),
                
                ft.Container(height=24),
                
                ft.Text(
                    "¡Proyecto creado!",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color="#2D3748",
                ),
                
                ft.Container(height=6),
                
                ft.Text(
                    f"Tu proyecto {nombre} está listo",
                    size=15,
                    color="#718096",
                ),
                
                ft.Container(height=28),
                
                # Info
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.LABEL_OUTLINED, color=color, size=18),
                            ft.Container(width=10),
                            ft.Text(f"Nombre: {self.project_name}", size=15, color="#2D3748"),
                        ]),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Icon(ft.Icons.FOLDER_OUTLINED, color=color, size=18),
                            ft.Container(width=10),
                            ft.Text(f"Ubicación: {self.project_path}", size=15, color="#2D3748"),
                        ]),
                    ]),
                    padding=ft.Padding.all(20),
                    border_radius=10,
                    bgcolor="#FFFFFF",
                    border=ft.Border.all(1, "#E2E8F0"),
                    width=450,
                ),
                
                ft.Container(height=28),
                
                # Botones
                ft.Row([
                    ft.ElevatedButton(
                        "Crear Otro",
                        on_click=lambda _: self.on_close(),
                        style=ft.ButtonStyle(
                            bgcolor="#FFFFFF",
                            color="#718096",
                            padding=ft.Padding.symmetric(horizontal=22, vertical=14),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=ft.BorderSide(1, "#E2E8F0"),
                        ),
                    ),
                    ft.Container(width=12),
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Abrir Proyecto",
                            on_click=lambda _: self._finish(),
                            style=ft.ButtonStyle(
                                padding=ft.Padding.symmetric(horizontal=22, vertical=14),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=0,
                            ),
                        ),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.Alignment(-1, 0),
                            end=ft.alignment.Alignment(1, 0),
                            colors=[color, ft.Colors.with_opacity(0.8, color)],
                        ),
                        border_radius=10,
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
            expand=True,
            bgcolor="#FAFAFA",
        )
    
    def _go_back_to_category(self):
        """Volver a selección de categoría"""
        self.current_step = 0
        self.selected_category = None
        self.selected_tech = None
        self.selected_js_framework = None
        self.selected_doc_type = None
        self.selected_img_type = None
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _go_back(self):
        """Volver atrás desde formulario"""
        # Si hay framework JS seleccionado, volver a JS frameworks
        if self.selected_js_framework:
            self.selected_js_framework = None
            self.current_step = 1.5
        # Si hay tipo de documento seleccionado, volver a tipos de documento
        elif self.selected_doc_type:
            self.selected_doc_type = None
            self.current_step = 1.6
        # Si hay tipo de imagen seleccionado, volver a tipos de imagen
        elif self.selected_img_type:
            self.selected_img_type = None
            self.current_step = 1.7
        # Si hay tecnología seleccionada, volver a tech selection
        elif self.selected_tech:
            self.selected_tech = None
            self.selected_js_framework = None
            self.current_step = 1
        else:
            # Si no, volver a categorías
            self.selected_category = None
            self.current_step = 0
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
    
    def _continue(self):
        """Continuar - Llama directamente a finish para crear el proyecto"""
        # Validar que el nombre no esté vacío
        if not self.project_name or not self.project_name.strip():
            self._show_error_snackbar("❌ Por favor ingresa un nombre para el proyecto")
            return
        
        # Validar que se haya seleccionado una carpeta
        if not self.project_path:
            self._show_error_snackbar("❌ Por favor selecciona una carpeta para el proyecto")
            return
        
        # Todo válido, crear el proyecto
        self._finish()
    
    def _show_error_snackbar(self, mensaje):
        """Muestra un snackbar de error"""
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor="#F56565",
            duration=3000,
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()
    
    def _select_folder(self):
        """Seleccionar carpeta"""
        try:
            result = subprocess.run(
                ['zenity', '--file-selection', '--directory', '--title=Seleccionar carpeta'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                self.project_path = result.stdout.strip()
                # Reconstruir la vista para mostrar la ruta
                self.page.controls.clear()
                self.page.add(self.build())
                self.page.update()
        except:
            pass
    
    def _finish(self):
        """Finalizar"""
        # Determinar tipo e icono
        if self.selected_js_framework:
            tipo = self.selected_js_framework["id"]
            icono = self.selected_js_framework.get("icono_src", "")
        elif self.selected_doc_type:
            tipo = self.selected_doc_type["id"]
            tipo = self.selected_doc_type["id"]
        elif self.selected_img_type:
            tipo = self.selected_img_type["id"]
        elif self.selected_tech:
            tipo = self.selected_tech["id"]
        else:
            tipo = self.selected_category["id"]
        
        self.on_create(self.project_name, self.project_path, tipo, self.create_initial_version)
