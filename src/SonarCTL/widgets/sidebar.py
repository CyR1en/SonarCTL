# src/SonarCTL/widgets/sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtCore import Qt, QSize, QUrl

from src.SonarCTL.widgets.console_window import ConsoleWindow


# src/SonarCTL/widgets/sidebar.py
class Sidebar(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("background-color: #202020;")  # Change to desired color
        self.setFixedWidth(40)  # Set fixed width for the sidebar
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)

        # Top buttons
        button1 = QPushButton()
        button1.setIcon(QIcon("assets/icon/setting.png"))
        button1.setIconSize(QSize(24, 24))  # Set icon size
        button1.setFixedSize(32, 32)  # Set fixed size to make it square
        button1.setStyleSheet("background: transparent; border: none;")  # Make button transparent
        button1.clicked.connect(self.on_button1_clicked)  # Connect listener
        layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        button2 = QPushButton()
        button2.setIcon(QIcon("assets/icon/terminal.png"))
        button2.setIconSize(QSize(20, 20))  # Set icon size
        button2.setFixedSize(32, 32)  # Set fixed size to make it square
        button2.setStyleSheet("background: transparent; border: none;")  # Make button transparent
        button2.clicked.connect(self.on_button2_clicked)  # Connect listener
        layout.addWidget(button2, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Spacer to push the logo to the bottom
        layout.addStretch()

        # Bottom logo
        source = QPushButton()
        source.setIcon(QIcon("assets/icon/github.png"))
        source.setIconSize(QSize(24, 24))  # Set icon size
        source.setFixedSize(32, 32)  # Set fixed size to make it square
        source.setStyleSheet("background: transparent; border: none;")  # Make button transparent
        source.clicked.connect(self.on_source_clicked)
        layout.addWidget(source, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def on_button2_clicked(self):
        console_window = ConsoleWindow(self.main_window.logger)
        console_window.setParent(self.main_window, Qt.WindowType.Window)
        console_window.show()

    @staticmethod
    def on_button1_clicked():
        print("Button 1 clicked")

    @staticmethod
    def on_source_clicked():
        QDesktopServices.openUrl(QUrl("https://github.com/CyR1en/SonarCtl"))
