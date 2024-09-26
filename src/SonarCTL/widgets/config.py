# src/SonarCTL/widgets/config_widget.py
import os
import json
import threading

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFileDialog, QLineEdit
from PySide6.QtCore import Qt, QStandardPaths
from PySide6.QtGui import QColor, QPainter
from src.SonarCTL.sonar import SonarMidiListener


class ConfigWidget(QWidget):
    DEFAULT_PATH = "C:\\ProgramData\\SteelSeries\\SteelSeries Engine 3\\coreProps.json"
    CONFIG_FILE = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation),
                               "SonarCTL", "config.json")

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.load_config()
        self.start_sonar_midi_listener()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)

        # Path selector
        path_layout = QVBoxLayout()
        self.path_label = QLabel("coreProps.json")
        self.path_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.path_field = QLineEdit()
        self.path_field.setReadOnly(True)
        self.path_field.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.path_button = QPushButton("Browse")
        self.path_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.path_button.clicked.connect(self.open_file_dialog)

        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_field)
        path_layout.addWidget(self.path_button)
        main_layout.addLayout(path_layout)

        # Check if the default path exists
        if os.path.exists(self.DEFAULT_PATH):
            self.path_field.setText(self.DEFAULT_PATH)
            self.path_button.hide()
        else:
            self.path_field.setText("Path to coreProps.json: Not Found")

        # Channel selectors
        self.channels_layout = QVBoxLayout()
        self.channels = ["Game", "Chat", "Media", "Mic", "Chat Mix", "None"]
        self.channel_selectors = []
        for i in range(1, 6):
            channel_layout = QHBoxLayout()
            channel_label = QLabel(f"MIDI Channel {i}")
            channel_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            channel_selector = QComboBox()
            channel_selector.addItems(self.channels)
            channel_selector.setCurrentText("None")  # Set default value to "None"
            channel_selector.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            channel_selector.currentIndexChanged.connect(self.update_channel_options)
            channel_selector.currentIndexChanged.connect(self.save_config)  # Save config on change
            self.channel_selectors.append(channel_selector)
            channel_layout.addWidget(channel_label)
            channel_layout.addWidget(channel_selector)
            self.channels_layout.addLayout(channel_layout)
        main_layout.addLayout(self.channels_layout)

        # Status dot and label
        status_layout = QHBoxLayout()
        status_layout.setSpacing(5)  # Adjust spacing to move the label closer to the dot
        status_layout.addStretch()
        self.status_label = QLabel("SonarCTL MIDI Not Connected")
        self.status_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.status_label.setStyleSheet("color: #696260;")  # Set label color to a little darker than white
        self.status_dot = StatusDot()
        self.status_dot.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.status_dot)
        main_layout.addLayout(status_layout)

        self.setLayout(main_layout)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        file_path, _ = file_dialog.getOpenFileName(self, "Select coreProps.json", "", "JSON Files (*.json)")
        if file_path:
            self.path_field.setText(file_path)
            self.path_button.hide()

    def update_channel_options(self):
        selected_options = [selector.currentText() for selector in self.channel_selectors]
        for selector in self.channel_selectors:
            current_text = selector.currentText()
            selector.blockSignals(True)
            selector.clear()
            selector.addItems(
                [option for option in self.channels if option not in selected_options or option == current_text])
            selector.setCurrentText(current_text)
            selector.blockSignals(False)
        self.update_sonar_midi_listener_channels()

    def update_sonar_midi_listener_channels(self):
        if hasattr(self, 'sonar_midi_listener'):
            self.sonar_midi_listener.channel_mappings = {f"channel_{i + 1}": selector.currentText() for i, selector in
                                                         enumerate(self.channel_selectors)}

    def save_config(self):
        config = {
            "channels": [selector.currentText() for selector in self.channel_selectors]
        }
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                config = json.load(f)
                for selector, value in zip(self.channel_selectors, config.get("channels", [])):
                    selector.setCurrentText(value)

    def set_status(self, connected):
        self.status_dot.set_connected(connected)
        if connected:
            self.status_label.setText("SonarCTL MIDI Connected")
        else:
            self.status_label.setText("SonarCTL MIDI Not Connected")

    def start_sonar_midi_listener(self):
        core_props_path = self.path_field.text()
        channel_mappings = {f"channel_{i + 1}": selector.currentText() for i, selector in
                            enumerate(self.channel_selectors)}
        self.sonar_midi_listener = SonarMidiListener(core_props_path, self.set_status, channel_mappings,
                                                     self.main_window.logger)
        threading.Thread(target=self.sonar_midi_listener.start, daemon=True).start()


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
