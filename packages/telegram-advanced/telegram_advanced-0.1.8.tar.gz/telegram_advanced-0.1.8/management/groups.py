# management/groups.py
class GroupManager:
    def __init__(self, client):
        self.client = client

    def create_group(self, title, user_ids):
        return self.client._make_request("createChat", {
            "title": title,
            "user_ids": user_ids
        })

    def invite_user(self, chat_id, user_id):
        return self.client._make_request("inviteUser", {
            "chat_id": chat_id,
            "user_id": user_id
        })

    def kick_user(self, chat_id, user_id):
        return self.client._make_request("kickUser", {
            "chat_id": chat_id,
            "user_id": user_id
        })

    def set_admin_rights(self, chat_id, user_id, rights):
        return self.client._make_request("setAdminRights", {
            "chat_id": chat_id,
            "user_id": user_id,
            "rights": rights
        })