from dataclasses import dataclass

from vijil.api import BASE_URL


@dataclass
class VijilClient:
    base_url: str = BASE_URL
    api_key: str = None
