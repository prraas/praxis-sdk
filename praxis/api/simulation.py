from praxis.core.http import HttpClient
from praxis.models.response import Response


class SimulationAPI:
    """
    Simulation operations - currently wraps navigation simulation.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def navigate(
        self,
        grid: list[list[int]],
        start: tuple[int, int] | list[int],
        goal: tuple[int, int] | list[int],
    ) -> Response[dict]:
        """
        Simulate navigation from start to goal.
        
        Args:
            grid: 2D grid where 0 = passable, 1 = obstacle
            start: Starting position (row, col)
            goal: Goal position (row, col)
            
        Returns:
            Response with reachability, steps, and path
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
