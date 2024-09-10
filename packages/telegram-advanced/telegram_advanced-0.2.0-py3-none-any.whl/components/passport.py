# components/passport.py
class PassportHandler:
    def __init__(self, client):
        self.client = client

    def request_passport_data(self, chat_id, scope, nonce):
        return self.client._make_request("requestPassportData", {
            "chat_id": chat_id,
            "scope": scope,
            "nonce": nonce
        })

    def set_passport_data_errors(self, user_id, errors):
        return self.client._make_request("setPassportDataErrors", {
            "user_id": user_id,
            "errors": errors
        })