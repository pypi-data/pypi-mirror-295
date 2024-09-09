# features/threads.py

class ThreadHandler:
    def __init__(self, client):
        self.client = client

    async def create_forum_topic(self, chat_id, name, **kwargs):
        return await self.client._make_request("createForumTopic", {
            "chat_id": chat_id,
            "name": name,
            **kwargs
        })

    async def edit_forum_topic(self, chat_id, message_thread_id, **kwargs):
        return await self.client._make_request("editForumTopic", {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            **kwargs
        })

    async def close_forum_topic(self, chat_id, message_thread_id):
        return await self.client._make_request("closeForumTopic", {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id
        })

    async def reopen_forum_topic(self, chat_id, message_thread_id):
        return await self.client._make_request("reopenForumTopic", {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id
        })

    async def delete_forum_topic(self, chat_id, message_thread_id):
        return await self.client._make_request("deleteForumTopic", {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id
        })

    async def unpin_all_forum_topic_messages(self, chat_id, message_thread_id):
        return await self.client._make_request("unpinAllForumTopicMessages", {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id
        })