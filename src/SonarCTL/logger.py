from PySide6.QtCore import QObject, Signal


class Logger(QObject):
    new_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.messages = []

    def log(self, message):
        self.messages.append(message)
        self.new_message.emit(message)

    def get_messages(self):
        return self.messages
