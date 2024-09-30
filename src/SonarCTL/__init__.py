import os
import sys
import ctypes
import qdarktheme
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from src.SonarCTL.main_window import MainWindow
from src.SonarCTL.utils import base_path

try:
    from ctypes import windll
    myappid = 'com.cyr1en.sonarctl'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

icon_dark_path = os.path.join(base_path, "assets/SonarCTL_dark.png")
icon_light_path = os.path.join(base_path, "assets/SonarCTL_light.png")

def is_already_running():
    mutex_name = "SonarCTL_Mutex"
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    return last_error == 183  # ERROR_ALREADY_EXISTS

if __name__ == "__main__":
    if is_already_running():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText("SonarCTL is already running.")
        msg_box.setWindowTitle("Warning")
        msg_box.exec()
        sys.exit(0)

    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    # Set an application icon (optional)
    app.setWindowIcon(QIcon(icon_dark_path))

    window = MainWindow(icon_dark_path)
    window.show()

    sys.exit(app.exec())