# src/SonarCTL/widgets/console_widget.py
from PySide6.QtCore import Qt, QMetaObject, Q_ARG
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class ConsoleWidget(QWidget):
    MAX_LINES = 200

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.init_ui()
        self.logger.new_message.connect(self.update_console)
        self.load_previous_messages()

    def init_ui(self):
        layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def load_previous_messages(self):
        for message in self.logger.get_messages():
            self.update_console(message)

    def update_console(self, message):
        message_str = str(message)  # Convert the message to a string
        QMetaObject.invokeMethod(self.text_edit, "insertPlainText", Qt.QueuedConnection, Q_ARG(str, message_str + '\n'))
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
        self.trim_lines()

    def trim_lines(self):
        text = self.text_edit.toPlainText()
        lines = text.split('\n')
        if len(lines) > self.MAX_LINES:
            trimmed_text = '\n'.join(lines[-self.MAX_LINES:])
            self.text_edit.setPlainText(trimmed_text)
            self.text_edit.moveCursor(QTextCursor.MoveOperation.End)