# utils/connection_pool.py
import aiohttp
from aiohttp import ClientSession

class ConnectionPool:
    def __init__(self, pool_size=10):
        self.pool_size = pool_size
        self.session = None

    async def get_session(self):
        if self.session is None:
            self.session = ClientSession(connector=aiohttp.TCPConnector(limit=self.pool_size))
        return self.session

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

# Usage example:
# pool = ConnectionPool()
# session = await pool.get_session()
# async with session.get(url) as response:
#     data = await response.json()
# await pool.close()