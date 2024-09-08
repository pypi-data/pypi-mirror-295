# api/client.py
import requests
import json
from ..exceptions import TelegramAPIError

class TelegramClient:
    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, token):
        self.token = token

    def _make_request(self, method, data=None, files=None):
        url = f"{self.BASE_URL}{self.token}/{method}"
        response = requests.post(url, data=data, files=files)
        if response.status_code != 200:
            raise TelegramAPIError(f"API request failed: {response.text}")
        return json.loads(response.text)

    def send_message(self, chat_id, text, **kwargs):
        data = {
            "chat_id": chat_id,
            "text": text,
            **kwargs
        }
        return self._make_request("sendMessage", data)

    def set_webhook(self, url):
        return self._make_request("setWebhook", {"url": url})

    def start_polling(self):
        offset = 0
        while True:
            updates = self._make_request("getUpdates", {"offset": offset, "timeout": 30})
            for update in updates["result"]:
                offset = update["update_id"] + 1
                self._process_update(update)

    def _process_update(self, update):
        # Implement update processing logic here
        pass