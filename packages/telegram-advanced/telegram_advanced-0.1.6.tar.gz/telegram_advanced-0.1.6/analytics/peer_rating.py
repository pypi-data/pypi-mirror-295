# analytics/peer_rating.py
class PeerRatingHandler:
    def __init__(self, client):
        self.client = client

    def get_top_peers(self, category):
        return self.client._make_request("getTopPeers", {"category": category})

    def reset_top_peer_rating(self, category):
        return self.client._make_request("resetTopPeerRating", {"category": category})