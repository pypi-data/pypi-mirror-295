"""Core agent definitions and functionality for the FlexAI framework.

Defines the Agent class for managing conversations, invoking tools, and
interacting with language models. Provides core functionality for creating
flexible AI agents capable of using various tools and capabilities to assist users.
"""

from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from typing import AsyncGenerator, Callable, TYPE_CHECKING

from flexai.llm import Client, DefaultClient
from flexai.message import (
    AIMessage,
    Message,
)
from flexai.tool import Tool, ToolCall, ToolResult, send_message

if TYPE_CHECKING:
    from flexai.capability import Capability


@dataclass(frozen=True)
class Agent:
    """LLM-powered agent using tools and capabilities to interact with users.

    Manages conversation flow, invokes tools, and leverages a language model
    to generate responses. Supports customization through capabilities and
    a flexible toolset.
    """

    # The system prompt to use for the agent.
    prompt: str = ""

    # A list of functions that the agent can call and use.
    tools: list[Callable] = field(default_factory=list, repr=False)

    # Hooks that can plugin to the main agent loop to modify its behavior.
    capabilities: list[Capability] = field(default_factory=list)

    # The language model to use for the agent.
    llm: Client | None = DefaultClient()

    # The mapping of tool names to tool functions.
    toolbox: dict[str, Tool] = field(default_factory=dict, init=False)

    def __post_init__(self):
        """Perform post-initialization setup."""
        # Always include the send_message tool.
        tools = (self.tools or []) + [send_message]

        # Convert callables to tools and store them in the toolbox.
        tools = {Tool.from_function(tool) for tool in set(tools)}
        tools = {tool.name: tool for tool in tools}

        # Hack around dataclass immutability.
        object.__setattr__(self, "toolbox", tools)

    def is_nonempty_list_of_class(self, content, cls):
        """
        Helper function that lets us determine if content is a list, 
        is not empty, and every element of it is an instance of cls.
        """
        return (
            isinstance(content, list)
            and len(content) > 0
            and all([isinstance(elt, cls) for elt in content])
        )

    async def modify_messages(self, messages: list[Message]) -> list[Message]:
        """Hook to modify the messages before sending them to the LLM.

        Args:
            messages: The current conversation messages.

        Returns:
            The modified messages.
        """
        # Iterate through the capabilities and modify the messages.
        for capability in self.capabilities:
            messages = await capability.modify_messages(messages)
        return messages

    async def get_system_message(self) -> str:
        """Hook to modify the system message before sending it to the LLM.

        Returns:
            The modified system message.
        """
        system = self.prompt

        # Iterate through the capabilities and modify the system message.
        for capability in self.capabilities:
            system = await capability.modify_prompt(system)
        return system

    async def modify_response(
        self, messages: list[Message], response: AIMessage
    ) -> AIMessage:
        """Hook to modify the AI response before sending it to the user.

        Args:
            messages: The current conversation messages.
            response: The AI response.

        Returns:
            The modified AI response.
        """
        # Iterate through the capabilities and modify the response.
        for capability in self.capabilities:
            response = await capability.modify_response(messages, response)
        return response

    async def invoke_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool and return the result.

        Handles both synchronous and asynchronous tools, times the execution,
        and catches any exceptions during invocation.

        Args:
            message: Tool use message with name and input parameters.

        Returns:
            The tool invocation result, including execution time and errors.
        """
        # Load the params.
        tool = self.toolbox[tool_call.name]

        # By default, no error
        is_error = False

        # Invoke the tool, time it, and return the result or the exception.
        start_time = time.time()
        try:
            if asyncio.iscoroutinefunction(tool.fn):
                result = await tool.fn(**tool_call.input)
            else:
                result = tool.fn(**tool_call.input)
        except Exception as e:
            result = str(e)
            is_error = True
        end_time = time.time()

        return ToolResult(
            tool_call.id, result, execution_time = end_time - start_time, is_error=is_error
        )

    async def step(self, messages: list[Message]) -> AIMessage:
        """Process a single turn in the conversation.

        Generates a response using the language model and determines if any
        tools need to be invoked based on the current conversation state.

        Args:
            messages: Current conversation messages.

        Returns:
            The generated responses, including potential tool use messages.

        Raises:
            If no LLM client is provided.
        """
        # Ensure an LLM client is provided.
        if self.llm is None:
            raise ValueError("No LLM client provided.")

        # Preprocess the messages and get the system message.
        messages = await self.modify_messages(messages)
        system = await self.get_system_message()

        # Get the response from the LLM.
        response = await self.llm.get_chat_response(
            messages, system=system, tools=list(self.toolbox.values())
        )

        # Return the tool use message.
        response = await self.modify_response(messages, response)

        # Base case: no tool uses suggested at all
        if (
            self.is_nonempty_list_of_class(response.content, ToolCall)
            and response.content[0].name == "send_message"
        ):
            return AIMessage(content=response.content[0].input["message"])

        return response

    async def stream(self, messages: list[Message]) -> AsyncGenerator[Message, None]:
        """Generate an asynchronous stream of agent responses and tool invocations.

        Processes conversation steps and invokes tools until a final response
        (non-tool use message) is generated.

        Args:
            messages: Initial conversation messages.

        Yields:
            Message: Each message in the conversation, including tool uses and results.
        """
        # Run in a loop.
        while True:
            # Get the response and yield.
            responses = await self.step(messages)
            for response in responses:
                yield response

                # If it's not a tool use, end the stream.
                if not self.is_nonempty_list_of_class(response.content, ToolCall):
                    return

                # Invoke the tool and yield.
                result = await self.invoke_tool(response)
                yield result

                # Append the messages.
                messages.append(response)
                messages.append(result)
