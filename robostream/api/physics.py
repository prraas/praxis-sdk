# robostream/api/physics.py
from robostream.core.http import HttpClient
from robostream.models.response import Response


class PhysicsAPI:
    """
    Physics-related operations.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def force(self, mass: float, acceleration: float) -> Response[dict]:
        """
        Compute force using F = m * a.
        """
        payload = {
            "mass": mass,
            "acceleration": acceleration,
        }

        return self._http.post(
            "/api/v1/physics/force",
            json=payload,
        )
