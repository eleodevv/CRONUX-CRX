"""
Pantalla de Inicio - Lista de proyectos con diseño moderno
"""
import flet as ft


class HomeScreen:
    """Pantalla principal con lista de proyectos"""
    
    def __init__(self, page: ft.Page, on_new_project, on_open_project, proyectos=None):
        self.page = page
        self.on_new_project = on_new_project
        self.on_open_project = on_open_project
        
        # Proyectos
        self.proyectos = proyectos if proyectos is not None else []
        
        # Limpiar automáticamente proyectos deprecados al iniciar
        self._auto_limpiar_proyectos_deprecados()
    
    def build(self):
        """Construye la pantalla principal"""
        return ft.Container(
            content=ft.Column([
                # Header con logo y acciones
                ft.Container(
                    content=ft.Row([
                        # Logo y título
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.HEXAGON, size=24, color="#FFFFFF"),
                                width=48,
                                height=48,
                                border_radius=12,
                                bgcolor="#667EEA",
                                alignment=ft.alignment.Alignment(0, 0),
                            ),
                            ft.Container(width=12),
                            ft.Text("CRONUX-CRX", size=22, weight=ft.FontWeight.BOLD, color="#000000"),
                        ]),
                        
                        ft.Container(expand=True),
                        
                        # Botones de acción
                        ft.Row([
                            # Botón Refrescar/Sincronizar
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.REFRESH, size=16, color="#667EEA"),
                                    ft.Container(width=4),
                                    ft.Text("Sincronizar", size=13, color="#667EEA", weight=ft.FontWeight.W_600),
                                ], spacing=0),
                                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                                border_radius=8,
                                border=ft.border.all(1.5, "#667EEA"),
                                on_click=lambda _: self._sincronizar_proyectos(),
                                tooltip="Busca proyectos nuevos creados desde CLI",
                                ink=True,
                            ),
                            
                            ft.Container(width=8),
                            
                            # Botón Limpiar proyectos deprecados
                            ft.Container(
                                content=ft.Text("Limpiar", size=13, color="#718096", weight=ft.FontWeight.W_600),
                                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                                border_radius=8,
                                bgcolor="#F7FAFC",
                                on_click=lambda _: self._limpiar_proyectos_deprecados(),
                                tooltip="Elimina proyectos que ya no existen",
                                ink=True,
                            ),
                            
                            ft.Container(width=12),
                            
                            # Botón Abrir
                            ft.OutlinedButton(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.FOLDER_OPEN_OUTLINED, size=18, color="#667EEA"),
                                    ft.Container(width=6),
                                    ft.Text("Abrir", size=14, weight=ft.FontWeight.W_600, color="#667EEA"),
                                ], spacing=0),
                                on_click=lambda _: self._abrir_proyecto_existente(),
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1.5, "#667EEA"),
                                    padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            
                            ft.Container(width=12),
                            
                            # Botón Nuevo
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.ROCKET_LAUNCH, size=18, color="#FFFFFF"),
                                    ft.Container(width=6),
                                    ft.Text("Nuevo", size=14, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                                ], spacing=0),
                                on_click=lambda _: self.on_new_project(),
                                style=ft.ButtonStyle(
                                    bgcolor="#667EEA",
                                    padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation=0,
                                ),
                            ),
                        ], spacing=0),
                    ]),
                    padding=ft.Padding.all(24),
                    bgcolor="#FFFFFF",
                    border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
                ),
                
                # Contenido principal
                ft.Container(
                    content=self._build_content(),
                    expand=True,
                    padding=ft.Padding.all(24),
                ),
                
            ], spacing=0),
            expand=True,
            bgcolor="#F7FAFC",
        )
    
    def _build_content(self):
        """Construye el contenido según si hay proyectos o no"""
        if not self.proyectos:
            # Estado vacío
            return ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.FOLDER_OPEN_OUTLINED, size=80, color="#CBD5E0"),
                        width=160, height=160, border_radius=80, bgcolor="#FFFFFF",
                        alignment=ft.alignment.Alignment(0, 0),
                        border=ft.Border.all(2, "#E2E8F0"),
                    ),
                    ft.Container(height=24),
                    ft.Text("No hay proyectos", size=24, weight=ft.FontWeight.BOLD, color="#2D3748"),
                    ft.Container(height=8),
                    ft.Text("Crea tu primer proyecto para comenzar", size=16, color="#718096"),
                    ft.Container(height=32),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ROCKET_LAUNCH_ROUNDED, size=20, color="#FFFFFF"),
                            ft.Container(width=8),
                            ft.Text("Crear Primer Proyecto", size=16, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        on_click=lambda _: self.on_new_project(),
                        style=ft.ButtonStyle(
                            bgcolor="#667EEA",
                            padding=ft.Padding.symmetric(horizontal=32, vertical=18),
                            shape=ft.RoundedRectangleBorder(radius=12),
                            elevation=0,
                        ),
                        width=260, height=56,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                alignment=ft.alignment.Alignment(0, 0),
            )
        else:
            # Cargar favoritos
            from cli_integration import cargar_favoritos, toggle_favorito
            self._favoritos = cargar_favoritos()

            # Ordenar: favoritos primero
            proyectos_ordenados = sorted(
                self.proyectos,
                key=lambda p: (0 if p.get("ruta") in self._favoritos else 1, p.get("nombre", ""))
            )

            self._proyectos_column = ft.Column(
                [self._create_project_card(p) for p in proyectos_ordenados],
                spacing=12,
            )

            def on_search(e):
                query = e.control.value.strip().lower()
                for ctrl in self._proyectos_column.controls:
                    # Buscar en el data-ruta del card
                    p_ruta = getattr(ctrl, '_proyecto_ruta', '')
                    p_nombre = getattr(ctrl, '_proyecto_nombre', '')
                    p_tipo = getattr(ctrl, '_proyecto_tipo', '')
                    visible = (
                        query == "" or
                        query in p_nombre.lower() or
                        query in p_ruta.lower() or
                        query in p_tipo.lower()
                    )
                    ctrl.visible = visible
                self._proyectos_column.update()

            return ft.Column([
                ft.Row([
                    ft.Text("Proyectos", size=20, weight=ft.FontWeight.BOLD, color="#2D3748"),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SEARCH, size=20, color="#A0AEC0"),
                            ft.Container(width=8),
                            ft.TextField(
                                hint_text="Buscar proyectos...",
                                border="none",
                                text_size=14,
                                width=200,
                                text_align=ft.TextAlign.LEFT,
                                on_change=on_search,
                            ),
                        ], alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.Padding.all(10),
                        border_radius=10,
                        bgcolor="#FFFFFF",
                        border=ft.Border.all(1, "#E2E8F0"),
                    ),
                ]),
                ft.Container(height=20),
                self._proyectos_column,
            ], scroll=ft.ScrollMode.AUTO)
    
    def _create_project_card(self, proyecto):
        """Crea una card de proyecto más grande y completamente clickable"""
        from cli_integration import toggle_favorito
        icono_src = proyecto.get("icono")
        tipo = proyecto.get("tipo", "general")
        ruta = proyecto.get("ruta", "")
        es_favorito = ruta in getattr(self, '_favoritos', set())

        iconos_flet = {
            "tareas": ft.Icons.ASSIGNMENT_ROUNDED,
            "investigacion": ft.Icons.SCIENCE_ROUNDED,
            "diseno": ft.Icons.PALETTE_ROUNDED,
        }

        if icono_src:
            icono_widget = ft.Image(src=icono_src, width=48, height=48)
        elif tipo.lower() in iconos_flet:
            icono_widget = ft.Icon(iconos_flet[tipo.lower()], size=40, color="#667EEA")
        else:
            icono_widget = ft.Icon(ft.Icons.FOLDER, size=36, color="#667EEA")

        # Botón de favorito con estado reactivo
        fav_container_ref = ft.Ref[ft.Container]()

        def toggle_fav(e, p=proyecto):
            es_fav_ahora = toggle_favorito(p["ruta"])
            if es_fav_ahora:
                self._favoritos.add(ruta)
            else:
                self._favoritos.discard(ruta)
            # Actualizar icono y color del contenedor
            fav_container_ref.current.content = ft.Icon(
                ft.Icons.STAR_ROUNDED if es_fav_ahora else ft.Icons.STAR_OUTLINE_ROUNDED,
                size=22,
                color="#F59E0B" if es_fav_ahora else "#CBD5E0",
            )
            fav_container_ref.current.bgcolor = "#FFFBEB" if es_fav_ahora else "#F7FAFC"
            fav_container_ref.current.update()
            # Reordenar lista con animación
            self._reordenar_con_animacion()

        card = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=icono_widget,
                    width=80, height=80, border_radius=16,
                    bgcolor="#EDF2F7",
                    alignment=ft.alignment.Alignment(0, 0),
                ),
                ft.Container(width=20),
                ft.Column([
                    ft.Text(proyecto.get("nombre", "Proyecto"), size=19, weight=ft.FontWeight.BOLD, color="#2D3748"),
                    ft.Container(height=6),
                    ft.Row([
                        ft.Icon(ft.Icons.FOLDER_OUTLINED, size=16, color="#A0AEC0"),
                        ft.Container(width=6),
                        ft.Text(ruta, size=14, color="#718096", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ], spacing=0),
                ], spacing=0, expand=True),

                # Botones de acción
                ft.Row([
                    # ⭐ Favorito
                    ft.Container(
                        ref=fav_container_ref,
                        content=ft.Icon(
                            ft.Icons.STAR_ROUNDED if es_favorito else ft.Icons.STAR_OUTLINE_ROUNDED,
                            size=22,
                            color="#F59E0B" if es_favorito else "#CBD5E0",
                        ),
                        width=40, height=40, border_radius=10,
                        bgcolor="#FFFBEB" if es_favorito else "#F7FAFC",
                        alignment=ft.alignment.Alignment(0, 0),
                        on_click=lambda e, p=proyecto: toggle_fav(e, p),
                        tooltip="Favorito",
                        ink=True,
                    ),
                    ft.Container(width=10),
                    ft.Container(
                        content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=20, color="#F59E0B"),
                        width=40, height=40, border_radius=10, bgcolor="#FFFBEB",
                        alignment=ft.alignment.Alignment(0, 0),
                        on_click=lambda _, p=proyecto: self._editar_nombre_proyecto(p),
                        tooltip="Editar Nombre", ink=True,
                    ),
                    ft.Container(width=10),
                    ft.Container(
                        content=ft.Icon(ft.Icons.FOLDER_OPEN_ROUNDED, size=20, color="#48BB78"),
                        width=40, height=40, border_radius=10, bgcolor="#F0FFF4",
                        alignment=ft.alignment.Alignment(0, 0),
                        on_click=lambda _, p=proyecto: self._open_folder(p),
                        tooltip="Abrir Carpeta", ink=True,
                    ),
                    ft.Container(width=10),
                    ft.Container(
                        content=ft.Icon(ft.Icons.DOWNLOAD_ROUNDED, size=20, color="#06B6D4"),
                        width=40, height=40, border_radius=10, bgcolor="#ECFEFF",
                        alignment=ft.alignment.Alignment(0, 0),
                        on_click=lambda _, p=proyecto: self._export_project(p),
                        tooltip="Exportar", ink=True,
                    ),
                    ft.Container(width=10),
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=20, color="#F56565"),
                        width=40, height=40, border_radius=10, bgcolor="#FFF5F5",
                        alignment=ft.alignment.Alignment(0, 0),
                        on_click=lambda _, p=proyecto: self._delete_project(p),
                        tooltip="Eliminar", ink=True,
                    ),
                ], spacing=0),
            ]),
            padding=ft.Padding.all(24),
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1.5 if es_favorito else 1, "#F59E0B" if es_favorito else "#E2E8F0"),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            on_click=lambda _, p=proyecto: self.on_open_project(p),
            ink=False,
        )

        # Guardar metadata para búsqueda
        card._proyecto_ruta   = ruta
        card._proyecto_nombre = proyecto.get("nombre", "")
        card._proyecto_tipo   = tipo

        return card
    
    def _reordenar_con_animacion(self):
        """Reordena la lista de proyectos poniendo favoritos primero"""
        if not hasattr(self, '_proyectos_column'):
            return

        # Reordenar: favoritos primero, luego alfabético
        proyectos_ordenados = sorted(
            self.proyectos,
            key=lambda p: (0 if p.get("ruta") in self._favoritos else 1, p.get("nombre", ""))
        )

        # Reconstruir y actualizar
        self._proyectos_column.controls = [self._create_project_card(p) for p in proyectos_ordenados]
        self._proyectos_column.update()

    def _open_folder(self, proyecto):
        """Abre la carpeta del proyecto"""
        from cli_integration import abrir_carpeta_proyecto
        exito = abrir_carpeta_proyecto(proyecto["ruta"])
        if exito:
            self._show_success_snackbar("✓ Carpeta abierta")
        else:
            self._show_error_snackbar("❌ Error al abrir la carpeta")
    
    def _export_project(self, proyecto):
        """Exporta el proyecto"""
        try:
            import subprocess
            result = subprocess.run(
                ['zenity', '--file-selection', '--directory', '--title=Seleccionar carpeta de destino'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                ruta_destino = result.stdout.strip()
                
                # Exportar proyecto
                from cli_integration import exportar_proyecto_ui
                archivo_zip = exportar_proyecto_ui(proyecto["ruta"], ruta_destino)
                
                if archivo_zip:
                    from pathlib import Path
                    self._show_success_snackbar(f"✓ Proyecto exportado: {Path(archivo_zip).name}")
                else:
                    self._show_error_snackbar("❌ Error al exportar")
        except:
            self._show_error_snackbar("❌ Error al seleccionar carpeta")
    
    def _delete_project(self, proyecto):
        """Elimina el proyecto con confirmación"""
        def confirmar_eliminacion():
            dialog.open = False
            self.page.update()
            
            # Eliminar proyecto
            from cli_integration import eliminar_proyecto_ui, cargar_lista_proyectos
            exito = eliminar_proyecto_ui(proyecto["ruta"])
            
            if exito:
                self._show_success_snackbar("✓ Proyecto eliminado")
                # Recargar lista de proyectos
                import time
                time.sleep(0.5)
                self.proyectos = cargar_lista_proyectos()
                # Reconstruir la vista
                self.page.controls.clear()
                self.page.add(self.build())
                self.page.update()
            else:
                self._show_error_snackbar("❌ Error al eliminar")
        
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    # Icono grande y moderno
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE_FOREVER_ROUNDED, size=56, color="#FFFFFF"),
                        width=100,
                        height=100,
                        border_radius=50,
                        bgcolor="#F56565",
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                    
                    ft.Container(height=24),
                    
                    # Título
                    ft.Text(
                        "Eliminar Proyecto",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=12),
                    
                    # Descripción
                    ft.Text(
                        "¿Estás seguro de eliminar este proyecto?",
                        size=15,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=8),
                    
                    ft.Text(
                        "Esta acción eliminará permanentemente todas las versiones guardadas.",
                        size=14,
                        color="#A0AEC0",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=24),
                    
                    # Card con info del proyecto
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.FOLDER_ROUNDED, size=20, color="#F56565"),
                                width=44,
                                height=44,
                                border_radius=10,
                                bgcolor="#FEF2F2",
                                alignment=ft.alignment.Alignment(0, 0),
                            ),
                            ft.Container(width=12),
                            ft.Column([
                                ft.Text(
                                    proyecto.get('nombre', ''),
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    color="#1A202C",
                                ),
                                ft.Container(height=2),
                                ft.Text(
                                    f"{len(proyecto.get('versiones', []))} versión{'es' if len(proyecto.get('versiones', [])) != 1 else ''}",
                                    size=13,
                                    color="#718096",
                                ),
                            ], spacing=0, expand=True),
                        ]),
                        padding=ft.Padding.all(16),
                        border_radius=12,
                        bgcolor="#F7FAFC",
                        border=ft.Border.all(1, "#E5E7EB"),
                    ),
                    
                    ft.Container(height=28),
                    
                    # Botones modernos
                    ft.Row([
                        # Botón Cancelar
                        ft.Container(
                            content=ft.TextButton(
                                content=ft.Container(
                                    content=ft.Text("Cancelar", size=15, weight=ft.FontWeight.W_600, color="#718096"),
                                    padding=ft.Padding.symmetric(vertical=14, horizontal=0),
                                    alignment=ft.alignment.Alignment(0, 0),
                                ),
                                on_click=lambda _: self._close_dialog(dialog),
                            ),
                            expand=1,
                            border_radius=12,
                            bgcolor="#F7FAFC",
                            border=ft.Border.all(1.5, "#E5E7EB"),
                        ),
                        
                        ft.Container(width=12),
                        
                        # Botón Eliminar
                        ft.Container(
                            content=ft.ElevatedButton(
                                content=ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=20, color="#FFFFFF"),
                                        ft.Container(width=8),
                                        ft.Text("Eliminar", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    padding=ft.Padding.symmetric(vertical=14, horizontal=0),
                                ),
                                on_click=lambda _: confirmar_eliminacion(),
                                style=ft.ButtonStyle(
                                    bgcolor="#F56565",
                                    elevation=0,
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                ),
                            ),
                            expand=2,
                        ),
                    ]),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding.all(32),
                width=500,
                border_radius=20,
                bgcolor="#FFFFFF",
            ),
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
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
    
    def _show_info_snackbar(self, mensaje):
        """Muestra un snackbar informativo"""
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor="#667EEA",
            duration=2000,  # 2 segundos
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()
    
    def _editar_nombre_proyecto(self, proyecto):
        """Edita el nombre del proyecto"""
        nombre_field = ft.TextField(
            value=proyecto.get("nombre", ""),
            hint_text="Nombre del proyecto",
            border_radius=10,
            border_color="#E2E8F0",
            focused_border_color="#667EEA",
            text_size=15,
            autofocus=True,
        )
        
        def guardar_nombre():
            nuevo_nombre = nombre_field.value.strip()
            if not nuevo_nombre:
                self._show_error_snackbar("❌ El nombre no puede estar vacío")
                return
            
            dialog.open = False
            self.page.update()
            
            # Actualizar nombre
            from cli_integration import actualizar_nombre_proyecto, cargar_lista_proyectos
            exito = actualizar_nombre_proyecto(proyecto["ruta"], nuevo_nombre)
            
            if exito:
                self._show_success_snackbar("✓ Nombre actualizado")
                # Recargar lista de proyectos
                import time
                time.sleep(0.3)
                self.proyectos = cargar_lista_proyectos()
                # Reconstruir la vista
                self.page.controls.clear()
                self.page.add(self.build())
                self.page.update()
            else:
                self._show_error_snackbar("❌ Error al actualizar nombre")
        
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    # Icono
                    ft.Container(
                        content=ft.Icon(ft.Icons.EDIT_ROUNDED, size=48, color="#FFFFFF"),
                        width=80,
                        height=80,
                        border_radius=40,
                        bgcolor="#F59E0B",
                        alignment=ft.alignment.Alignment(0, 0),
                    ),
                    
                    ft.Container(height=20),
                    
                    ft.Text(
                        "Editar nombre del proyecto",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#1A202C",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=8),
                    
                    ft.Text(
                        "Nombre del proyecto",
                        size=13,
                        color="#718096",
                        text_align=ft.TextAlign.LEFT,
                    ),
                    
                    ft.Container(height=8),
                    
                    nombre_field,
                    
                    ft.Container(height=24),
                    
                    # Botones
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
                                on_click=lambda _: guardar_nombre(),
                                style=ft.ButtonStyle(
                                    bgcolor="#F59E0B",
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
    
    def _limpiar_proyectos_deprecados(self):
        """Limpia proyectos que ya no existen y busca nuevos proyectos en el sistema"""
        from cli_integration import cargar_lista_proyectos, guardar_lista_proyectos, obtener_proyectos_existentes
        from pathlib import Path
        
        proyectos_actuales = cargar_lista_proyectos()
        proyectos_validos = []
        proyectos_eliminados = 0
        
        # Paso 1: Limpiar proyectos deprecados
        for proyecto in proyectos_actuales:
            ruta = Path(proyecto["ruta"])
            carpeta_cronux = ruta / ".cronux"
            
            # Verificar si el proyecto existe
            if carpeta_cronux.exists():
                proyectos_validos.append(proyecto)
            else:
                proyectos_eliminados += 1
        
        # Paso 2: Buscar nuevos proyectos en el sistema
        rutas_actuales = {p["ruta"] for p in proyectos_validos}
        proyectos_encontrados = obtener_proyectos_existentes()
        proyectos_nuevos = 0
        
        for proyecto in proyectos_encontrados:
            if proyecto["ruta"] not in rutas_actuales:
                proyectos_validos.append(proyecto)
                proyectos_nuevos += 1
        
        # Guardar lista actualizada
        guardar_lista_proyectos(proyectos_validos)
        self.proyectos = proyectos_validos
        
        # Reconstruir la vista
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
        
        # Mostrar mensaje según lo que pasó
        if proyectos_eliminados > 0 and proyectos_nuevos > 0:
            self._show_success_snackbar(f"✓ {proyectos_eliminados} eliminado{'s' if proyectos_eliminados != 1 else ''}, {proyectos_nuevos} nuevo{'s' if proyectos_nuevos != 1 else ''} agregado{'s' if proyectos_nuevos != 1 else ''}")
        elif proyectos_eliminados > 0:
            self._show_success_snackbar(f"✓ {proyectos_eliminados} proyecto{'s' if proyectos_eliminados != 1 else ''} eliminado{'s' if proyectos_eliminados != 1 else ''}")
        elif proyectos_nuevos > 0:
            self._show_success_snackbar(f"✓ {proyectos_nuevos} proyecto{'s' if proyectos_nuevos != 1 else ''} nuevo{'s' if proyectos_nuevos != 1 else ''} encontrado{'s' if proyectos_nuevos != 1 else ''}")
        else:
            self._show_success_snackbar("✓ Lista actualizada, sin cambios")
    
    def _sincronizar_proyectos(self):
        """Sincroniza proyectos entre CLI y UI escaneando el sistema"""
        from cli_integration import sincronizar_proyectos
        
        # Mostrar mensaje de carga
        self._show_info_snackbar("🔄 Escaneando sistema...")
        
        # Sincronizar en segundo plano
        import threading
        def sync_thread():
            proyectos_sincronizados = sincronizar_proyectos()
            
            # Actualizar UI en el hilo principal
            self.proyectos = proyectos_sincronizados
            self.page.controls.clear()
            self.page.add(self.build())
            self.page.update()
            
            # Mostrar resultado
            self._show_success_snackbar(f"✓ Sincronizado: {len(proyectos_sincronizados)} proyectos")
        
        threading.Thread(target=sync_thread, daemon=True).start()
    
    def _auto_limpiar_proyectos_deprecados(self):
        """Limpia automáticamente proyectos deprecados al cargar (sin mostrar mensaje)"""
        from cli_integration import guardar_lista_proyectos
        from pathlib import Path
        
        if not self.proyectos:
            return
        
        proyectos_validos = []
        proyectos_eliminados = 0
        
        for proyecto in self.proyectos:
            ruta = Path(proyecto["ruta"])
            carpeta_cronux = ruta / ".cronux"
            
            if carpeta_cronux.exists():
                proyectos_validos.append(proyecto)
            else:
                proyectos_eliminados += 1
                print(f"[AUTO-CLEAN] Proyecto deprecado eliminado: {proyecto.get('nombre', 'Sin nombre')}")
        
        if proyectos_eliminados > 0:
            guardar_lista_proyectos(proyectos_validos)
            self.proyectos = proyectos_validos
    
    def _buscar_proyectos_nuevos_silencioso(self):
        """Busca nuevos proyectos en el sistema y los agrega automáticamente sin notificar"""
        from cli_integration import obtener_proyectos_existentes, guardar_lista_proyectos
        
        # Obtener rutas de proyectos actuales
        rutas_actuales = {p["ruta"] for p in self.proyectos}
        
        # Buscar proyectos en el sistema
        proyectos_encontrados = obtener_proyectos_existentes()
        
        # Agregar proyectos nuevos
        proyectos_nuevos = 0
        for proyecto in proyectos_encontrados:
            if proyecto["ruta"] not in rutas_actuales:
                self.proyectos.append(proyecto)
                proyectos_nuevos += 1
                print(f"[AUTO-DISCOVER] Nuevo proyecto encontrado: {proyecto.get('nombre', 'Sin nombre')} ({proyecto['ruta']})")
        
        if proyectos_nuevos > 0:
            # Guardar lista actualizada
            guardar_lista_proyectos(self.proyectos)
            print(f"[AUTO-DISCOVER] {proyectos_nuevos} proyecto{'s' if proyectos_nuevos != 1 else ''} nuevo{'s' if proyectos_nuevos != 1 else ''} agregado{'s' if proyectos_nuevos != 1 else ''} automáticamente")
    
    def _abrir_proyecto_existente(self):
        """Abre un proyecto existente desde el sistema de archivos"""
        try:
            import subprocess
            result = subprocess.run(
                ['zenity', '--file-selection', '--directory', '--title=Seleccionar carpeta del proyecto'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                ruta_proyecto = result.stdout.strip()
                
                # Verificar que sea un proyecto Cronux
                from pathlib import Path
                carpeta_cronux = Path(ruta_proyecto) / ".cronux"
                
                if not carpeta_cronux.exists():
                    self._show_error_snackbar("❌ No es un proyecto Cronux válido")
                    return
                
                # Agregar a la lista
                from cli_integration import agregar_proyecto_a_lista, cargar_lista_proyectos
                proyecto_info = agregar_proyecto_a_lista(ruta_proyecto)
                
                if proyecto_info:
                    self._show_success_snackbar("✓ Proyecto agregado")
                    # Recargar lista de proyectos
                    import time
                    time.sleep(0.3)
                    self.proyectos = cargar_lista_proyectos()
                    # Reconstruir la vista
                    self.page.controls.clear()
                    self.page.add(self.build())
                    self.page.update()
                else:
                    self._show_success_snackbar("✓ Proyecto ya existe en la lista")
        except:
            self._show_error_snackbar("❌ Error al seleccionar carpeta")
