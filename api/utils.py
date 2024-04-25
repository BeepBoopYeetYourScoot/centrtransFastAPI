import httpx
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def get_async(url):
    async with httpx.AsyncClient(verify=False, timeout=600) as client:
        return await client.get(url)
