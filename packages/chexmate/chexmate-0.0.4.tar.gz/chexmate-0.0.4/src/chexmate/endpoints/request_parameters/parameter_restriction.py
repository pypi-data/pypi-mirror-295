from typing import Any, Callable
import inspect


class ParameterRestriction:
    """Basically just a stand-in for a lambda function right now. Additional functionality is planned."""

    def __init__(self, restriction: Callable[[Any], bool]):
        self.restriction = restriction

    def __call__(self, parameter_value: Any, ) -> bool:
        return self.restriction(parameter_value)

    def __str__(self):
        return inspect.getsource(self.restriction).strip()
