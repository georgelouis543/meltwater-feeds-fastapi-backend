import os

from dotenv import load_dotenv

load_dotenv()
PHANTOM_JS_API_URL = os.getenv("PHANTOM_JS_URL")

async def get_javascript_page(url: str):
    pass


async def get_non_javascript_page(url: str):
    pass