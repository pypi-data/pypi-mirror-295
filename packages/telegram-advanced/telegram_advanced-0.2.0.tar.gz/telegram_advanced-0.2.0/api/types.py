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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            id=data['id'],
            is_bot=data['is_bot'],
            first_name=data['first_name'],
            last_name=data.get('last_name'),
            username=data.get('username'),
            language_code=data.get('language_code')
        )

class Chat:
    def __init__(self, id: int, type: str, **kwargs):
        self.id = id
        self.type = type
        self.title = kwargs.get('title')
        self.username = kwargs.get('username')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chat':
        return cls(
            id=data['id'],
            type=data['type'],
            title=data.get('title'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )

class MessageEntity:
    def __init__(self, type: str, offset: int, length: int, **kwargs):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = kwargs.get('url')
        self.user = kwargs.get('user')
        self.language = kwargs.get('language')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageEntity':
        return cls(
            type=data['type'],
            offset=data['offset'],
            length=data['length'],
            url=data.get('url'),
            user=data.get('user'),
            language=data.get('language')
        )

class Message:
    def __init__(self, message_id: int, date: int, chat: Chat, **kwargs):
        self.message_id = message_id
        self.date = date
        self.chat = chat
        self.from_user = kwargs.get('from_user')
        self.text = kwargs.get('text')
        self.entities = [MessageEntity.from_dict(entity) for entity in kwargs.get('entities', [])]
        self.reply_markup = kwargs.get('reply_markup')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(
            message_id=data['message_id'],
            date=data['date'],
            chat=Chat.from_dict(data['chat']),
            from_user=User.from_dict(data['from']) if 'from' in data else None,
            text=data.get('text'),
            entities=[MessageEntity.from_dict(entity) for entity in data.get('entities', [])],
            reply_markup=InlineKeyboardMarkup.from_button_list(data.get('reply_markup', {}).get('inline_keyboard', [])) if 'reply_markup' in data else None
        )

class InlineKeyboardButton:
    def __init__(self, text: str, **kwargs):
        self.text = text
        self.url = kwargs.get('url')
        self.callback_data = kwargs.get('callback_data')
        self.switch_inline_query = kwargs.get('switch_inline_query')
        self.switch_inline_query_current_chat = kwargs.get('switch_inline_query_current_chat')

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

class CallbackQuery:
    def __init__(self, id: str, from_user: User, message: Optional[Message] = None, **kwargs):
        self.id = id
        self.from_user = from_user
        self.message = message
        self.inline_message_id = kwargs.get('inline_message_id')
        self.chat_instance = kwargs.get('chat_instance')
        self.data = kwargs.get('data')
        self.game_short_name = kwargs.get('game_short_name')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CallbackQuery':
        return cls(
            id=data['id'],
            from_user=User.from_dict(data['from']),
            message=Message.from_dict(data['message']) if 'message' in data else None,
            inline_message_id=data.get('inline_message_id'),
            chat_instance=data.get('chat_instance'),
            data=data.get('data'),
            game_short_name=data.get('game_short_name')
        )

class InlineQuery:
    def __init__(self, id: str, from_user: User, query: str, **kwargs):
        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = kwargs.get('offset')
        self.chat_type = kwargs.get('chat_type')
        self.location = kwargs.get('location')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InlineQuery':
        return cls(
            id=data['id'],
            from_user=User.from_dict(data['from']),
            query=data['query'],
            offset=data.get('offset'),
            chat_type=data.get('chat_type'),
            location=data.get('location')
        )

class ChosenInlineResult:
    def __init__(self, result_id: str, from_user: User, query: str, **kwargs):
        self.result_id = result_id
        self.from_user = from_user
        self.query = query

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChosenInlineResult':
        return cls(
            result_id=data['result_id'],
            from_user=User.from_dict(data['from']),
            query=data['query']
        )

class ShippingQuery:
    def __init__(self, id: str, from_user: User, invoice_payload: str, shipping_address: Dict[str, Any]):
        self.id = id
        self.from_user = from_user
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ShippingQuery':
        return cls(
            id=data['id'],
            from_user=User.from_dict(data['from']),
            invoice_payload=data['invoice_payload'],
            shipping_address=data['shipping_address']
        )

class PreCheckoutQuery:
    def __init__(self, id: str, from_user: User, currency: str, total_amount: int, invoice_payload: str):
        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PreCheckoutQuery':
        return cls(
            id=data['id'],
            from_user=User.from_dict(data['from']),
            currency=data['currency'],
            total_amount=data['total_amount'],
            invoice_payload=data['invoice_payload']
        )

class Poll:
    def __init__(self, id: str, question: str, options: List[Dict[str, Any]], is_closed: bool):
        self.id = id
        self.question = question
        self.options = options
        self.is_closed = is_closed

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Poll':
        return cls(
            id=data['id'],
            question=data['question'],
            options=data['options'],
            is_closed=data['is_closed']
        )

class Update:
    def __init__(self, update_id: int, **kwargs):
        self.update_id = update_id
        self.message = Message.from_dict(kwargs['message']) if 'message' in kwargs else None
        self.edited_message = Message.from_dict(kwargs['edited_message']) if 'edited_message' in kwargs else None
        self.channel_post = Message.from_dict(kwargs['channel_post']) if 'channel_post' in kwargs else None
        self.edited_channel_post = Message.from_dict(kwargs['edited_channel_post']) if 'edited_channel_post' in kwargs else None
        self.inline_query = InlineQuery.from_dict(kwargs['inline_query']) if 'inline_query' in kwargs else None
        self.chosen_inline_result = ChosenInlineResult.from_dict(kwargs['chosen_inline_result']) if 'chosen_inline_result' in kwargs else None
        self.callback_query = CallbackQuery.from_dict(kwargs['callback_query']) if 'callback_query' in kwargs else None
        self.shipping_query = ShippingQuery.from_dict(kwargs['shipping_query']) if 'shipping_query' in kwargs else None
        self.pre_checkout_query = PreCheckoutQuery.from_dict(kwargs['pre_checkout_query']) if 'pre_checkout_query' in kwargs else None
        self.poll = Poll.from_dict(kwargs['poll']) if 'poll' in kwargs else None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Update':
        return cls(update_id=data['update_id'], **data)

class UpdateNewMessage(Update):
    def __init__(self, message: Message, pts: int, pts_count: int):
        super().__init__(update_id=0)
        self.message = message
        self.pts = pts
        self.pts_count = pts_count
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UpdateNewMessage':
        return cls(
            message=Message.from_dict(data['message']),
            pts=data['pts'],
            pts_count=data['pts_count']
        )

class UpdateDeleteMessages(Update):
    def __init__(self, messages: List[int], pts: int, pts_count: int):
        super().__init__(update_id=0)
        self.messages = messages
        self.pts = pts
        self.pts_count = pts_count
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UpdateDeleteMessages':
        return cls(
            messages=data['messages'],
            pts=data['pts'],
            pts_count=data['pts_count']
        )

class UpdateUserTyping(Update):
    def __init__(self, user_id: int, action: str):
        super().__init__(update_id=0)
        self.user_id = user_id
        self.action = action
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UpdateUserTyping':
        return cls(
            user_id=data['user_id'],
            action=data['action']
        )