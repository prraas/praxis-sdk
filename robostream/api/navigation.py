# robostream/api/navigation.py
from robostream.core.http import HttpClient
from robostream.models.response import Response


class NavigationAPI:
    """
    Navigation / pathfinding operations.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def plan(
        self,
        start: dict,
        goal: dict,
        obstacles: list[dict] | None = None,
    ) -> Response[dict]:
        """
        Plan a navigation path.
        """
        payload = {
            "start": start,
            "goal": goal,
            "obstacles": obstacles or [],
        }

        return self._http.post(
            "/api/v1/navigation/plan",
            json=payload,
        )
