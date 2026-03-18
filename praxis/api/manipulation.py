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

    def grasp_feasibility(
        self,
        object_width: float,
        gripper_max_aperture: float,
        gripper_min_aperture: float = 0.0,
    ) -> Response[dict]:
        """
        Assess feasibility of a grasp based on object and gripper geometry.

        Args:
            object_width: Width of the object to grasp in meters.
            gripper_max_aperture: Maximum opening of the gripper in meters.
            gripper_min_aperture: Minimum opening of the gripper in meters.

        Returns:
            Response with feasibility score, and warnings if any.
        """
        payload = {
            "object_width": object_width,
            "gripper_max_aperture": gripper_max_aperture,
            "gripper_min_aperture": gripper_min_aperture,
        }

        return self._http.post(
            "/api/v1/robotics/grasp/feasibility",
            json=payload,
        )

    def grasp_closure(
        self,
        contacts: list[dict[str, float]],
        friction_mu: float = 0.4,
    ) -> Response[dict]:
        """
        Validate force-closure for a set of contact points.

        Args:
            contacts: List of contact points with normals {"x", "y", "nx", "ny"}.
            friction_mu: Coefficient of friction.

        Returns:
            Response with has_closure status and closure score.
        """
        payload = {
            "contacts": contacts,
            "friction_mu": friction_mu,
        }

        return self._http.post(
            "/api/v1/robotics/grasp/closure",
            json=payload,
        )
