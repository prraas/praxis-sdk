from praxis.core.http import HttpClient
from praxis.models.response import Response

class MultiAgentAPI:
    """
    API for multi-agent coordination and swarm intelligence.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def check_conflicts(self, path_a: list[dict], path_b: list[dict], safe_distance: float = 0.5) -> Response[dict]:
        """
        Check for space-time conflicts between two agent trajectories.
        Paths should be lists of dicts with {'x', 'y', 'z', 't'}.
        """
        payload = {
            "path_a": path_a,
            "path_b": path_b,
            "safe_distance": safe_distance
        }
        return self._http.post("/api/v1/multi-agent/conflict-check", json=payload)

    def formation_pose(self, leader_pose: dict, follower_index: int, pattern: str = "v-shape", spacing: float = 1.0) -> Response[dict]:
        """Calculate target pose for a follower in a formation."""
        payload = {
            "leader_pose": leader_pose,
            "follower_index": follower_index,
            "pattern": pattern,
            "spacing": spacing
        }
        return self._http.post("/api/v1/multi-agent/formation", json=payload)

    def swarm_steering(self, agent_pose: dict, neighbor_poses: list[dict], desired_dist: float = 1.0) -> Response[dict]:
        """Calculate swarm steering vectors (Separation, Cohesion, Alignment)."""
        payload = {
            "agent_pose": agent_pose,
            "neighbor_poses": neighbor_poses,
            "desired_dist": desired_dist
        }
        return self._http.post("/api/v1/multi-agent/swarm", json=payload)
