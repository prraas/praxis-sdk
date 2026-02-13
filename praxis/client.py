from praxis.core.config import Config
from praxis.core.http import HttpClient

from praxis.api.physics import PhysicsAPI
from praxis.api.navigation import NavigationAPI
from praxis.api.simulation import SimulationAPI
from praxis.api.vision import VisionAPI
from praxis.session import Session
from praxis.api.skills import SkillsAPI


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
        
        # Phase 1: Access Boundary Check

        self._http = HttpClient(self.config)

        # Public domain APIs
        self.physics = PhysicsAPI(self._http)
        self.navigation = NavigationAPI(self._http)
        self.simulation = SimulationAPI(self._http)
        self.vision = VisionAPI(self._http)
        self.skills = SkillsAPI(self._http)

    def session(self) -> Session:
        """
        Create an agent/session context.
        """
        return Session(self)
