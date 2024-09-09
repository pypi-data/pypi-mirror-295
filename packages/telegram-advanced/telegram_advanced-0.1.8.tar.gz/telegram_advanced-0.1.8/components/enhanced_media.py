# components/enhanced_media.py
class EnhancedMediaHandler:
    def __init__(self, client):
        self.client = client

    async def send_media_group(self, chat_id, media):
        return await self.client._make_request("sendMediaGroup", {
            "chat_id": chat_id,
            "media": media
        })

    async def edit_message_media(self, chat_id, message_id, media, **kwargs):
        return await self.client._make_request("editMessageMedia", {
            "chat_id": chat_id,
            "message_id": message_id,
            "media": media,
            **kwargs
        })

    async def send_animation(self, chat_id, animation, **kwargs):
        return await self.client._make_request("sendAnimation", {
            "chat_id": chat_id,
            "animation": animation,
            **kwargs
        })

    async def send_voice(self, chat_id, voice, **kwargs):
        return await self.client._make_request("sendVoice", {
            "chat_id": chat_id,
            "voice": voice,
            **kwargs
        })

    async def send_video_note(self, chat_id, video_note, **kwargs):
        return await self.client._make_request("sendVideoNote", {
            "chat_id": chat_id,
            "video_note": video_note,
            **kwargs
        })

