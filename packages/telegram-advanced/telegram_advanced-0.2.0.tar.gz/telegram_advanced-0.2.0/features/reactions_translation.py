# features/reactions_translation.py
class ReactionsTranslationHandler:
    def __init__(self, client):
        self.client = client

    async def set_message_reaction(self, chat_id, message_id, reaction, **kwargs):
        return await self.client._make_request("setMessageReaction", {
            "chat_id": chat_id,
            "message_id": message_id,
            "reaction": reaction,
            **kwargs
        })

    async def get_message_reactions(self, chat_id, message_id, **kwargs):
        return await self.client._make_request("getMessageReactions", {
            "chat_id": chat_id,
            "message_id": message_id,
            **kwargs
        })

    async def translate_text(self, text, target_language_code):
        return await self.client._make_request("translateText", {
            "text": text,
            "target_language_code": target_language_code
        })

