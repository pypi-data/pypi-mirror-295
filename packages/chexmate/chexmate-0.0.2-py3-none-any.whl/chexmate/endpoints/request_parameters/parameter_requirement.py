from typing import Any, Callable


class ParameterRequirement:
    """Basically just a stand-in for a lambda function right now. Additional functionality is planned."""

    def __init__(self, requirement: Callable[[Any], bool]):
        self.requirement = requirement

    def __call__(self, parameter_value: Any, ) -> bool:
        return self.requirement(parameter_value)