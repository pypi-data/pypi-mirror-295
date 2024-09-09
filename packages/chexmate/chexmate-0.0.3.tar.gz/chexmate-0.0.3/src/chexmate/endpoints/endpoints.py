from chexmate.endpoints.create_a_check_endpoint import CreateACheckEndpoint


class Endpoints:

    def __init__(self, base_url: str, api_key: str):
        self.create_a_check: CreateACheckEndpoint = CreateACheckEndpoint(base_url, api_key)
