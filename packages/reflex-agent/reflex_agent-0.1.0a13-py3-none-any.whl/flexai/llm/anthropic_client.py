from __future__ import annotations
import json
import os
from dataclasses import dataclass, field, replace
from typing import AsyncGenerator, TYPE_CHECKING, Type

# Try to import the anthropic library.
try:
    from anthropic import AsyncAnthropic
    from anthropic.types import ToolUseBlock
    from pydantic import BaseModel
except ImportError:
    raise ImportError(
        "The anthropic library is required for the AnthropicClient. "
        "Please install it using `pip install anthropic`."
    )
from flexai.llm.client import Client
from flexai.message import (
    AIMessage,
    Message,
    UserMessage,
)
from flexai.tool import ToolCall, ToolResult

if TYPE_CHECKING:
    from flexai.tool import Tool

def get_tool_call(tool_use: ToolUseBlock) -> ToolCall:
    """Get the tool call from a tool use block.

    Args:
        tool_use: The tool use block to get the call from.

    Returns:
        The tool call from the tool use block.
    """
    return ToolCall(
        id=tool_use.id,
        name=tool_use.name,
        input=tool_use.input,
    )

@dataclass(frozen=True)
class AnthropicClient(Client):
    """Client for interacting with the Anthropic language model."""

    # The client to use for interacting with the model.
    client: AsyncAnthropic = AsyncAnthropic()

    # The model to use for generating responses.
    model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")

    # The maximum number of tokens to generate in a response.
    max_tokens: int = 8192

    # Extra headers to include in the request.
    extra_headers: dict = field(default_factory=lambda: {"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"})

    async def get_chat_response(
        self,
        messages: list[Message],
        system: str = "",
        tools: list[Tool] | None = None,
    ) -> AIMessage:
        # Get the response from the chat model.
        
        # Create a new list of messages with JSON-dumped content if it's not a string
        for i in range(len(messages)):
            if not isinstance(messages[i].content, str):
                try:
                    if not isinstance(messages[i], Message):
                        messages[i].content = json.dumps(messages[i].content)
                    else:
                        messages[i] = replace(messages[i], content=json.dumps(messages[i].content))
                except:
                    breakpoint()
        

        # Get the response from the chat model.
        response = await self.client.messages.create(
            **self._get_params(messages, system, tools)
        )

        tool_uses = [get_tool_call(message) for message in response.content if isinstance(message, ToolUseBlock)]

        content_to_return = tool_uses or '\n'.join([message.text for message in response.content])

        return AIMessage(
            content = content_to_return,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    async def stream_chat_response(
        self,
        messages: list[Message],
        system: str = "",
        tools: list[Tool] | None = None,
    ) -> AsyncGenerator[AIMessage, None]:
        async with self.client.messages.stream(
            **self._get_params(messages, system, tools)
        ) as stream:
            async for text in stream.text_stream:
                yield AIMessage(content=text)

    def _get_params(self, messages, system, tools) -> dict:
        """Get the common params to send to the model.

        Args:
            messages: The messages to send to the model.
            system: The system message to send to the model.
            tools: The tools to send to the model.

        Returns:
            The common params to send to the model.
        """
        kwargs = {
            "max_tokens": self.max_tokens,
            "messages": self.to_llm_messages(messages),
            "model": self.model,
            "system": system,
            "extra_headers": self.extra_headers,
        }

        # If tools are provided, force the model to use them (for now).
        if tools:
            kwargs["tools"] = self.to_tool_descriptions(tools)
            kwargs["tool_choice"] = {"type": "any"}
        else:
            kwargs["tools"] = []
        return kwargs

    @staticmethod
    def to_llm_messages(messages: list[Message]) -> list[dict]:
        """Convert messages to the Anthropic format.

        Args:
            messages: The messages to convert.

        Returns:
            The messages in the anthropic format.
        """
        return [{"role": m.role, "content": m.content} for m in messages]

    @staticmethod
    def to_tool_descriptions(tools: list[Tool]) -> list[dict]:
        """Convert tools to the Anthropic format.

        Args:
            tools: The tools to convert.

        Returns:
            The tools in the anthropic format.
        """
        return [tool.to_description() for tool in tools]
    

    async def get_structured_response(
        self,
        messages: list[Message],
        model: Type[BaseModel],
        system: str | None = None,
    ) -> list[Type[BaseModel]]:
        """Get the structured response from the chat model.
        Args:
            messages: The messages to send to the model.
            model: The model to use for the response.
        Returns:
            The structured response from the model.
        """
        system = f"""{system or ""}
Return your answer according to the 'properties' of the following schema:
{model.schema()}
Return only the JSON object with the properties filled in.
Do not include anything in your response other than the JSON object.
Do not begin your response with ```json or end it with ```.
"""
        responses = await self.get_chat_response(messages, system=system)
        results = []
        for response in responses:
            try:
                obj = model.parse_raw(response.content)
                results.append(obj)
            except Exception as e:
                # Try again, printing the exception.
                messages = messages + [
                    response,
                    UserMessage(
                        content=f"There was an error while parsing. Make sure to only include the JSON. Error: {e}"
                    ),
                ]
                return await self.get_structured_response(
                    messages, model=model, system=system
                )
        return results
