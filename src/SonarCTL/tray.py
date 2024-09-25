# tray.py
import darkdetect
import pystray
from PIL import Image
import threading
from pystray import Icon

from src.SonarCTL import icon_dark_path, icon_light_path
from src.SonarCTL.sonar import midi_monitor, logger  # Ensure logger is imported from sonar.py
from src.SonarCTL.console_window import open_console


def on_quit(_icon):
    _icon.stop()


def setup(_icon):
    icon_path = icon_dark_path if darkdetect.isDark() else icon_light_path
    icon.icon = load_png_icon(icon_path)
    icon.title = "SonarCTL"  # Set the tooltip
    icon.menu = pystray.Menu(
        pystray.MenuItem('Console View', lambda: open_console(logger)),  # Pass the logger instance
        pystray.MenuItem('Quit', on_quit)
    )
    _icon.visible = True
    threading.Thread(target=midi_monitor, daemon=True).start()
    threading.Thread(target=darkdetect.listener, args=(change_icon,), daemon=True).start()


def load_png_icon(png_path, size=(64, 64)):
    image = Image.open(png_path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    return image


def change_icon(msg):
    global icon
    print(msg)
    _icon_path = icon_dark_path if msg == "Dark" else icon_light_path
    icon.icon = load_png_icon(_icon_path)


# Create the system tray icon
icon = Icon("SonarCTL")

icon.run(setup)
