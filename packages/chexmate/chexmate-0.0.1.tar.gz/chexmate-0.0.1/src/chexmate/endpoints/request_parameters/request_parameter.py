from typing import Any

from src.chexmate.endpoints.request_parameters.parameter_requirement import ParameterRequirement
from src.chexmate.endpoints.request_parameters.parameter_restriction import ParameterRestriction


class RequestParameter:

    def __init__(self,
                 *,
                 param_name: str,
                 param_types: type | tuple[type, ...],
                 param_value: Any,
                 restrictions: list[ParameterRestriction],
                 description: str,
                 required: bool | ParameterRequirement):
        self.param_name = param_name
        self.param_types = param_types
        self.param_value = param_value
        self.restrictions = restrictions
        self.description = description
        self.required = required

    def validate(self) -> None:
        """Validates the parameter. Will raise a ValueError if it's invalid."""
        required_value = self.required if isinstance(self.required, bool) else self.required(self.param_value)
        if required_value is True and self.param_value is None:
            raise ValueError(f'A required parameter was not given a value: "{self.param_name}"')
        if required_value is False and self.param_value is None:
            return
        if not isinstance(self.param_value, self.param_types):
            raise ValueError(f'The value of the "{self.param_name}" parameter is not the correct type: "{self.param_value}" was expected to be an instance of "{self.param_types}", not "{type(self.param_value)}"')
        for restriction in self.restrictions:
            result = restriction(self.param_value)
            if not result:
                raise ValueError(f'Invalid request parameter detected for "{self.param_name}". The invalid value was "{self.param_value}".')

    def to_dict(self):
        key, val = self.to_key_value_pair()
        return {key: val}

    def to_key_value_pair(self):
        return self.param_name, self.param_value

    def __str__(self):
        return f'''
        Parameter Name: {self.param_name}
        Parameter Value: {self.param_value}
        Parameter Description: {self.description}
        '''
