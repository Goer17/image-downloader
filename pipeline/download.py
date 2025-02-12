import os
import base64
from pathlib import Path
from abc import ABC, abstractmethod
from typing import (
    List
)
from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup

from urllib.parse import quote_plus
from urllib.parse import urlparse

from utils.logger import logger

class URLCrawler(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def __call__(
        self,
        query: str,
        max_n: int = 10
    ) -> List[str]:
        pass

class GoogleURLCrawler(URLCrawler):
    """
    > fetching images' url from images.google.com
    """
    def __init__(self):
        super().__init__()
        self.url = "https://www.google.com"
    
    def __call__(self, query: str, max_n: int = 10) -> List[str]:
        if max_n <= 0:
            return []
        url = f"{self.url}/search?q={quote_plus(query)}&tbm=isch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
        }
        
        try:
            session = HTMLSession()
            response = session.get(url, headers=headers)
            response.html.render(timeout=20) # render the page
            
            soup = BeautifulSoup(response.html.html, "html.parser")
            imgs = soup.find_all("img")
            urls = []
            for img in imgs:
                if img.has_attr("id") and img["id"].startswith("dimg") and img.has_attr("src") and len(img["src"]) >= 4096:
                    urls.append(img["src"])
            return urls   
        
        except Exception as e:
            logger.error(f"GoogleDowloader.__call__() : {e}")
            return []


class Downloader:
    def __init__(self):
        raise RuntimeError("Downloader is a static class.")

    @staticmethod
    def download(urls: List[str], path: str | Path):
        if not os.path.exists(path):
            os.makedirs(path)

        for i, url in enumerate(urls):
            parsed = urlparse(url)

            if parsed.scheme in ("http", "https"):
                Downloader._download_http(url, path, i)
            elif url.startswith("data:"):
                Downloader._download_base64(url, path, i)
            else:
                print(f"Unsupported URL format: {url}")

    @staticmethod
    def _download_http(url: str, path: str, index: int):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            filename = os.path.join(path, f"image_{index}{Downloader._get_extension(url)}")
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            
            logger.info(f"Downloaded: {filename}")
        except Exception as e:
            logger.info(f"Failed to download {url}: {e}")

    @staticmethod
    def _download_base64(data_url: str, path: str, index: int):
        try:
            header, encoded = data_url.split(",", 1)
            ext = Downloader._get_base64_extension(header)
            decoded = base64.b64decode(encoded)

            filename = os.path.join(path, f"image_{index}{ext}")
            with open(filename, "wb") as f:
                f.write(decoded)

            logger.info(f"Decoded and saved: {filename}")
        except Exception as e:
            logger.info(f"Failed to decode base64: {e}")

    @staticmethod
    def _get_extension(url: str) -> str:
        parsed = urlparse(url)
        ext = os.path.splitext(parsed.path)[-1]
        return ext if ext else ".bin"

    @staticmethod
    def _get_base64_extension(header: str) -> str:
        if "image/png" in header:
            return ".png"
        elif "image/jpeg" in header:
            return ".jpg"
        elif "image/gif" in header:
            return ".gif"
        elif "application/pdf" in header:
            return ".pdf"
        else:
            return ".bin"