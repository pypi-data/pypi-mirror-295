# handlers/callback_handler.py
class CallbackHandler:
    def __init__(self, client):
        self.client = client
        self.callbacks = {}

    def register_callback(self, data_prefix, handler):
        self.callbacks[data_prefix] = handler

    def handle_callback(self, callback_query):
        for prefix, handler in self.callbacks.items():
            if callback_query.data.startswith(prefix):
                handler(callback_query)
                break