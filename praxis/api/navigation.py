from praxis.core.http import HttpClient
from praxis.models.response import Response


class NavigationAPI:
    """
    Navigation / pathfinding operations using A* algorithm.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def plan(
        self,
        grid: list[list[int]],
        start: tuple[int, int] | list[int],
        goal: tuple[int, int] | list[int],
    ) -> Response[dict]:
        """
        Plan a navigation path using grid-based A* pathfinding.
        
        Status: Stable (v1-alpha)
        Guarantee: Deterministic

        Args:
            grid: 2D grid where 0 = passable, 1 = obstacle
            start: Starting position (row, col)
            goal: Goal position (row, col)
            
        Returns:
            Response with path, steps, reachable status
        """
        payload = {
            "grid": grid,
            "start": list(start),
            "goal": list(goal),
        }

        return self._http.post(
            "/api/v1/simulate/navigation",
            json=payload,
        )
