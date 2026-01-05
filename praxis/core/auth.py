from praxis.core.config import Config


class Auth:
    def __init__(self, config: Config):
        self._config = config

    def headers(self) -> dict:
        return {
            "X-API-Key": self._config.api_key,
            "Content-Type": "application/json",
        }
