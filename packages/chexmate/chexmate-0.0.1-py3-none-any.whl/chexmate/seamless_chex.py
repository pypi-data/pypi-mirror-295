import os

from src.chexmate.endpoints.endpoints import Endpoints
from src.chexmate.enums.seamless_chex_base_url_enum import SeamlessChexBaseUrl


class SeamlessChex:

    def __init__(self):
        self._seamless_chex_environment = os.environ.get('SEAMLESS_CHEX_ENVIRONMENT')
        if self._seamless_chex_environment is None:
            raise ValueError(f'The "SEAMLESS_CHEX_ENVIRONMENT" environment variable needs to be set with a string representing either "PRODUCTION" for production mode or anything else for sandbox mode. It is currently {self._seamless_chex_environment}')
        self._is_sandbox_mode = self._seamless_chex_environment != 'PRODUCTION'
        self._base_url = SeamlessChexBaseUrl.SANDBOX_BASE_URL.value if self._is_sandbox_mode else SeamlessChexBaseUrl.PRODUCTION_BASE_URL.value
        self._api_key = os.environ.get('SEAMLESS_CHEX_API_KEY')
        if self._api_key is None:
            raise ValueError(f'The "SEAMLESS_CHEX_API_KEY" environment variable needs to be set with either the base sandbox or base production api key.')

        self.endpoints = Endpoints(self.base_url, self.api_key)

    @property
    def is_sandbox_mode(self):
        return self._is_sandbox_mode

    @property
    def seamless_chex_environment(self):
        return self._seamless_chex_environment

    @property
    def api_key(self):
        return self._api_key

    @property
    def base_url(self):
        return self._base_url
