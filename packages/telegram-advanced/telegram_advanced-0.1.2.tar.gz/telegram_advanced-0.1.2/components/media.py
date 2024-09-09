# components/media.py
class MediaHandler:
    def __init__(self, client):
        self.client = client

    def send_photo(self, chat_id, photo, caption=None, **kwargs):
        return self.client._make_request("sendPhoto", {
            "chat_id": chat_id,
            "photo": photo,
            "caption": caption,
            **kwargs
        })

    def send_video(self, chat_id, video, caption=None, **kwargs):
        return self.client._make_request("sendVideo", {
            "chat_id": chat_id,
            "video": video,
            "caption": caption,
            **kwargs
        })

    def send_document(self, chat_id, document, caption=None, **kwargs):
        return self.client._make_request("sendDocument", {
            "chat_id": chat_id,
            "document": document,
            "caption": caption,
            **kwargs
        })