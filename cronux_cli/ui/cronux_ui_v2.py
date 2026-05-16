#!/usr/bin/env python3
"""
Cronux UI v2 - Diseño minimalista con colores claros
"""

import flet as ft
from pathlib import Path
import sys
import os


def _setup_paths():
    """Configura los paths para encontrar módulos tanto en dev como en build de Flet"""
    # En flet build, el código se ejecuta desde un directorio temporal
    # __file__ puede no estar disponible, usamos sys.executable como referencia
    
    try:
        base = Path(__file__).parent
    except Exception:
        base = Path(sys.executable).parent

    # Posibles ubicaciones de los módulos CLI
    candidatos_cli = [
        base / "cli",                    # ui/cli/ (copiado por el workflow)
        base.parent / "cli",             # cronux_cli/cli/
        Path(sys.executable).parent / "cli",
        Path(os.getcwd()) / "cli",
    ]

    for ruta in candidatos_cli:
        if ruta.exists() and str(ruta) not in sys.path:
            sys.path.insert(0, str(ruta))
            print(f"[PATH] CLI path: {ruta}")
            break

    # Path del directorio ui (para screens, components, cli_integration)
    candidatos_ui = [
        base,
        Path(sys.executable).parent,
        Path(os.getcwd()),
    ]

    for ruta in candidatos_ui:
        if ruta.exists() and str(ruta) not in sys.path:
            sys.path.insert(0, str(ruta))
            print(f"[PATH] UI path: {ruta}")
            break


def main(page: ft.Page):
    """Punto de entrada principal"""
    
    # 1. Configurar paths PRIMERO
    _setup_paths()

    # 2. Configurar página básica inmediatamente para que no se vea negro
    page.title = "CRONUX - Control de Versiones"
    page.bgcolor = "#FAFAFA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.auto_scroll = False

    # Mostrar loading mientras carga
    page.add(
        ft.Container(
            content=ft.Column([
                ft.ProgressRing(color="#667EEA"),
                ft.Container(height=16),
                ft.Text("Cargando CRONUX...", color="#667EEA", size=16),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center,
            bgcolor="#FAFAFA",
        )
    )
    page.update()

    # 3. Importar módulos (después de configurar paths)
    try:
        from screens.home_screen import HomeScreen
        from screens.wizard_screen import WizardScreen
        from cli_integration import (
            crear_proyecto_ui, leer_info_proyecto,
            cargar_lista_proyectos, guardar_lista_proyectos
        )
        print("[OK] Módulos importados correctamente")
    except Exception as e:
        import traceback
        print(f"[ERROR] Fallo importando módulos: {e}")
        traceback.print_exc()
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color="#F56565"),
                    ft.Container(height=16),
                    ft.Text("Error al iniciar CRONUX", size=20, weight=ft.FontWeight.BOLD, color="#2D3748"),
                    ft.Container(height=8),
                    ft.Text(str(e), size=13, color="#718096", text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                alignment=ft.alignment.center,
                bgcolor="#FAFAFA",
                padding=40,
            )
        )
        page.update()
        return

    # 4. Configurar ventana completa
    try:
        page.window.width = 1200
        page.window.height = 800
        page.window.min_width = 1000
        page.window.min_height = 700
    except Exception as e:
        print(f"[WARN] No se pudo configurar ventana: {e}")

    # 5. Configurar icono según plataforma
    try:
        import platform
        sistema = platform.system()
        base = Path(__file__).parent

        if sistema == "Windows":
            candidatos = [
                base / "assets" / "cronux_icon.ico",
                base.parent / "assets" / "cronux_icon.ico",
            ]
        elif sistema == "Darwin":
            candidatos = [
                base / "assets" / "cronux_icon.icns",
                base.parent / "assets" / "cronux_icon.icns",
            ]
        else:
            candidatos = [
                base / "assets" / "cronux_icon.png",
                base.parent / "assets" / "cronux_icon.png",
            ]

        for icon_path in candidatos:
            if icon_path.exists():
                page.window.icon = str(icon_path)
                print(f"[ICON] {icon_path}")
                break
    except Exception as e:
        print(f"[WARN] Icono no cargado: {e}")

    # 6. Iniciar la app
    app = CronuxApp(page, cargar_lista_proyectos, crear_proyecto_ui,
                    leer_info_proyecto, guardar_lista_proyectos,
                    HomeScreen, WizardScreen)
    app.start()


