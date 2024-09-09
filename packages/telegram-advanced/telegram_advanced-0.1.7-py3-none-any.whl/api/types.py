
# telegram_advanced/api/types.py

from typing import List, Optional, Union, Dict, Any

class User:
    def __init__(self, id: int, is_bot: bool, first_name: str, **kwargs):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = kwargs.get('last_name')
        self.username = kwargs.get('username')
        self.language_code = kwargs.get('language_code')

class Chat:
    def __init__(self, id: int, type: str, **kwargs):
        self.id = id
        self.type = type
        self.title = kwargs.get('title')
        self.username = kwargs.get('username')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

class MessageEntity:
    def __init__(self, type: str, offset: int, length: int, **kwargs):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = kwargs.get('url')
        self.user = kwargs.get('user')
        self.language = kwargs.get('language')

class Message:
    def __init__(self, message_id: int, date: int, chat: Chat, **kwargs):
        self.message_id = message_id
        self.date = date
        self.chat = chat
        self.from_user = kwargs.get('from')
        self.text = kwargs.get('text')
        self.entities = [MessageEntity(**entity) for entity in kwargs.get('entities', [])]
        self.reply_markup = kwargs.get('reply_markup')
        # Add other fields as needed

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(
            message_id=data['message_id'],
            date=data['date'],
            chat=Chat(**data['chat']),
            **{k: v for k, v in data.items() if k not in ['message_id', 'date', 'chat']}
        )

class InlineKeyboardButton:
    def __init__(self, text: str, **kwargs):
        self.text = text
        self.url = kwargs.get('url')
        self.callback_data = kwargs.get('callback_data')
        self.switch_inline_query = kwargs.get('switch_inline_query')
        self.switch_inline_query_current_chat = kwargs.get('switch_inline_query_current_chat')
        # Add other fields as needed

    def to_dict(self) -> Dict[str, Any]:
        button_dict = {'text': self.text}
        if self.url:
            button_dict['url'] = self.url
        if self.callback_data:
            button_dict['callback_data'] = self.callback_data
        if self.switch_inline_query is not None:
            button_dict['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            button_dict['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        return button_dict

class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: List[List[InlineKeyboardButton]]):
        self.inline_keyboard = inline_keyboard

    def to_dict(self) -> Dict[str, List[List[Dict[str, Any]]]]:
        return {
            'inline_keyboard': [
                [button.to_dict() for button in row]
                for row in self.inline_keyboard
            ]
        }

    @classmethod
    def from_button_list(cls, buttons: List[List[Dict[str, Any]]]) -> 'InlineKeyboardMarkup':
        return cls([
            [InlineKeyboardButton(**button) for button in row]
            for row in buttons
        ])

# Add other necessary classes here (e.g., CallbackQuery, InlineQuery, etc.)
