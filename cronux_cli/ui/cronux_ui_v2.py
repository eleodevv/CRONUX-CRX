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
        """Crea un nuevo proyecto con loader Git-style timeline"""
        from components.loader import LoaderView
        
        # Definir pasos del timeline
        steps = [
            {"title": "Creando estructura", "subtitle": "Inicializando carpeta .cronux", "status": "active"},
            {"title": "Inicializando versión 1.0", "subtitle": "Preparando sistema de versiones", "status": "pending"},
            {"title": "Guardando archivos", "subtitle": "Copiando contenido del proyecto", "status": "pending"},
        ]
        
        # Crear loader con timeline
        loader = LoaderView(self.page, "Creando proyecto", steps)
        
        # Crear dialog
        dialog = ft.AlertDialog(
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
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
        
        # Función async para crear el proyecto
        async def crear_proyecto_async():
            import asyncio
            
            try:
                # Paso 1: Creando estructura
                await asyncio.sleep(0.5)
                steps[0]["status"] = "completed"
                steps[1]["status"] = "active"
                loader.update_steps(steps)
                
                if create_initial_version:
                    # Paso 2: Inicializando versión
                    await asyncio.sleep(0.5)
                    steps[1]["status"] = "completed"
                    steps[2]["status"] = "active"
                    loader.update_steps(steps)
                    
                    # Paso 3: Guardando archivos (operación real)
                    proyecto_info = await asyncio.to_thread(
                        crear_proyecto_ui, nombre, ruta, tipo, None
                    )
                    
                    await asyncio.sleep(0.5)
                    steps[2]["status"] = "completed"
                    loader.update_steps(steps)
                    
                    if proyecto_info:
                        # Recargar lista desde archivo (ya fue guardado por crear_proyecto_ui)
                        self.proyectos = cargar_lista_proyectos()
                        
                        # Pequeña pausa para ver el timeline completo
                        await asyncio.sleep(0.8)
                        
                        # Cerrar diálogo
                        dialog.open = False
                        self.page.update()
                        
                        # Abrir directamente el proyecto creado
                        self.show_project(proyecto_info)
                    else:
                        # Error
                        dialog.open = False
                        self.page.update()
                        self._show_error_snackbar("Error al crear el proyecto")
                else:
                    # Crear proyecto sin versión inicial (solo estructura)
                    import os
                    os.chdir(ruta)
                    
                    # Crear carpeta .cronux
                    carpeta_cronux = Path(ruta) / ".cronux"
                    carpeta_cronux.mkdir(exist_ok=True)
                    
                    # Crear datos del proyecto
                    import json
                    from datetime import datetime
                    
                    datos_proyecto = {
                        "nombre": nombre,
                        "tipo": tipo,
                        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "autor": "usuario"
                    }
                    
                    # Guardar JSON
                    archivo_proyecto = carpeta_cronux / "proyecto.json"
                    with open(archivo_proyecto, "w") as f:
                        json.dump(datos_proyecto, f, indent=2)
                    
                    # Crear carpeta de versiones vacía
                    carpeta_versiones = carpeta_cronux / "versiones"
                    carpeta_versiones.mkdir(exist_ok=True)
                    
                    steps[1]["status"] = "completed"
                    steps[2]["status"] = "completed"
                    loader.update_steps(steps)
                    
                    # Agregar a la lista
                    from cli_integration import obtener_icono_por_tipo
                    
                    proyecto = {
                        "nombre": nombre,
                        "ruta": ruta,
                        "tipo": tipo,
                        "icono": obtener_icono_por_tipo(tipo),
                        "versiones": [],
                        "tamaño_total": "0 B",
                        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    self.proyectos.append(proyecto)
                    
                    # Guardar lista de proyectos (deduplicando)
                    guardar_lista_proyectos(self.proyectos)
                    self.proyectos = cargar_lista_proyectos()
                    
                    # Pequeña pausa para ver el timeline completo
                    await asyncio.sleep(0.8)
                    
                    # Cerrar diálogo
                    dialog.open = False
                    self.page.update()
                    
                    # Abrir directamente el proyecto creado
                    self.show_project(proyecto)
                    
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                print(f"Error creando proyecto: {error_detail}")
                dialog.open = False
                self.page.update()
                self._show_error_snackbar(f"Error: {str(e)}")
        
        # Ejecutar con run_task para permitir actualizaciones de UI
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
    
    CronuxUIv2(page)
 

if __name__ == "__main__":
    ft.run(target=main)