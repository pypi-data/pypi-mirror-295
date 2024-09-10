# features/reactions.py

from ..exceptions import TelegramBotError

class ReactionHandler:
    def __init__(self, client):
        self.client = client

    async def set_message_reaction(self, chat_id, message_id, reaction, is_big=False):
        """
        Set a reaction on a message.
        
        :param chat_id: Unique identifier for the target chat
        :param message_id: Identifier of the message to react to
        :param reaction: Reaction to set (emoji or custom emoji identifier)
        :param is_big: If True, the reaction is displayed in a larger size
        """
        try:
            return await self.client._make_request("setMessageReaction", {
                "chat_id": chat_id,
                "message_id": message_id,
                "reaction": reaction,
                "is_big": is_big
            })
        except Exception as e:
            raise TelegramBotError(f"Failed to set message reaction: {str(e)}")

    async def get_message_reaction_count(self, chat_id, message_id):
        """
        Get the count of reactions on a message.
        
        :param chat_id: Unique identifier for the target chat
        :param message_id: Identifier of the message
        """
        try:
            return await self.client._make_request("getMessageReactionCount", {
                "chat_id": chat_id,
                "message_id": message_id
            })
        except Exception as e:
            raise TelegramBotError(f"Failed to get message reaction count: {str(e)}")

    async def get_message_reaction_list(self, chat_id, message_id):
        """
        Get the list of users who reacted to a message.
        
        :param chat_id: Unique identifier for the target chat
        :param message_id: Identifier of the message
        """
        try:
            return await self.client._make_request("getMessageReactionList", {
                "chat_id": chat_id,
                "message_id": message_id
            })
        except Exception as e:
            raise TelegramBotError(f"Failed to get message reaction list: {str(e)}")

    async def handle_message_reaction(self, reaction_update):
        """
        Handle a message reaction update.
        
        :param reaction_update: The reaction update received from Telegram
        """
        try:
            chat_id = reaction_update['chat_id']
            message_id = reaction_update['message_id']
            user_id = reaction_update['user_id']
            reaction = reaction_update['reaction']

            # Here you can implement your logic to respond to reactions
            # For example, you might want to log the reaction, update a database, or send a response

            print(f"User {user_id} reacted with {reaction} to message {message_id} in chat {chat_id}")

            # You might want to trigger some action based on the reaction
            if reaction == '👍':
                await self.client.send_message(chat_id, f"Thanks for the thumbs up, user {user_id}!")
            elif reaction == '❤️':
                await self.client.send_message(chat_id, f"We're glad you loved the message, user {user_id}!")

        except Exception as e:
            raise TelegramBotError(f"Failed to handle message reaction: {str(e)}")

    async def handle_message_reaction_count(self, reaction_count_update):
        """
        Handle a message reaction count update.
        
        :param reaction_count_update: The reaction count update received from Telegram
        """
        try:
            chat_id = reaction_count_update['chat_id']
            message_id = reaction_count_update['message_id']
            reaction_counts = reaction_count_update['reaction_counts']

            # Here you can implement your logic to respond to reaction count changes
            # For example, you might want to update a database or trigger an action when a certain count is reached

            print(f"Reaction counts updated for message {message_id} in chat {chat_id}: {reaction_counts}")

            # You might want to trigger some action based on the reaction count
            total_reactions = sum(count for reaction, count in reaction_counts.items())
            if total_reactions > 10:
                await self.client.send_message(chat_id, f"Wow! Message {message_id} is getting a lot of reactions!")

        except Exception as e:
            raise TelegramBotError(f"Failed to handle message reaction count: {str(e)}")