from dataclasses import dataclass

from flexai.capability import Capability
from flexai.message import Message, AIMessage
from flexai.tool import ToolCall


@dataclass(frozen=True)
class LimitToolUse(Capability):
    """Force an agent to stop if there are too many tool use."""

    # The maximum number of tool uses allowed.
    max_tool_uses: int

    async def modify_response(
        self, messages: list[Message], response: AIMessage
    ) -> AIMessage:
        # There's nothing to modify
        if not isinstance(response.content, list):
            return response
        
        # Initial: Number of tool uses that this current response requests.
        total_tool_uses = len([entry for entry in response.content if isinstance(entry, ToolCall)])
        
        for message in messages:
            if not isinstance(message.content, list):
                continue
            
            # For each past message, add the number of tool uses it suggested to our total count.
            for entry in message.content:
                if isinstance(entry, ToolCall):
                    total_tool_uses += 1

        # If the total tool use count, including this response, is too much, we can't use one more
        if total_tool_uses > self.max_tool_uses:
            send_message_call = ToolCall(
                id="",
                name="send_message",
                input={"message": f"Exceeded tool usage limit: {self.max_tool_uses}"},
            )
            response.content = [send_message_call]

        return response
