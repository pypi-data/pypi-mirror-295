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