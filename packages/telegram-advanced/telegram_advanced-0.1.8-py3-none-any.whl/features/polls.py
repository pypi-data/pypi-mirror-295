# features/polls.py

class PollHandler:
    def __init__(self, client):
        self.client = client

    async def send_poll(self, chat_id, question, options, **kwargs):
        return await self.client._make_request("sendPoll", {
            "chat_id": chat_id,
            "question": question,
            "options": options,
            **kwargs
        })

    async def stop_poll(self, chat_id, message_id, **kwargs):
        return await self.client._make_request("stopPoll", {
            "chat_id": chat_id,
            "message_id": message_id,
            **kwargs
        })

    async def handle_poll(self, poll):
        # Handle incoming poll updates
        print(f"Received poll update: {poll['id']}")
        # Implement your poll handling logic here

    async def handle_poll_answer(self, poll_answer):
        # Handle incoming poll answer updates
        print(f"Received poll answer: {poll_answer['poll_id']}")
        # Implement your poll answer handling logic here