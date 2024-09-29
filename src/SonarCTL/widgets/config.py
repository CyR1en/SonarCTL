# src/SonarCTL/widgets/config_widget.py
import os
import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFileDialog, QLineEdit
from PySide6.QtCore import Qt, QStandardPaths

class ConfigWidget(QWidget):
    DEFAULT_PATH = "C:\\ProgramData\\SteelSeries\\SteelSeries Engine 3\\coreProps.json"
    CONFIG_FILE = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation), "SonarCTL", "config.json")

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.load_config()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)

        self.setup_path_selector(main_layout)
        self.setup_channel_selectors(main_layout)

        self.setLayout(main_layout)

    def setup_path_selector(self, layout):
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
        layout.addLayout(path_layout)

        if os.path.exists(self.DEFAULT_PATH):
            self.path_field.setText(self.DEFAULT_PATH)
            self.path_button.hide()
        else:
            self.path_field.setText("Path to coreProps.json: Not Found")

    def setup_channel_selectors(self, layout):
        self.channels_layout = QVBoxLayout()
        self.channels = ["Game", "Chat", "Media", "Mic", "Chat Mix", "None"]
        self.channel_selectors = []
        self.toggle_buttons = []

        for i in range(1, 6):
            channel_layout = QHBoxLayout()
            channel_layout.setSpacing(5)
            channel_label = QLabel(f"MIDI Channel {i}")
            channel_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            channel_selector = QComboBox()
            channel_selector.addItems(self.channels)
            channel_selector.setCurrentText("None")
            channel_selector.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            channel_selector.currentIndexChanged.connect(self.update_channel_options)
            channel_selector.currentIndexChanged.connect(self.save_config)
            self.channel_selectors.append(channel_selector)

            toggle_button = QPushButton("M")
            toggle_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            toggle_button.setFixedSize(26, 26)
            toggle_button.setStyleSheet("margin-top: 0px; font-size: 11px;")
            toggle_button.clicked.connect(self.create_toggle_button_handler(toggle_button))
            self.toggle_buttons.append(toggle_button)

            channel_layout.addWidget(channel_label)
            channel_layout.addWidget(channel_selector)
            channel_layout.addWidget(toggle_button)
            self.channels_layout.addLayout(channel_layout)

        layout.addLayout(self.channels_layout)

    def create_toggle_button_handler(self, button):
        def toggle_button():
            if button.text() == "M":
                button.setText("S")
            else:
                button.setText("M")
            self.save_config()

        return toggle_button

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
            options = [option for option in self.channels if option not in selected_options or option == current_text]
            if "None" not in options:
                options.append("None")
            selector.addItems(options)
            selector.setCurrentText(current_text)
            selector.blockSignals(False)
        self.update_sonar_midi_listener_channels()
        self.update_slider_labels()

    def update_sonar_midi_listener_channels(self):
        if hasattr(self, 'sonar_midi_listener'):
            self.sonar_midi_listener.channel_mappings = {f"channel_{i + 1}": selector.currentText() for i, selector in enumerate(self.channel_selectors)}

    def update_slider_labels(self):
        labels = [selector.currentText() for selector in self.channel_selectors]
        self.main_window.slider_widget.update_slider_labels(labels)

    def save_config(self):
        config = {
            "channels": [selector.currentText() for selector in self.channel_selectors],
            "toggle_states": [button.text() for button in self.toggle_buttons]
        }
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f)

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                config = json.load(f)
                for selector, value in zip(self.channel_selectors, config.get("channels", [])):
                    selector.setCurrentText(value)
                for button, state in zip(self.toggle_buttons, config.get("toggle_states", [])):
                    button.setText(state)
            self.update_slider_labels()

    def get_channel_mappings(self):
        return {f"channel_{i + 1}": selector.currentText() for i, selector in enumerate(self.channel_selectors)}