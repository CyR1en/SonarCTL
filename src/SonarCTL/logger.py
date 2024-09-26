from PySide6.QtCore import QObject, Signal

class Logger(QObject):
    new_message = Signal(str)
    MAX_MESSAGES = 200

    def __init__(self):
        super().__init__()
        self.messages = []

    def log(self, message):
        self.messages.append(message)
        if len(self.messages) > self.MAX_MESSAGES:
            self.messages.pop(0)  # Remove the oldest message
        self.new_message.emit(message)

    def get_messages(self):
        return self.messages
