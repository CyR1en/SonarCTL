import os
import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFileDialog, QLineEdit
from PySide6.QtCore import Qt, QStandardPaths

import os
import json
from PySide6.QtCore import QStandardPaths


class Configuration:
    CONFIG_FILE = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation),
                               "SonarCTL", "config.json")

    def __init__(self):
        self.config_data = {}
        self.load_raw_config()

    def save_config(self):
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f)

    def load_raw_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                self.config_data = json.load(f)

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set(self, key, value):
        self.config_data[key] = value
        self.save_config()


class ConfigWidget(QWidget):
    DEFAULT_PATH = "C:\\ProgramData\\SteelSeries\\SteelSeries Engine 3\\coreProps.json"

    def __init__(self, main_window, configuration):
        super().__init__()
        self.main_window = main_window
        self.configuration = configuration
        self.init_ui()
        self.load_values_to_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)

        self.setup_path_selector(main_layout)
        self.setup_channel_selectors(main_layout)

        self.setLayout(main_layout)

    def setup_path_selector(self, layout):
        path_layout = QVBoxLayout()
        path_layout.setSpacing(5)
        self.path_label = QLabel("coreProps.json")
        self.path_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.path_field = QLineEdit()
        self.path_field.setReadOnly(True)
        self.path_field.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.path_field.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.path_button = QPushButton("Browse")
        self.path_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.path_button.clicked.connect(self.open_file_dialog)

        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_field)
        path_layout.addWidget(self.path_button)
        layout.addLayout(path_layout)

        if os.path.exists(self.DEFAULT_PATH):
            self.path_field.setText(self.DEFAULT_PATH)
            self.path_field.setCursorPosition(0)
            self.path_button.hide()
        else:
            self.path_field.setText("Path to coreProps.json: Not Found")

    def setup_channel_selectors(self, layout):
        self.channels_layout = QVBoxLayout()
        self.channels = ["Game", "Chat", "Media", "Mic", "Chat Mix", "Master", "None"]
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
            channel_selector.setStyleSheet("QComboBox:focus { border: none; }")
            channel_selector.currentIndexChanged.connect(self.update_channel_options)
            channel_selector.currentIndexChanged.connect(self.save_config)
            self.channel_selectors.append(channel_selector)

            toggle_button = QPushButton("M")
            toggle_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            toggle_button.setFixedSize(26, 26)
            toggle_button.setStyleSheet("margin-top: 0px; font-size: 11px;")
            toggle_button.clicked.connect(self.create_toggle_button_handler(toggle_button))
            toggle_button.clicked.connect(self.save_config)
            self.toggle_buttons.append(toggle_button)

            channel_layout.addWidget(channel_label)
            channel_layout.addWidget(channel_selector)
            channel_layout.addWidget(toggle_button)
            self.channels_layout.addLayout(channel_layout)

        layout.addLayout(self.channels_layout)

    @staticmethod
    def create_toggle_button_handler(button):
        def toggle_button():
            if button.text() == "M":
                button.setText("S")
            else:
                button.setText("M")

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
        for i, selector in enumerate(self.channel_selectors):
            current_text = selector.currentText()
            selector.blockSignals(True)
            selector.clear()
            options = [option for option in self.channels if option not in selected_options or option == current_text]
            if "None" not in options:
                options.append("None")
            selector.addItems(options)
            selector.setCurrentText(current_text)
            selector.blockSignals(False)

            # Disable the toggle button if the selected option is "Chat Mix"
            if current_text == "Chat Mix":
                self.toggle_buttons[i].setEnabled(False)
            else:
                self.toggle_buttons[i].setEnabled(True)

        self.update_sonar_midi_listener_channels()
        self.update_slider_labels()

    def update_sonar_midi_listener_channels(self):
        if hasattr(self.main_window, 'sonar_midi_listener'):
            self.main_window.sonar_midi_listener.channel_mappings = {
                f"channel_{i + 1}": selector.currentText() for i, selector in enumerate(self.channel_selectors)
            }
            print(self.main_window.sonar_midi_listener.channel_mappings)

    def update_slider_labels(self):
        labels = [selector.currentText() for selector in self.channel_selectors]
        self.main_window.slider_widget.update_slider_labels(labels)

    def save_config(self):
        config = {
            "channels": [selector.currentText() for selector in self.channel_selectors],
            "toggle_states": [button.text() for button in self.toggle_buttons],
        }
        self.configuration.set("config_data", config)

    def load_values_to_ui(self):
        config = self.configuration.get("config_data", {})
        for button, state in zip(self.toggle_buttons, config.get("toggle_states", [])):
            button.setText(state)
        for selector, value in zip(self.channel_selectors, config.get("channels", [])):
            selector.setCurrentText(value)

    def get_channel_mappings(self):
        return {f"channel_{i + 1}": selector.currentText() for i, selector in enumerate(self.channel_selectors)}
