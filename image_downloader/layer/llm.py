from typing import (
    List, Dict,
    Callable
)
import asyncio
from openai import AsyncClient

from ..utils.logger import logger


class Critic:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        sys_prompt: str,
        filter_func: Callable
    ):
        self.client = AsyncClient(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model
        self.sys_prompt = sys_prompt
        self.filter_func = filter_func
        
    async def fetch(self, url: str, text: str):
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.sys_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": text},
                        {"type": "image_url", "image_url": {"url": url}}
                    ]}
                ]
            )
        except Exception as e:
            logger.error(f"Critic.fetch() : {e}")
            return None
        content = response.choices[0].message.content
        return {"url": url, "content": content} if self.filter_func(content) else None

    def __call__(self, urls: List[Dict[str, str]], text: str) -> List[Dict[str, str]]:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self.fetch(url_info["url"], text) for url_info in urls]
        results = loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
        return [r for r in results if r is not None]