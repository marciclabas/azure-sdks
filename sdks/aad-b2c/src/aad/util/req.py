import aiohttp

async def get(url: str) -> bytes:
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url) as r:
            return await r.content.read()