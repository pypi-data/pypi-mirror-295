# api/client.py
import aiohttp
import asyncio
from ..exceptions import handle_telegram_error, NetworkError

class TelegramClient:
    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, token):
        self.token = token
        self.session = None

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _make_request(self, method, data=None, files=None):
        url = f"{self.BASE_URL}{self.token}/{method}"
        session = await self._get_session()
        
        try:
            if files:
                form_data = aiohttp.FormData()
                for key, value in data.items():
                    form_data.add_field(key, str(value))
                for key, file in files.items():
                    form_data.add_field(key, file, filename=file.name)
                response = await session.post(url, data=form_data)
            else:
                response = await session.post(url, json=data)
            
            response_json = await response.json()
            
            if not response_json.get('ok'):
                handle_telegram_error(response_json)
            
            return response_json['result']
        
        except aiohttp.ClientError as e:
            raise NetworkError(f"Network error occurred: {str(e)}")

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def send_message(self, chat_id, text, **kwargs):
        data = {
            "chat_id": chat_id,
            "text": text,
            **kwargs
        }
        return await self._make_request("sendMessage", data)

    async def set_webhook(self, url):
        return await self._make_request("setWebhook", {"url": url})

    async def get_updates(self, offset=None, limit=None, timeout=None, allowed_updates=None):
        return await self._make_request("getUpdates", {
            "offset": offset,
            "limit": limit,
            "timeout": timeout,
            "allowed_updates": allowed_updates
        })

    async def start_polling(self, process_update_func):
        offset = 0
        while True:
            try:
                updates = await self.get_updates(offset=offset, timeout=30)
                for update in updates:
                    offset = update["update_id"] + 1
                    await process_update_func(update)
            except Exception as e:
                print(f"Error in polling: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    # Add more methods as needed...