class CronuxApp:
    def __init__(self, page, cargar_lista_proyectos, crear_proyecto_ui,
                 leer_info_proyecto, guardar_lista_proyectos,
                 HomeScreen, WizardScreen):
        self.page = page
        self._cargar_lista = cargar_lista_proyectos
        self._crear_proyecto = crear_proyecto_ui
        self._leer_info = leer_info_proyecto
        self._guardar_lista = guardar_lista_proyectos
        self._HomeScreen = HomeScreen
        self._WizardScreen = WizardScreen
        self.proyectos = []

    def start(self):
        self.proyectos = self._cargar_lista()
        self.show_home()

    def show_home(self):
        self.proyectos = self._cargar_lista()
        screen = self._HomeScreen(
            page=self.page,
            on_new_project=self.show_wizard,
            on_open_project=self.show_project,
            proyectos=self.proyectos,
        )
        self.page.controls.clear()
        self.page.add(screen.build())
        self.page.update()

    def show_wizard(self):
        wizard = self._WizardScreen(
            page=self.page,
            on_close=self.show_home,
            on_create=self._handle_create,
        )
        self.page.controls.clear()
        self.page.add(wizard.build())
        self.page.update()

    def show_project(self, proyecto):
        try:
            from screens.project_screen_v2 import ProjectScreenV2
            screen = ProjectScreenV2(
                page=self.page,
                proyecto=proyecto,
                on_back=self.show_home,
                on_refresh=self._refresh_project,
            )
            self.page.controls.clear()
            self.page.add(screen.build())
            self.page.update()
        except Exception as e:
            print(f"[ERROR] show_project: {e}")
            self._show_error(f"Error abriendo proyecto: {e}")

    def _refresh_project(self, ruta):
        for i, p in enumerate(self.proyectos):
            if p["ruta"] == ruta:
                updated = self._leer_info(ruta)
                if updated:
                    self.proyectos[i] = updated
                    self._guardar_lista(self.proyectos)
                    return updated
        return None

    def _handle_create(self, nombre, ruta, tipo, create_initial_version=True):
        from components.terminal_loader import TerminalLoaderView

        loader = TerminalLoaderView(self.page, "Creando proyecto")
        dialog = ft.AlertDialog(
            modal=True,
            content=loader.build(),
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor="#F7FAFC",
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

        def on_progress(msg):
            loader.add_message(msg)
            loader.update_display()

        async def run():
            import asyncio
            try:
                await asyncio.sleep(0.2)
                info = self._crear_proyecto(nombre, ruta, tipo, on_progress)
                loader.set_completed(success=bool(info))
                await asyncio.sleep(1.5)
                dialog.open = False
                self.page.update()
                if info:
                    self.proyectos = self._cargar_lista()
                    self.show_project(info)
                else:
                    self._show_error("Error al crear el proyecto")
            except Exception as e:
                import traceback
                traceback.print_exc()
                loader.set_completed(success=False)
                loader.add_message(f"❌ Error: {e}")
                loader.update_display()
                await asyncio.sleep(2)
                dialog.open = False
                self.page.update()
                self._show_error(str(e))

        self.page.run_task(run)

    def _show_error(self, msg):
        snack = ft.SnackBar(
            content=ft.Text(msg, color="#FFFFFF"),
            bgcolor="#F56565",
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()


if __name__ == "__main__":
    ft.app(main)
