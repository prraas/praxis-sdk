from praxis.core.http import HttpClient
from praxis.models.response import Response 

class ManipulationAPI:
    """
    API for robotic manipulation skills (Pick, Place, Move).
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def pick(
            self,
            object_position: list[float],
            gripper_position: list[float],
            object_size: list[float],
            gripper_opening: float,
            obstacles: list[dict] | None = None,
            object_mass: float = 0.5,
            object_material: str = "plastic"
    ) -> Response[dict]:
        """
        Assess pick feasibility for an object.

        Evaluates reachability, grasp feasibility, collision detection, and calculates a grasp quality score.
        """

        payload = {
            "object_position": object_position,
            "gripper_position": gripper_position,
            "object_size": object_size,
            "gripper_opening": gripper_opening,
            "object_mass": object_mass,
            "object_material": object_material
        }

        if obstacles is not None:
            payload["obstacles"] = obstacles

        return self._http.post(
            "/api/v1/skills/pick",
            json=payload,
        )
