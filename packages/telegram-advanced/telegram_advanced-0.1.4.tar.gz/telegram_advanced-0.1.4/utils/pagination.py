# utils/pagination.py
class PaginationHandler:
    def __init__(self, client, method, params, item_key, page_size=100):
        self.client = client
        self.method = method
        self.params = params
        self.item_key = item_key
        self.page_size = page_size
        self.offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.params['offset'] = self.offset
        self.params['limit'] = self.page_size
        
        result = self.client._make_request(self.method, self.params)
        items = result.get(self.item_key, [])
        
        if not items:
            raise StopIteration
        
        self.offset += len(items)
        return items
