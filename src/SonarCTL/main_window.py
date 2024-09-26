from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication, QHBoxLayout, QWidget

from src.SonarCTL.logger import Logger
from src.SonarCTL.widgets.sidebar import Sidebar
from src.SonarCTL.widgets.config import ConfigWidget


class MainWindow(QMainWindow):
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 300

    def __init__(self, icon_path):
        super().__init__()
        self.logger = Logger()

        self.setWindowTitle("SonarCTL")
        # calculate middle of screen
        screen_width = QApplication.primaryScreen().size().width()
        screen_height = QApplication.primaryScreen().size().height()

        x = ((screen_width - self.WINDOW_WIDTH) // 2) - (self.WINDOW_WIDTH // 2)
        y = ((screen_height - self.WINDOW_HEIGHT) // 2)

        # make it not resizable
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.move(x, y)

        # Create the main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to zero

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Add the sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        # Add the config widget to the right side
        self.config_widget = ConfigWidget(self)
        main_layout.addWidget(self.config_widget)

        # Set stretch factors: 1 for sidebar (10%) and 9 for config widget (90%)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 9)

        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        if not QIcon(icon_path).isNull():
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            print(f"Error: Icon not found at {icon_path}")

        # Create a menu for the system tray
        tray_menu = QMenu()
        open_action = QAction("Open", self)
        quit_action = QAction("Quit", self)

        open_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit_app)

        tray_menu.addAction(open_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # Show the tray icon
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.show()
        else:
            print("Error: System tray not available")

        # Connect the tray icon click to show the window
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def closeEvent(self, event):
        """ Override the close event to minimize the app to the system tray """
        event.ignore()
        self.hide()

    def show_window(self):
        """ Show the main window """
        self.show()
        self.activateWindow()  # Brings the window to the foreground

    def on_tray_icon_activated(self, reason):
        """ Handle the tray icon activation (e.g., when it's clicked) """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()

    def quit_app(self):
        """ Quit the application """
        self.tray_icon.hide()
        QApplication.instance().quit()
