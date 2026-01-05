# robostream/core/serializer.py
from robostream.models.errors import InvalidEnvelopeError


class Serializer:
    """
    Validates and normalizes backend response envelope.
    """

    @staticmethod
    def parse_envelope(payload: dict) -> dict:
        if not isinstance(payload, dict):
            raise InvalidEnvelopeError("Response is not a JSON object")

        required_fields = {
            "success",
            "data",
            "error",
            "message",
            "cost",
            "request_id",
        }

        missing = required_fields - payload.keys()
        if missing:
            raise InvalidEnvelopeError(
                f"Malformed response. Missing fields: {missing}"
            )

        return {
            "success": payload["success"],
            "data": payload["data"],
            "error": payload["error"],
            "message": payload["message"],
            "cost": payload["cost"],
            "request_id": payload["request_id"],
        }
