# src/SonarCTL/widgets/sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtCore import Qt, QSize, QUrl

class Sidebar(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("background-color: #202020;")
        self.setFixedWidth(40)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)

        button1 = self.create_button("assets/icon/setting.png", 24, 32, self.main_window.switch_to_config_widget)
        layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        button2 = self.create_button("assets/icon/terminal.png", 20, 32, self.main_window.switch_to_console_widget)
        layout.addWidget(button2, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        button3 = self.create_button("assets/icon/mixer.png", 24, 32, self.main_window.switch_to_slider_widget)
        layout.addWidget(button3, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch()

        source = self.create_button("assets/icon/github.png", 24, 32, self.on_source_clicked)
        layout.addWidget(source, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    @staticmethod
    def create_button(icon_path, icon_size, button_size, click_handler):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(icon_size, icon_size))
        button.setFixedSize(button_size, button_size)
        button.setStyleSheet("background: transparent; border: none;")
        button.clicked.connect(click_handler)
        return button

    @staticmethod
    def on_source_clicked():
        QDesktopServices.openUrl(QUrl("https://github.com/CyR1en/SonarCtl"))