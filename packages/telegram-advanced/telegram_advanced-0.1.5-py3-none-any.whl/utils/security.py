# utils/security.py
import hashlib
import hmac
import time
import os

class SecurityHandler:
    def __init__(self, client):
        self.client = client

    def generate_2fa_password(self, password, salt):
        # This is a simplified example. In a real-world scenario, use a proper password hashing algorithm
        return hashlib.sha256(password.encode() + salt.encode()).hexdigest()

    def verify_2fa(self, user_id, provided_password):
        # Fetch the user's salt and stored password hash from your database
        stored_salt, stored_hash = self.get_user_2fa_info(user_id)
        
        calculated_hash = self.generate_2fa_password(provided_password, stored_salt)
        return hmac.compare_digest(calculated_hash, stored_hash)

    def get_user_2fa_info(self, user_id):
        # Implement fetching user's 2FA info from your database
        pass

    def set_user_2fa(self, user_id, password):
        salt = self.generate_salt()
        password_hash = self.generate_2fa_password(password, salt)
        # Store salt and password_hash in your database for the user
        pass

    def generate_salt(self):
        return os.urandom(16).hex()

    def verify_update(self, update_json, bot_token):
        # Verify update authenticity (for webhook setups)
        data = update_json.encode()
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        computed_hash = hmac.new(secret_key, data, hashlib.sha256).hexdigest()
        return computed_hash == update_json.get('hash')