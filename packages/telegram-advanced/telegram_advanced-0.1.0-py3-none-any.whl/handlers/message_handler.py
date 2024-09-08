# handlers/message_handler.py
from ..utils.logger import CustomLogger
from ..utils.error_handler import handle_error, APIError, ValidationError

logger = CustomLogger(__name__)

class MessageHandler:
    def __init__(self, client):
        self.client = client

    @handle_error
    async def handle_message(self, message):
        logger.info(f"Handling message from user {message['from']['id']}")
        # Implement message handling logic here

    @handle_error
    async def handle_edited_message(self, message):
        logger.info(f"Handling edited message from user {message['from']['id']}")
        # Implement edited message handling logic here

    @handle_error
    async def handle_channel_post(self, post):
        logger.info(f"Handling channel post in channel {post['chat']['id']}")
        # Implement channel post handling logic here

    @handle_error
    async def handle_edited_channel_post(self, post):
        logger.info(f"Handling edited channel post in channel {post['chat']['id']}")
        # Implement edited channel post handling logic here

    @handle_error
    async def send_message(self, chat_id, text, **kwargs):
        logger.info(f"Sending message to chat {chat_id}")
        try:
            return await self.client._make_request("sendMessage", {
                "chat_id": chat_id,
                "text": text,
                **kwargs
            })
        except APIError as e:
            logger.error(f"Failed to send message to chat {chat_id}: {str(e)}")
            raise
        except ValidationError as e:
            logger.warning(f"Validation error when sending message to chat {chat_id}: {str(e)}")
            raise

    @handle_error
    async def delete_message(self, chat_id, message_id):
        logger.info(f"Deleting message {message_id} from chat {chat_id}")
        try:
            return await self.client._make_request("deleteMessage", {
                "chat_id": chat_id,
                "message_id": message_id
            })
        except APIError as e:
            logger.error(f"Failed to delete message {message_id} from chat {chat_id}: {str(e)}")
            raise