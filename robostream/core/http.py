# robostream/core/http.py
import requests

from robostream.core.auth import Auth
from robostream.core.config import Config
from robostream.core.retries import retry
from robostream.core.serializer import Serializer

from robostream.exceptions import (
    APIError,
    ValidationError,
    PaymentError,
    ExecutionError,
)
from robostream.models.envelope import Envelope
from robostream.models.response import Response


class HttpClient:
    """
    Low-level HTTP client.
    Handles transport, retries, auth, error mapping,
    and response normalization.
    """

    def __init__(self, config: Config):
        self._config = config
        self._auth = Auth(config)

    def post(self, path: str, json: dict) -> Response:
        if not path.startswith("/"):
            raise ValueError("API path must start with '/'")

        url = f"{self._config.base_url}{path}"

        def _request():
            try:
                resp = requests.post(
                    url,
                    headers=self._auth.headers(),
                    json=json,
                    timeout=self._config.timeout,
                )
            except requests.RequestException as exc:
                raise APIError(f"Network error: {exc}") from exc

            return self._handle_response(resp)

        return retry(
            _request,
            retries=2,
            backoff=0.5,
            retry_on=(APIError,),
        )

    def _handle_response(self, resp: requests.Response) -> Response:
        try:
            payload = resp.json()
        except Exception:
            raise APIError("Invalid JSON response from server")

        if resp.status_code >= 400:
            self._raise_api_error(payload)

        parsed = Serializer.parse_envelope(payload)
        envelope = Envelope(**parsed)
        return Response(envelope)

    def _raise_api_error(self, payload: dict) -> None:
        error = payload.get("error") or "unknown_error"
        message = payload.get("message") or "Request failed"

        if error == "validation_error":
            raise ValidationError(message)

        if error == "payment_error":
            raise PaymentError(message)

        if error == "execution_error":
            raise ExecutionError(message)

        raise APIError(message)
