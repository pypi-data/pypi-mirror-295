from collections import UserList

from src.chexmate.endpoints.request_parameters.request_parameter import RequestParameter


class RequestParameterList(UserList):
    """A simple list of RequestParameter objects, with some additional functionality rolled in."""

    def __init__(self, *request_parameters: RequestParameter):
        super().__init__(request_parameters)

    def validate(self) -> None:
        """If any RequestParameters in this list are invalid, this method will raise a ValueError."""
        for param in self:
            param.validate()

    def to_dict(self) -> dict:
        """Converts this list of RequestParameters to a dict that can be inserted into a header or body section of a
        request. Any RequestParameters with a value of None will be omitted from the dictionary."""
        result = {}
        for param in self:
            key, value = param.to_key_value_pair()
            if value is not None:
                result.update({key: value})
        return result

    def __str__(self):
        return ''.join([str(x) for x in self])
