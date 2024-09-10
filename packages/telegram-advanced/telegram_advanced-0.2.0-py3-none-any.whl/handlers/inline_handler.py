# handlers/inline_handler.py

class InlineHandler:
    def __init__(self, client):
        self.client = client

    async def answer_inline_query(self, inline_query_id, results, **kwargs):
        return await self.client._make_request("answerInlineQuery", {
            "inline_query_id": inline_query_id,
            "results": results,
            **kwargs
        })

    async def handle_inline_query(self, inline_query):
        # Handle incoming inline queries
        query_id = inline_query['id']
        query_text = inline_query['query']
        
        # Example: respond with a simple text result
        results = [
            {
                "type": "article",
                "id": "1",
                "title": "Sample Result",
                "input_message_content": {
                    "message_text": f"You searched for: {query_text}"
                }
            }
        ]
        
        await self.answer_inline_query(query_id, results)

    async def handle_chosen_inline_result(self, chosen_inline_result):
        # Handle when a user selects an inline result
        result_id = chosen_inline_result['result_id']
        query = chosen_inline_result['query']
        
        print(f"User selected result {result_id} for query: {query}")
        # Implement your chosen inline result handling logic here