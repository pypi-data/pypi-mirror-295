import requests
from requests import Response
from urllib.parse import urljoin
from abc import ABC, abstractmethod

from chexmate.endpoints.request_parameters.request_parameter_list import RequestParameterList
from chexmate.enums.content_type_enum import ContentType
from chexmate.enums.http_method_enum import HTTPMethod


class BaseEndpoint(ABC):

    def __init__(self, base_url: str, url_tail: str, api_key: str, method: HTTPMethod, content_type: ContentType):
        self._base_url = base_url
        self._url_tail = url_tail
        self._full_url = urljoin(self._base_url, self._url_tail)
        self._api_key = api_key
        self._method = method
        self._content_type = content_type

    @property
    def base_url(self):
        return self._base_url

    @property
    def url_tail(self):
        return self._url_tail

    @property
    def full_url(self):
        return self._full_url

    @property
    def api_key(self):
        return self._api_key

    @property
    def method(self):
        return self._method

    @property
    def content_type(self):
        return self._content_type

    @abstractmethod
    def create_request_header_list(self, **kwargs) -> RequestParameterList:
        """Creates the list of parameters for the header and body of the request.
        Please refer to this method for documentation of each parameter."""
        pass

    @abstractmethod
    def create_request_body_list(self, **kwargs) -> RequestParameterList:
        """Creates the list of parameters for the header and body of the request.
        Please refer to this method for documentation of each parameter."""
        pass

    def send_request(self, header_params: RequestParameterList, body_params: RequestParameterList) -> Response:
        header_params.validate()
        body_params.validate()
        new_request = requests.Request(
            method=self.method.value,
            url=self.full_url,
            headers=header_params.to_dict(),
            json=body_params.to_dict()
        )
        prepared_request = new_request.prepare()
        with requests.session() as sesh:
            resp = sesh.send(prepared_request)
        return resp


