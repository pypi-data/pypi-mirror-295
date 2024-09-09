# components/payments.py
class PaymentsHandler:
    def __init__(self, client):
        self.client = client

    def send_invoice(self, chat_id, title, description, payload, provider_token, currency, prices, **kwargs):
        return self.client._make_request("sendInvoice", {
            "chat_id": chat_id,
            "title": title,
            "description": description,
            "payload": payload,
            "provider_token": provider_token,
            "currency": currency,
            "prices": prices,
            **kwargs
        })

    def answer_shipping_query(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        return self.client._make_request("answerShippingQuery", {
            "shipping_query_id": shipping_query_id,
            "ok": ok,
            "shipping_options": shipping_options,
            "error_message": error_message
        })
