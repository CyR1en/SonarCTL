from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt


class SliderWidget(QWidget):
    slider_colors = ['rgba(2, 221, 183, 0.5)', 'rgba(45, 172, 239, 0.5)',
                     'rgba(110, 54, 159, 0.5)', 'rgba(139, 81, 244, 0.5)',
                     'rgba(250, 166, 48, 0.5)']

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()  # Use QVBoxLayout for top-to-bottom layout
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)  # Reduce spacing

        # Add the label at the top, aligned to the left
        title_label = QLabel("SonarCTL MIDI View")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.main_layout.addWidget(title_label)

        sliders_layout = QHBoxLayout()
        sliders_layout.setContentsMargins(10, 10, 10, 10)
        sliders_layout.setSpacing(10)  # Reduce spacing
        self.sliders = []

        for i, color in enumerate(self.slider_colors, start=1):
            slider_layout = QVBoxLayout()
            slider_layout.setContentsMargins(0, 0, 0, 0)
            slider_layout.setSpacing(5)

            slider = QSlider(Qt.Orientation.Vertical)
            slider.setRange(0, 100)
            slider.setValue(50)
            slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            slider.setEnabled(False)  # Disable user interaction

            slider.setStyleSheet(f"""
                QSlider::handle:vertical {{
                    background: rgba(255, 255, 255, 0.5); /* semi-transparent color */
                    height: 20px;
                    margin: 0 -5px; /* handle is placed by default on the contents rect of the groove */
                    border: 1px solid #000000; /* small dark line in the middle */
                }}
                QSlider::add-page:vertical {{
                    background: {color};
                }}
                QSlider::sub-page:vertical {{
                    background: {color};
                }}
            """)

            label = QLabel(f"C{i}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            slider_layout.addWidget(slider, alignment=Qt.AlignmentFlag.AlignHCenter)
            slider_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

            sliders_layout.addLayout(slider_layout)
            self.sliders.append((slider, label))

        self.main_layout.addLayout(sliders_layout)
        self.setLayout(self.main_layout)

    def update_slider_labels(self, labels):
        for (slider, label), new_label in zip(self.sliders, labels):
            label.setText(new_label)

    def update_slider_values(self, values):
        for (slider, _), value in zip(self.sliders, values):
            slider.setValue(value)

    def update_slider(self, index, value):
        if 0 <= index < len(self.sliders):
            slider, _ = self.sliders[index]
            slider.setValue(value)
