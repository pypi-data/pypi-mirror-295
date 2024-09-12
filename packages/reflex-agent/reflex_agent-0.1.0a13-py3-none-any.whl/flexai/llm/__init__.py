"""Module for interacting with different language models."""

from .client import Client

# Import the default client if available.
try:
    from .anthropic_client import AnthropicClient as DefaultClient
except ImportError:
    DefaultClient = lambda: None
