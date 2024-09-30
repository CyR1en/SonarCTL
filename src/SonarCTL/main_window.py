# src/SonarCTL/main_window.py
import os
import sys
import threading

from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication, QHBoxLayout, QVBoxLayout, QWidget, \
    QStackedWidget, QLabel
from PySide6.QtGui import QIcon, QAction

from src.SonarCTL.logger import Logger
from src.SonarCTL.sonar import SonarMidiListener
from src.SonarCTL.widgets.console_widget import ConsoleWidget
from src.SonarCTL.widgets.sidebar import Sidebar
from src.SonarCTL.widgets.config import ConfigWidget
from src.SonarCTL.widgets.sliders import SliderWidget
from src.SonarCTL.widgets.status_bar import StatusBar  # Import StatusDot


class MainWindow(QMainWindow):
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 300

    def __init__(self, icon_path):
        super().__init__()
        self.logger = Logger()

        self.setWindowTitle("SonarCTL")
        screen_width = QApplication.primaryScreen().size().width()
        screen_height = QApplication.primaryScreen().size().height()

        x = ((screen_width - self.WINDOW_WIDTH) // 2) - (self.WINDOW_WIDTH // 2)
        y = ((screen_height - self.WINDOW_HEIGHT) // 2)

        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.move(x, y)

        # Create the main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Add the sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        # Create a vertical layout for the active widget
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Create a stacked widget for central content
        self.central_stack = QStackedWidget()
        self.slider_widget = SliderWidget()
        self.status_bar = StatusBar()  # Create StatusBar instance
        self.config_widget = ConfigWidget(self)
        self.console_widget = ConsoleWidget(self.logger)  # Create ConsoleWidget instance
        self.central_stack.addWidget(self.config_widget)
        self.central_stack.addWidget(self.slider_widget)
        self.central_stack.addWidget(self.console_widget)  # Add ConsoleWidget to stack
        right_layout.addWidget(self.central_stack)

        # Create a horizontal layout for the status bar to stick to the right
        status_layout = QHBoxLayout()
        status_layout.addStretch()  # Add stretch to push the status bar to the right
        status_layout.addWidget(self.status_bar)
        right_layout.addLayout(status_layout)

        # Set stretch factors: 1 for central stack and 0 for status layout
        right_layout.setStretch(0, 1)
        right_layout.setStretch(1, 0)

        # Add the vertical layout to the main layout
        main_layout.addLayout(right_layout)

        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        if not QIcon(icon_path).isNull():
            self.tray_icon.setIcon(QIcon(icon_path))
            self.tray_icon.setToolTip("SonarCTL")
        else:
            print(f"Error: Icon not found at {icon_path}")

        tray_menu = QMenu()
        open_action = QAction("Open", self)
        quit_action = QAction("Quit", self)
        self.launch_on_startup_action = QAction("Launch on startup", self)
        self.launch_on_startup_action.setCheckable(True)
        self.launch_on_startup_action.setChecked(False)
        self.launch_on_startup_action.triggered.connect(self.toggle_launch_on_startup)

        open_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit_app)

        tray_menu.addAction(open_action)
        tray_menu.addAction(quit_action)
        tray_menu.addAction(self.launch_on_startup_action)

        self.tray_icon.setContextMenu(tray_menu)

        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.show()
        else:
            print("Error: System tray not available")

        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.sonar_midi_listener = SonarMidiListener(
            core_props_path=self.config_widget.path_field.text(),
            status_callback=self.status_bar.set_connected,  # Pass the status callback
            channel_mappings=self.config_widget.get_channel_mappings(),
            logger=self.logger,
            toggle_buttons=self.config_widget.toggle_buttons,
            slider_widget=self.slider_widget
        )
        threading.Thread(target=self.sonar_midi_listener.midi_monitor, daemon=True).start()

    def toggle_launch_on_startup(self):
        if self.launch_on_startup_action.isChecked():
            self.enable_launch_on_startup()
        else:
            self.disable_launch_on_startup()

    @staticmethod
    def enable_launch_on_startup():
        # Platform-specific code to enable launch on startup
        if os.name == 'nt':  # Windows
            import winreg as reg
            key = reg.HKEY_CURRENT_USER
            key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'
            with reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS) as key:
                reg.SetValueEx(key, "SonarCTL", 0, reg.REG_SZ, sys.executable)

    @staticmethod
    def disable_launch_on_startup():
        # Platform-specific code to disable launch on startup
        if os.name == 'nt':  # Windows
            import winreg as reg
            key = reg.HKEY_CURRENT_USER
            key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'
            with reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS) as key:
                reg.DeleteValue(key, "SonarCTL")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def show_window(self):
        self.show()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.instance().quit()

    def switch_to_slider_widget(self):
        if self.central_stack.currentWidget() != self.slider_widget:
            self.central_stack.setCurrentWidget(self.slider_widget)

    def switch_to_config_widget(self):
        if self.central_stack.currentWidget() != self.config_widget:
            self.central_stack.setCurrentWidget(self.config_widget)

    def switch_to_console_widget(self):
        if self.central_stack.currentWidget() != self.console_widget:
            self.central_stack.setCurrentWidget(self.console_widget)
