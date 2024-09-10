
# telegram_advanced/api/methods.py

from typing import Optional, List, Union, Dict, Any
from .types import Message, User, Chat, File, UserProfilePhotos, ChatMember, ChatInviteLink, BotCommand, MenuButton

class TelegramMethods:
    def __init__(self, api_client):
        self.api_client = api_client

    async def get_me(self) -> User:
        """Get information about the bot."""
        result = await self.api_client._make_request("getMe")
        return User(**result)

    async def send_message(self, chat_id: Union[int, str], text: str, **kwargs) -> Message:
        """Send a text message."""
        data = {
            "chat_id": chat_id,
            "text": text,
            **kwargs
        }
        result = await self.api_client._make_request("sendMessage", data)
        return Message.from_dict(result)

    async def forward_message(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_id: int, **kwargs) -> Message:
        """Forward a message."""
        data = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            **kwargs
        }
        result = await self.api_client._make_request("forwardMessage", data)
        return Message.from_dict(result)

    async def send_photo(self, chat_id: Union[int, str], photo: Union[str, bytes], **kwargs) -> Message:
        """Send a photo."""
        data = {
            "chat_id": chat_id,
            "photo": photo,
            **kwargs
        }
        result = await self.api_client._make_request("sendPhoto", data)
        return Message.from_dict(result)

    async def send_audio(self, chat_id: Union[int, str], audio: Union[str, bytes], **kwargs) -> Message:
        """Send an audio file."""
        data = {
            "chat_id": chat_id,
            "audio": audio,
            **kwargs
        }
        result = await self.api_client._make_request("sendAudio", data)
        return Message.from_dict(result)

    async def send_document(self, chat_id: Union[int, str], document: Union[str, bytes], **kwargs) -> Message:
        """Send a document."""
        data = {
            "chat_id": chat_id,
            "document": document,
            **kwargs
        }
        result = await self.api_client._make_request("sendDocument", data)
        return Message.from_dict(result)

    async def send_video(self, chat_id: Union[int, str], video: Union[str, bytes], **kwargs) -> Message:
        """Send a video."""
        data = {
            "chat_id": chat_id,
            "video": video,
            **kwargs
        }
        result = await self.api_client._make_request("sendVideo", data)
        return Message.from_dict(result)

    async def send_animation(self, chat_id: Union[int, str], animation: Union[str, bytes], **kwargs) -> Message:
        """Send an animation."""
        data = {
            "chat_id": chat_id,
            "animation": animation,
            **kwargs
        }
        result = await self.api_client._make_request("sendAnimation", data)
        return Message.from_dict(result)

    async def send_voice(self, chat_id: Union[int, str], voice: Union[str, bytes], **kwargs) -> Message:
        """Send a voice message."""
        data = {
            "chat_id": chat_id,
            "voice": voice,
            **kwargs
        }
        result = await self.api_client._make_request("sendVoice", data)
        return Message.from_dict(result)

    async def send_location(self, chat_id: Union[int, str], latitude: float, longitude: float, **kwargs) -> Message:
        """Send a location."""
        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            **kwargs
        }
        result = await self.api_client._make_request("sendLocation", data)
        return Message.from_dict(result)

    async def edit_message_text(self, text: str, **kwargs) -> Union[Message, bool]:
        """Edit the text of a message."""
        data = {
            "text": text,
            **kwargs
        }
        result = await self.api_client._make_request("editMessageText", data)
        return Message.from_dict(result) if isinstance(result, dict) else result

    async def delete_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        """Delete a message."""
        data = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        return await self.api_client._make_request("deleteMessage", data)

    async def answer_callback_query(self, callback_query_id: str, **kwargs) -> bool:
        """Answer a callback query."""
        data = {
            "callback_query_id": callback_query_id,
            **kwargs
        }
        return await self.api_client._make_request("answerCallbackQuery", data)

    async def get_chat(self, chat_id: Union[int, str]) -> Chat:
        """Get information about a chat."""
        data = {
            "chat_id": chat_id
        }
        result = await self.api_client._make_request("getChat", data)
        return Chat(**result)

    async def get_chat_administrators(self, chat_id: Union[int, str]) -> List[ChatMember]:
        """Get a list of administrators in a chat."""
        data = {
            "chat_id": chat_id
        }
        result = await self.api_client._make_request("getChatAdministrators", data)
        return [ChatMember(**member) for member in result]

    async def get_chat_member(self, chat_id: Union[int, str], user_id: int) -> ChatMember:
        """Get information about a member of a chat."""
        data = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        result = await self.api_client._make_request("getChatMember", data)
        return ChatMember(**result)

    # Add more methods as needed...
