import sys

import qdarktheme
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.SonarCTL.main_window import MainWindow

icon_dark_path = "assets/SonarCTL_dark.png"
icon_light_path = "assets/SonarCTL_light.png"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    # Set an application icon (optional)
    app.setWindowIcon(QIcon(icon_dark_path))

    window = MainWindow(icon_dark_path)
    window.show()

    sys.exit(app.exec())
