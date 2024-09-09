# utils/rate_limiter.py
import time
from functools import wraps

class RateLimiter:
    def __init__(self, max_calls, time_frame):
        self.max_calls = max_calls
        self.time_frame = time_frame
        self.calls = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            self.calls = [call for call in self.calls if call > now - self.time_frame]
            
            if len(self.calls) >= self.max_calls:
                sleep_time = self.calls[0] - (now - self.time_frame)
                time.sleep(sleep_time)
            
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper

# Usage example:
# @RateLimiter(max_calls=30, time_frame=1)  # 30 calls per second
# def some_api_call():
#     pass





# utils/batch_processing.py
async def process_in_batches(items, batch_size, process_func):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        await process_func(batch)

# Usage example:
# async def send_messages(users):
#     async def send_batch(batch):
#         for user in batch:
#             await bot.send_message(user.id, "Hello!")
#     await process_in_batches(users, 100, send_batch)