from typing import Generic, TypeVar
from praxis.models.envelope import Envelope

T = TypeVar("T")


class Response(Generic[T]):
    """
    High-level SDK response object.
    """

    def __init__(self, envelope: Envelope):
        self._envelope = envelope

    @property
    def data(self) -> T:
        return self._envelope.data

    @property
    def cost(self) -> float:
        return self._envelope.cost

    @property
    def request_id(self) -> str:
        return self._envelope.request_id

    @property
    def success(self) -> bool:
        return self._envelope.success

    def __repr__(self) -> str:
        return (
            f"<Response success={self.success} "
            f"cost={self.cost} request_id={self.request_id}>"
        )
