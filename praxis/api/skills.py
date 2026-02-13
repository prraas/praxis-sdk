# SKILLS Api for manipulation and perception operations 

from praxis.core.http import HttpClient
from praxis.models.response import Response 

# Robotics skills for manipulation and perception
class SkillsAPI:
    # provides high-level skills for object manipulation ( pick, sort , align )

    def __init__(self, http: HttpClient):
        self._http = http

    def pick(
            self,
            object_position: list[float],
            gripper_position: list[float],
            object_size: list[float],
            gripper_opening: float,
            obstacles: list[dict] | None = None,
    ) -> Response[dict]:
        """
        Access pick feasibility for an object.

        Evaluates reachability, grasp feasibility, collision detection, and calculates a grasp quality score.
        """

        payload = {
            "object_position": object_position,
            "gripper_position": gripper_position,
            "object_size": object_size,
            "gripper_opening": gripper_opening
        }

        if obstacles is not None:
            payload["obstacles"] = obstacles

        return self._http.post(
            "/api/v1/skills/pick",
            json=payload,
        )
    
    def identify(
            self,
            scene: dict,
            confidence_threshold: float = 0.5,
    ) -> Response[dict]:
        """
        Identify objects in a scene.

        Detects and classifies objects with bounding boxes and confidence scores.
        """

        payload = {
            "scene": scene,
            "confidence_threshold": confidence_threshold
        }

        return self._http.post(
            "/api/v1/robotics/detect",
            json=payload,
        )
