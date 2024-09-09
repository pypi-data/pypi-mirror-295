import os

from src.chexmate.endpoints.endpoints import Endpoints
from src.chexmate.enums.seamless_chex_base_url_enum import SeamlessChexBaseUrl


class SeamlessChex:

    def __init__(self, api_key: str, is_production_mode: bool = False):
        self._is_production_mode = is_production_mode
        self._base_url = SeamlessChexBaseUrl.PRODUCTION_BASE_URL.value if self._is_production_mode else SeamlessChexBaseUrl.SANDBOX_BASE_URL.value
        self._api_key = api_key
        self.endpoints = Endpoints(self.base_url, self.api_key)

    @property
    def is_production_mode(self):
        return self._is_production_mode

    @property
    def base_url(self):
        return self._base_url

    @property
    def api_key(self):
        return self._api_key
