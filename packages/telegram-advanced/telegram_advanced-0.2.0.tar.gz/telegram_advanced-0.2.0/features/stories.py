# features/stories.py
class StoriesHandler:
    def __init__(self, client):
        self.client = client

    async def send_story(self, peer, media, **kwargs):
        return await self.client._make_request("stories.sendStory", {
            "peer": peer,
            "media": media,
            **kwargs
        })

    async def get_all_stories(self, **kwargs):
        return await self.client._make_request("stories.getAllStories", kwargs)

    async def get_pinned_stories(self, peer, **kwargs):
        return await self.client._make_request("stories.getPinnedStories", {
            "peer": peer,
            **kwargs
        })

    async def get_story_viewers(self, peer, story_id, **kwargs):
        return await self.client._make_request("stories.getStoryViewsList", {
            "peer": peer,
            "id": story_id,
            **kwargs
        })

    async def delete_stories(self, peer, story_ids):
        return await self.client._make_request("stories.deleteStories", {
            "peer": peer,
            "id": story_ids
        })