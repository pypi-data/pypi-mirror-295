"""Base class to define agent tools."""

import inspect
from dataclasses import dataclass
from typing import Callable, Any
from collections import namedtuple


@dataclass(frozen=True)
class Tool:
    """A tool is a function that can be called by an agent."""

    # The name of the tool.
    name: str

    # A description of how the tool works - this should be detailed
    description: str

    # The function parameters and their types.
    params: tuple[tuple[str, str], ...]

    # The return type of the function.
    return_type: str

    # The function to call.
    fn: Callable

    @classmethod
    def from_function(cls, func: Callable):
        """Create a tool from a function."""
        signature = inspect.signature(func)
        params = tuple(
            (
                (
                    name,
                    (
                        param.annotation.__name__
                        if hasattr(param.annotation, "__name__")
                        else "No annotation"
                    ),
                )
            )
            for name, param in signature.parameters.items()
        )
        return_type = (
            signature.return_annotation.__name__
            if hasattr(signature.return_annotation, "__name__")
            else "No annotation"
        )
        description = inspect.getdoc(func) or "No description"
        return cls(
            name=func.__name__,
            description=description,
            params=params,
            return_type=return_type,
            fn=func,
        )

    def to_description(self) -> dict:
        """Convert the tool to a description."""
        type_map = {
            "str": "string",
            "int": "number",
            "float": "number",
            "bool": "boolean",
            "list": "array",
            "dict": "object",
        }

        input_schema = {
            "type": "object",
            "properties": {},
        }
        for param_name, param_type in self.params:
            param_type = type_map.get(str(param_type), param_type)
            input_schema["properties"][param_name] = {
                "type": param_type,
            }

        description = {
            "name": self.name,
            "description": self.description,
            "input_schema": input_schema,
        }
        return description

ToolCallBase = namedtuple('ToolCallBase', ['id', 'name', 'input', 'type'])

class ToolCall(ToolCallBase):
    """A tool call is a request to execute a tool."""

    def __new__(cls, id: str, name: str, input: Any, type: str = 'ToolCall'):
        assert type == 'ToolCall'
        return super(ToolCall, cls).__new__(cls, id=id, name=name, input=input, type=type)
    

ToolResultBase = namedtuple('ToolResultBase', ['tool_use_id', 'result', 'execution_time', 'is_error', 'type'])

class ToolResult(ToolResultBase):
    """The result of a tool invocation."""

    def __new__(cls, tool_use_id: str, result: Any, execution_time: float, is_error: bool = False, type: str = 'ToolResult'):
        assert type == 'ToolResult'
        return super(ToolResult, cls).__new__(cls, tool_use_id=tool_use_id, result=result, execution_time=execution_time, is_error=is_error, type=type)

def parse_tool_item(item: Any) -> Any:
    if isinstance(item, list):
        if item[-1] == 'ToolCall':
            return ToolCall(*item)
        
        if item[-1] == 'ToolResult':
            return ToolResult(*item)
        
    if isinstance(item, dict):
        if item['type'] == 'ToolCall':
            return ToolCall(**item)
        
        if item['type'] == 'ToolResult':
            return ToolResult(**item)
    
    return item

def send_message(message: str) -> None:
    """Send a final message to the user. This should be done after all internal processing is completed."""
    pass
