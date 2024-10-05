from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor

class StatusDot(QWidget):
    def __init__(self):
        super().__init__()
        self.connected = False
        self.setFixedSize(15, 15)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_connected(self, connected):
        self.connected = connected
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        color = QColor("#02ddbc") if self.connected else QColor("#b94247")
        painter.setBrush(color)
        painter.drawEllipse(0, 0, self.width(), self.height())

class StatusBar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.status_label = QLabel("SonarCTL MIDI Not Connected")
        self.status_label.setStyleSheet("color: #616978;")
        self.status_dot = StatusDot()
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_dot)
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.setFixedHeight(30)  # Set the fixed height to make the status bar thinner


    def set_connected(self, connected):
        self.status_dot.set_connected(connected)
        if connected:
            self.status_label.setText("SonarCTL MIDI Connected")
            self.layout.setContentsMargins(0, 0, 0, 10)
        else:
            self.status_label.setText("SonarCTL MIDI Not Connected")
            self.layout.setContentsMargins(0, 0, 10, 10)
        self.update()  # Ensure the UI is updated