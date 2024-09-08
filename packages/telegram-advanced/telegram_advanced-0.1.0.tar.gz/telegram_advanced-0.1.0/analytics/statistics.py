# analytics/statistics.py
from collections import defaultdict
import time

class AnalyticsHandler:
    def __init__(self, client):
        self.client = client
        self.message_count = defaultdict(int)
        self.user_activity = defaultdict(lambda: defaultdict(int))
        self.command_usage = defaultdict(int)

    def log_message(self, chat_id, user_id):
        self.message_count[chat_id] += 1
        self.user_activity[chat_id][user_id] += 1

    def log_command(self, command):
        self.command_usage[command] += 1

    def get_chat_statistics(self, chat_id):
        return {
            "total_messages": self.message_count[chat_id],
            "active_users": len(self.user_activity[chat_id]),
            "top_users": sorted(self.user_activity[chat_id].items(), key=lambda x: x[1], reverse=True)[:5]
        }

    def get_command_statistics(self):
        return dict(self.command_usage)

    def get_channel_stats(self, channel_id):
        return self.client._make_request("getChannelStats", {"channel_id": channel_id})
