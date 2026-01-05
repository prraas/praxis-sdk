# robostream/core/config.py
import os


class Config:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 10.0,
    ):
        self.api_key = api_key or os.getenv("ROBOSTREAM_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key missing. Set ROBOSTREAM_API_KEY or pass api_key explicitly."
            )

        self.base_url = (
            base_url
            or os.getenv("ROBOSTREAM_BASE_URL")
            or "http://localhost:8000"
        ).rstrip("/")

        self.timeout = timeout
