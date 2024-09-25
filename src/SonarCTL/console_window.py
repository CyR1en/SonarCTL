import sys
import qdarktheme
import threading
from PySide6.QtCore import Qt, QMetaObject, Q_ARG
from PySide6.QtGui import QTextCursor, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit

from src.SonarCTL import icon_dark_path

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
        QMetaObject.invokeMethod(self.text_edit, "insertPlainText", Qt.QueuedConnection, Q_ARG(str, message + '\n'))
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)

def open_console(logger):
    def run_app():
        app = QApplication.instance()
        if app is None:
            qdarktheme.enable_hi_dpi()
            app = QApplication(sys.argv)
            qdarktheme.setup_theme("auto")
            app.setWindowIcon(QIcon(icon_dark_path))  # Set the application icon here
        console_window = ConsoleWindow(logger)
        console_window.show()
        app.exec_()

    threading.Thread(target=run_app, daemon=True).start()