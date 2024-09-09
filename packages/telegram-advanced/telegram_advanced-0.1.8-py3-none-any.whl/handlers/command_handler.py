# handlers/command_handler.py
class CommandHandler:
    def __init__(self, client):
        self.client = client
        self.commands = {}

    def register_command(self, command, handler):
        self.commands[command] = handler

    def handle_command(self, message):
        command = message.text.split()[0][1:]
        if command in self.commands:
            self.commands[command](message)