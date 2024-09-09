from dataclasses import dataclass, field

from flexai.capability import Capability
from flexai.message import Message


@dataclass(frozen=True)
class Scratchpad(Capability):
    """Track agent state"""

    # The agent state.
    state: dict = field(default_factory=dict)

    async def modify_response(self, messages: list[Message]) -> list[Message]:
        print(messages[-1])
        return messages
