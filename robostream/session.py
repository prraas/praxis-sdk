# robostream/session.py
from typing import Any


class Session:
    """
    Session groups multiple SDK calls
    under a logical execution context.

    Useful for:
    - agent loops
    - multi-step workflows
    - future optimizations (batching, tracing)
    """

    def __init__(self, client: Any):
        self._client = client
        self._active = False

    def __enter__(self):
        self._active = True
        return self

    def __exit__(self, exc_type, exc, tb):
        self._active = False
        return False  # propagate exceptions

    # Pass-through access to APIs

    @property
    def physics(self):
        return self._client.physics

    @property
    def navigation(self):
        return self._client.navigation

    @property
    def simulation(self):
        return self._client.simulation
