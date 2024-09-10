# components/games.py
class GamesHandler:
    def __init__(self, client):
        self.client = client

    def send_game(self, chat_id, game_short_name, **kwargs):
        return self.client._make_request("sendGame", {
            "chat_id": chat_id,
            "game_short_name": game_short_name,
            **kwargs
        })

    def set_game_score(self, user_id, score, force=None, disable_edit_message=None, chat_id=None, message_id=None, inline_message_id=None):
        return self.client._make_request("setGameScore", {
            "user_id": user_id,
            "score": score,
            "force": force,
            "disable_edit_message": disable_edit_message,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id
        })