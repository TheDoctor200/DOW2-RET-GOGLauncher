import flet as ft
import os
import shutil
import subprocess
from pathlib import Path

class DOW2Launcher:
    def __init__(self):
        self.game_path = ""
        self.config_file = "launcher_config.txt"
        self.load_config()
        
    def load_config(self):
        """Load saved game path from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.game_path = f.read().strip()
        except:
            self.game_path = ""
    
    def save_config(self):
        """Save game path to config file"""
        try:
            with open(self.config_file, 'w') as f:
                f.write(self.game_path)
        except:
            pass
    
    def validate_game_path(self, path):
        """Validate if the path contains DOW2.exe"""
        if not path:
            return False
        dow2_exe = os.path.join(path, "DOW2.exe")
        return os.path.exists(dow2_exe)
    
    def inject_dlls(self, source_folder):
        """Inject DLLs from specified folder into game directory"""
        if not self.game_path or not self.validate_game_path(self.game_path):
            return False, "Invalid game path. Please set the correct DOW2 installation directory."
        
        try:
            # Get the DLL source paths
            current_dir = os.path.dirname(os.path.abspath(__file__))
            source_path = os.path.join(current_dir, source_folder)
            
            if not os.path.exists(source_path):
                return False, f"Source folder {source_folder} not found!"
            
            # Define which DLLs to inject - only Galaxy.dll is required
            dll_files = ["Galaxy.dll"]
            
            # First, delete existing DLLs in game directory
            for dll in dll_files:
                target_dll = os.path.join(self.game_path, dll)
                if os.path.exists(target_dll):
                    try:
                        os.remove(target_dll)
                    except Exception as e:
                        return False, f"Failed to delete existing {dll}: {str(e)}"
            
            # Copy new DLLs to game directory
            for dll in dll_files:
                source_dll = os.path.join(source_path, dll)
                target_dll = os.path.join(self.game_path, dll)
                
                if os.path.exists(source_dll):
                    shutil.copy2(source_dll, target_dll)
                else:
                    return False, f"DLL file {dll} not found in {source_folder}!"
            
            return True, f"Successfully injected DLLs from {source_folder}!"
            
        except Exception as e:
            return False, f"Error injecting DLLs: {str(e)}"
    
    def launch_game(self):
        """Launch the game"""
        if not self.game_path or not self.validate_game_path(self.game_path):
            return False, "Invalid game path. Please set the correct DOW2 installation directory."
        
        try:
            dow2_exe = os.path.join(self.game_path, "DOW2.exe")
            subprocess.Popen([dow2_exe], cwd=self.game_path)
            return True, "Game launched successfully!"
        except Exception as e:
            return False, f"Error launching game: {str(e)}"

def main(page: ft.Page):
    # INSTANT STARTUP: Set all window properties immediately for fastest loading
    page.title = "DOW2: Retribution - GOG Launcher"
    page.padding = 15
    page.spacing = 15
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1a1a"
    page.color_scheme_seed = "#8b0000"
    
    # INSTANT DESKTOP WINDOW PROPERTIES - Set immediately for instant loading
    try:
        # Modern Flet window properties (instant loading)
        page.window.width = 500
        page.window.height = 500
        page.window.resizable = False
        page.window.maximizable = False
        page.window.center()
        page.window.min_width = 500
        page.window.min_height = 500
        page.window.always_on_top = False
        page.window.skip_task_bar = False
        page.window.frameless = False
        page.window.full_screen = False
        page.window.visible = True
    except Exception:
        # Fallback for older Flet versions (instant loading)
        try:
            page.window_width = 500
            page.window_height = 500
            page.window_resizable = False
            page.window_maximizable = False
        except Exception:
            pass
    
    # INSTANT ICON SETUP - Optimized icon loading
    try:
        base_dir = Path(__file__).parent
        assets_dir = base_dir / "assets"
        
        # Try ICO first (Windows native, fastest)
        ico_icon = assets_dir / "icon_windows.ico"
        if ico_icon.exists():
            page.icon_path = str(ico_icon)
            try:
                page.window.icon = str(ico_icon)
            except Exception:
                pass
        else:
            # Fallback to PNG with ICO conversion
            png_icon = assets_dir / "favicon.png"
            if png_icon.exists():
                page.icon_path = str(png_icon)
                # Try to create ICO for better Windows performance
                try:
                    from PIL import Image
                    img = Image.open(png_icon)
                    sizes = [(16,16), (24,24), (32,32), (48,48), (64,64), (128,128), (256,256)]
                    img.save(ico_icon, sizes=sizes)
                    # Use the newly created ICO
                    page.icon_path = str(ico_icon)
                    try:
                        page.window.icon = str(ico_icon)
                    except Exception:
                        pass
                except Exception:
                    pass
    except Exception:
        pass
    
    # INSTANT WEB FAVICON
    try:
        page.favicon = "assets/favicon.png"
    except Exception:
        pass
    
    # INSTANT LAUNCHER INITIALIZATION
    launcher = DOW2Launcher()
    
    # INSTANT UI BUILDING - Create all UI elements at once for faster rendering
    # Game cover image
    game_cover = ft.Image(
        src="assets/dow2_retribution_final-1300181503.jpg",
        width=80,
        height=120,
        fit=ft.ImageFit.CONTAIN,
        border_radius=8
    )
    
    title = ft.Text(
        "DOW2: Retribution - GOG Launcher",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#ffd700",
        text_align=ft.TextAlign.CENTER
    )
    
    # Header row with image and title
    header_row = ft.Row(
        [game_cover, title],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    # Game path input
    path_input = ft.TextField(
        label="Game Installation Directory",
        hint_text="Enter the path where DOW2.exe is located...",
        value=launcher.game_path,
        border_color="#8b0000",
        focused_border_color="#ff0000",
        color="#ffffff",
        bgcolor="#1a1a1a",
        text_size=14,
        expand=True
    )
    
    def save_path(e):
        launcher.game_path = path_input.value
        launcher.save_config()
        status_text.value = "Game path saved successfully!"
        status_text.color = "#00ff00"
        page.update()
    
    save_button = ft.ElevatedButton(
        "Save Path",
        on_click=save_path,
        bgcolor="#8b0000",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )
    
    path_row = ft.Row(
        [path_input, save_button],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    
    # Action buttons
    def play_offline_skirmish(e):
        success, message = launcher.inject_dlls("GOGEmuDLL")
        if success:
            launcher.launch_game()
            status_text.value = message
            status_text.color = "#00ff00"
        else:
            status_text.value = message
            status_text.color = "#ff0000"
        page.update()
    
    def switch_to_gog(e):
        success, message = launcher.inject_dlls("OriginalGOGDLL")
        if success:
            launcher.launch_game()
            status_text.value = message
            status_text.color = "#00ff00"
        else:
            status_text.value = message
            status_text.color = "#ff0000"
        page.update()
    
    offline_button = ft.ElevatedButton(
        "Play Offline Skirmish",
        on_click=play_offline_skirmish,
        bgcolor="#006400",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        expand=True
    )
    
    gog_button = ft.ElevatedButton(
        "Switch to GOG Version",
        on_click=switch_to_gog,
        bgcolor="#000080",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        expand=True
    )
    
    button_row = ft.Row(
        [offline_button, gog_button],
        spacing=15
    )
    
    # Open ngalaxye_settings folder button
    def open_ngalaxye_settings(e):
        if not launcher.game_path or not launcher.validate_game_path(launcher.game_path):
            status_text.value = "Invalid game path. Please set the correct DOW2 installation directory."
            status_text.color = "#ff0000"
            page.update()
            return
        settings_folder = os.path.join(launcher.game_path, "ngalaxye_settings")
        if os.path.isdir(settings_folder):
            try:
                if os.name == "nt":
                    os.startfile(settings_folder)
                else:
                    try:
                        subprocess.Popen(["xdg-open", settings_folder])
                    except Exception:
                        subprocess.Popen(["open", settings_folder])
                status_text.value = "Opened ngalaxye_settings folder."
                status_text.color = "#00ff00"
            except Exception as ex:
                status_text.value = f"Failed to open folder: {str(ex)}"
                status_text.color = "#ff0000"
        else:
            status_text.value = "ngalaxye_settings folder not found in the game directory."
            status_text.color = "#ff0000"
        page.update()

    open_folder_button = ft.ElevatedButton(
        "Open ngalaxye_settings Folder",
        on_click=open_ngalaxye_settings,
        bgcolor="#444444",
        color="#ffffff",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )
    
    # Status display
    status_text = ft.Text(
        "Ready to launch DOW2: Retribution",
        size=14,
        color="#cccccc",
        text_align=ft.TextAlign.CENTER,
        ref=ft.Ref[ft.Text]()
    )
    
    # INSTANT LAYOUT - Add all elements at once for fastest rendering
    page.add(
        header_row,
        ft.Divider(color="#8b0000", thickness=2),
        path_row,
        button_row,
        open_folder_button,
        ft.Divider(color="#8b0000", thickness=1),
        status_text
    )
    
    # INSTANT PATH LOADING - Update UI immediately with saved path
    if launcher.game_path:
        path_input.value = launcher.game_path
        # Force immediate update for instant loading
        page.update()

if __name__ == "__main__":
    # OPTIMIZED APP LAUNCH - Use fastest view mode and assets
    ft.app(
        target=main, 
        view=ft.AppView.FLET_APP, 
        assets_dir="assets",
        # Additional startup optimizations
        upload_dir="temp_uploads"  # Faster file handling
    )
