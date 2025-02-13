from pathlib import Path
from typing import (
    List, Dict
)

from .layer.download import URLCrawler, GoogleURLCrawler, Downloader
from .layer.llm import Critic

class Pipeline:
    def __init__(
        self,
        crawlers: List[URLCrawler],
        layers: List[Critic]
    ):
        self.crawlers = crawlers
        self.layers = layers
    
    def __call__(
        self,
        query: str,
        text: str,
        max_n: int = 10,
        dowload_path: str | Path = None
    ) -> List[Dict[str, str]]:
        urls = []
        for crawler in self.crawlers:
            urls += crawler(query, max_n)
        for layer in self.layers:
            urls = layer(urls, text)
        
        if dowload_path is not None:
            Downloader.download(urls, dowload_path)
        
        return urls
