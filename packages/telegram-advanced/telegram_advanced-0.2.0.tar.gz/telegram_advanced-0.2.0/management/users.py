# management/users.py
class UserManager:
    def __init__(self, client):
        self.client = client

    def get_user_profile(self, user_id):
        return self.client._make_request("getUserProfilePhotos", {"user_id": user_id})

    def set_user_profile_photo(self, photo):
        return self.client._make_request("setUserProfilePhoto", {"photo": photo})

    def delete_user_profile_photo(self, photo_id):
        return self.client._make_request("deleteUserProfilePhoto", {"photo_id": photo_id})

    def get_user_status(self, user_id):
        return self.client._make_request("getUserStatus", {"user_id": user_id})

    def get_contacts(self):
        return self.client._make_request("getContacts")

    def add_contact(self, user_id, first_name, last_name=None, phone_number=None):
        return self.client._make_request("addContact", {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number
        })

    def delete_contact(self, user_id):
        return self.client._make_request("deleteContact", {"user_id": user_id})

    def block_user(self, user_id):
        return self.client._make_request("blockUser", {"user_id": user_id})

    def unblock_user(self, user_id):
        return self.client._make_request("unblockUser", {"user_id": user_id})

    def get_blocked_users(self):
        return self.client._make_request("getBlockedUsers")