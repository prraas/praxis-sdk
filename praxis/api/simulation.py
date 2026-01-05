from praxis.core.http import HttpClient
from praxis.models.response import Response


class SimulationAPI:
    """
    Simulation-related operations.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def run(self, scenario: dict) -> Response[dict]:
        """
        Run a simulation scenario.
        """
        payload = {
            "scenario": scenario,
        }

        return self._http.post(
            "/api/v1/simulation/run",
            json=payload,
        )
