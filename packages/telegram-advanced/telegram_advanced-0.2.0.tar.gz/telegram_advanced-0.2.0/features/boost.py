# features/boost.py
class BoostHandler:
    def __init__(self, client):
        self.client = client

    async def get_boost_status(self, peer):
        return await self.client._make_request("premium.getBoostsStatus", {
            "peer": peer
        })

    async def apply_boost(self, peer, slots=None):
        return await self.client._make_request("premium.applyBoost", {
            "peer": peer,
            "slots": slots
        })

    async def get_my_boosts(self):
        return await self.client._make_request("premium.getMyBoosts")
