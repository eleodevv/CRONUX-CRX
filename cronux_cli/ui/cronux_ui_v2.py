#!/usr/bin/env python3
"""
Cronux UI v2 - Diseño minimalista con colores claros
Estilo: Clean, espacioso, profesional
"""

import flet as ft
from pathlib import Path
import sys
import threading

# Agregar el directorio cli al path
sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
sys.path.insert(0, str(Path(__file__).parent))

from screens.home_screen import HomeScreen
from screens.wizard_screen import WizardScreen
from cli_integration import crear_proyecto_ui, leer_info_proyecto, cargar_lista_proyectos, guardar_lista_proyectos


class CronuxUIv2:
    """Aplicación principal con diseño limpio"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "CRONUX - Control de Versiones Elegante"
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.min_width = 1000
        self.page.window.min_height = 700
        self.page.padding = 0
        self.page.bgcolor = "#FAFAFA"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Configurar icono de la ventana
        try:
            icon_path = Path(__file__).parent.parent / "assets" / "cronux_icon.icns"
            if icon_path.exists():
                self.page.window.icon = str(icon_path)
            else:
                # Fallback a PNG si no existe ICNS
                icon_png = Path(__file__).parent.parent / "assets" / "cronux_icon.png"
                if icon_png.exists():
                    self.page.window.icon = str(icon_png)
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
        
        # Pantalla actual
        self.current_screen = None
        
        # Cargar proyectos
        print("Cargando proyectos...")
        self.proyectos = cargar_lista_proyectos()
        print(f"Proyectos cargados: {len(self.proyectos)}")
        
        # Mostrar pantalla de inicio
        self.show_home()
    
    def show_home(self):
        """Muestra la pantalla de inicio"""
        # Recargar lista de proyectos cada vez que se muestra el home
        print("[HOME] Recargando lista de proyectos...")
        self.proyectos = cargar_lista_proyectos()
        print(f"[HOME] Proyectos cargados: {len(self.proyectos)}")
        
        self.current_screen = HomeScreen(
            page=self.page,
            on_new_project=self.show_wizard,
            on_open_project=self.show_project,
            proyectos=self.proyectos,
        )
        
        self.page.controls.clear()
        self.page.add(self.current_screen.build())
        self.page.update()
    
    def show_wizard(self):
        """Muestra el wizard"""
        wizard = WizardScreen(
            page=self.page,
            on_close=self.show_home,
            on_create=self._create_project,
        )
        
        self.page.controls.clear()
        self.page.add(wizard.build())
        self.page.update()
    
    def show_project(self, proyecto):
        """Muestra la vista de un proyecto"""
        from screens.project_screen_v2 import ProjectScreenV2
        
        project_screen = ProjectScreenV2(
            page=self.page,
            proyecto=proyecto,
            on_back=self.show_home,
            on_refresh=self._refresh_project,
        )
        
        self.page.controls.clear()
        self.page.add(project_screen.build())
        self.page.update()
    
    def _refresh_project(self, ruta_proyecto):
        """Refresca la información de un proyecto"""
        # Buscar el proyecto en la lista
        for i, p in enumerate(self.proyectos):
            if p["ruta"] == ruta_proyecto:
                # Leer información actualizada (el icono se genera automáticamente)
                proyecto_actualizado = leer_info_proyecto(ruta_proyecto)
                if proyecto_actualizado:
                    self.proyectos[i] = proyecto_actualizado
                    
                    # Guardar lista actualizada
                    guardar_lista_proyectos(self.proyectos)
                    
                    return proyecto_actualizado
        return None

    def _create_project(self, nombre, ruta, tipo, create_initial_version=True):
        """Crea un nuevo proyecto con loader de progreso en tiempo real"""
        from components.terminal_loader import TerminalLoaderView
        
        # Crear loader tipo terminal
        terminal_loader = TerminalLoaderView(self.page, "Creando proyecto")
        
        # Crear dialog
        progress_dialog = ft.AlertDialog(
            modal=True,
            content=terminal_loader.build(),
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor="#F7FAFC",
        )
        
        self.page.overlay.append(progress_dialog)
        progress_dialog.open = True
        self.page.update()
        
        # Callback para actualizar progreso en tiempo real
        def actualizar_progreso(mensaje):
            """Callback que recibe mensajes de progreso de las funciones CLI"""
            print(f"[PROGRESS] {mensaje}")
            
            # Agregar mensaje a la terminal
            terminal_loader.add_message(mensaje)
            terminal_loader.update_display()
        
        # Función async para crear el proyecto
        async def crear_proyecto_async():
            import asyncio
            
            try:
                # Pequeña pausa inicial
                await asyncio.sleep(0.2)
                
                # Crear proyecto con callback de progreso
                proyecto_info = crear_proyecto_ui(nombre, ruta, tipo, actualizar_progreso)
                
                # Marcar como completado
                terminal_loader.set_completed(success=bool(proyecto_info))
                
                # Pequeña pausa para ver el resultado
                await asyncio.sleep(1.5)
                
                # Cerrar dialog
                progress_dialog.open = False
                self.page.update()
                
                if proyecto_info:
                    # Recargar lista desde archivo (ya fue guardado por crear_proyecto_ui)
                    self.proyectos = cargar_lista_proyectos()
                    
                    # Abrir directamente el proyecto creado
                    self.show_project(proyecto_info)
                else:
                    # Error
                    self._show_error_snackbar("Error al crear el proyecto")
            
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                print(f"Error en creación: {error_detail}")
                terminal_loader.set_completed(success=False)
                terminal_loader.add_message(f"❌ Error: {str(e)}")
                terminal_loader.update_display()
                await asyncio.sleep(2)
                progress_dialog.open = False
                self.page.update()
                self._show_error_snackbar(f"Error: {str(e)}")
        
        # Ejecutar con run_task
        self.page.run_task(crear_proyecto_async)
    
    def _show_error_snackbar(self, mensaje):
        """Muestra un snackbar de error"""
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor="#F56565",
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()


def main(page: ft.Page):
    """Punto de entrada"""
    # Configurar assets
    script_dir = Path(__file__).parent
    page.assets_dir = str(script_dir / "assets")
    
    # IMPORTANTE: Configurar para que los updates sean inmediatos
    page.auto_scroll = False
    
    CronuxUIv2(page)
 

if __name__ == "__main__":
    ft.run(main)