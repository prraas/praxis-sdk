# robostream/client.py
from robostream.core.config import Config
from robostream.core.http import HttpClient

from robostream.api.physics import PhysicsAPI
from robostream.api.navigation import NavigationAPI
from robostream.api.simulation import SimulationAPI
from robostream.session import Session


class Client:
    """
    Main SDK entry point.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 10.0,
    ):
        self.config = Config(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )

        self._http = HttpClient(self.config)

        # Public domain APIs
        self.physics = PhysicsAPI(self._http)
        self.navigation = NavigationAPI(self._http)
        self.simulation = SimulationAPI(self._http)

    def session(self) -> Session:
        """
        Create an agent/session context.
        """
        return Session(self)
