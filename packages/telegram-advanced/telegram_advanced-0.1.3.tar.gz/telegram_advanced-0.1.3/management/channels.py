# management/channels.py

class ChannelManager:
    def __init__(self, client):
        self.client = client

    async def create_channel(self, title, description):
        return await self.client._make_request("createChannel", {
            "title": title,
            "description": description
        })

    async def edit_channel(self, channel_id, **kwargs):
        return await self.client._make_request("editChannel", {
            "channel_id": channel_id,
            **kwargs
        })

    async def delete_channel(self, channel_id):
        return await self.client._make_request("deleteChannel", {
            "channel_id": channel_id
        })

    async def get_channel_members(self, channel_id, **kwargs):
        return await self.client._make_request("getChannelMembers", {
            "channel_id": channel_id,
            **kwargs
        })

    async def invite_to_channel(self, channel_id, user_id):
        return await self.client._make_request("inviteToChannel", {
            "channel_id": channel_id,
            "user_id": user_id
        })

    async def leave_channel(self, channel_id):
        return await self.client._make_request("leaveChannel", {
            "channel_id": channel_id
        })

    async def promote_channel_member(self, channel_id, user_id, **kwargs):
        return await self.client._make_request("promoteChatMember", {
            "chat_id": channel_id,
            "user_id": user_id,
            **kwargs
        })