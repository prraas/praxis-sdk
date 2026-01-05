# robostream/models/envelope.py
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Envelope:
    """
    Exact representation of backend response envelope.
    """

    success: bool
    data: Any
    error: str | None
    message: str | None
    cost: float
    request_id: str
