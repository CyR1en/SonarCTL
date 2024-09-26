from PySide6.QtCore import Qt, QMetaObject, Q_ARG
from PySide6.QtGui import QTextCursor, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit


class ConsoleWindow(QMainWindow):
    def __init__(self, logger):
        super().__init__()
        self.setWindowTitle("Console View")
        self.setGeometry(100, 100, 800, 600)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)
        self.logger = logger
        self.logger.new_message.connect(self.update_console)
        self.load_previous_messages()

    def load_previous_messages(self):
        for message in self.logger.get_messages():
            self.update_console(message)

    def update_console(self, message):
        message_str = str(message)  # Convert the message to a string
        QMetaObject.invokeMethod(self.text_edit, "insertPlainText", Qt.QueuedConnection, Q_ARG(str, message_str + '\n'))
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
