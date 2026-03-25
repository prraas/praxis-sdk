from praxis.core.http import HttpClient
from praxis.models.response import Response


class PhysicsAPI:
    """
    Physics-related operations.
    All methods are deterministic: same input always produces same output.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def force(self, mass: float, acceleration: float) -> Response[dict]:
        """
        Compute force using F = m * a.

        Status: Stable (v1-alpha)
        Guarantee: Deterministic
        """
        payload = {
            "mass": mass,
            "acceleration": acceleration,
        }

        return self._http.post(
            "/api/v1/physics/force",
            json=payload,
        )

    def mass(self, volume: float, density: float) -> Response[dict]:
        """Compute mass using m = p * V."""
        payload = {"volume": volume, "density": density}
        return self._http.post("/api/v1/physics/mass", json=payload)

    def stability(self, base_width: float, center_of_mass_height: float) -> Response[dict]:
        """Compute simple stability score."""
        payload = {"base_width": base_width, "center_of_mass_height": center_of_mass_height}
        return self._http.post("/api/v1/physics/stability", json=payload)

    def collision(
        self,
        box_a: dict,
        box_b: dict,
    ) -> Response[dict]:
        """
        Check if two 3D axis-aligned bounding boxes (AABB) overlap.

        Each box must have keys: x, y, z (center position) and w, h, d (dimensions).

        Args:
            box_a: First bounding box {"x": ..., "y": ..., "z": ..., "w": ..., "h": ..., "d": ...}
            box_b: Second bounding box (same format)

        Returns:
            Response with:
                - colliding (bool): True if boxes overlap
                - penetration: per-axis overlap depth {x, y, z}
                - min_translation_vector: smallest axis+depth to separate boxes

        Status: Stable (v1-alpha)
        Guarantee: Deterministic
        """
        payload = {
            "box_a": box_a,
            "box_b": box_b,
        }

        return self._http.post(
            "/api/v1/physics/collision",
            json=payload,
        )

    def resistance(
        self,
        velocity: float,
        drag_coefficient: float,
        cross_sectional_area: float,
        fluid_density: float = 1.225,
    ) -> Response[dict]:
        """
        Calculate aerodynamic drag resistance force using:
        F_drag = 0.5 * rho * v² * Cd * A

        Args:
            velocity: Object speed in m/s
            drag_coefficient: Cd value (e.g. 0.47 for sphere, 1.0 for flat plate)
            cross_sectional_area: Frontal area in m²
            fluid_density: Fluid density in kg/m³ (default: 1.225 = air at sea level)

        Returns:
            Response with drag_force in Newtons and echo of input parameters

        Status: Stable (v1-alpha)
        Guarantee: Deterministic
        """
        payload = {
            "velocity": velocity,
            "drag_coefficient": drag_coefficient,
            "cross_sectional_area": cross_sectional_area,
            "fluid_density": fluid_density,
        }

        return self._http.post(
            "/api/v1/physics/resistance",
            json=payload,
        )

    def leverage(
        self,
        arm_length: float,
        angle_degrees: float,
        load_mass: float,
        pivot_torque_limit: float,
    ) -> Response[dict]:
        """
        Calculate mechanical leverage and torque at a specific joint.

        Args:
            arm_length: Length of the arm in meters.
            angle_degrees: Angle of the arm in degrees (0 = horizontal).
            load_mass: Mass of the load in kg.
            pivot_torque_limit: Maximum torque limit of the joint in Nm.

        Returns:
            Response with torque_exerted, exceeds_limit, and mechanical_advantage.

        Status: Stable (v1-alpha)
        Guarantee: Deterministic
        """
        payload = {
            "arm_length": arm_length,
            "angle_degrees": angle_degrees,
            "load_mass": load_mass,
            "pivot_torque_limit": pivot_torque_limit,
        }

        return self._http.post(
            "/api/v1/physics/leverage",
            json=payload,
        )

    def collision_sphere(self, sphere_a: dict, sphere_b: dict) -> Response[dict]:
        """Check collision between two spheres."""
        payload = {"sphere_a": sphere_a, "sphere_b": sphere_b}
        return self._http.post("/api/v1/physics/collision/sphere", json=payload)

    def collision_obb(self, box_a: dict, box_b: dict) -> Response[dict]:
        """Check collision between two oriented bounding boxes (OBB)."""
        payload = {"box_a": box_a, "box_b": box_b}
        return self._http.post("/api/v1/physics/collision/obb", json=payload)

    def grip_requirement(self, load_mass: float, acceleration: float = 0.0, mu: float = 0.4, safety: float = 1.5) -> Response[dict]:
        """Calculate minimum grip force required to prevent slip."""
        payload = {
            "load_mass": load_mass,
            "acceleration_m_s2": acceleration,
            "friction_mu": mu,
            "safety_factor": safety
        }
        return self._http.post("/api/v1/physics/grip-requirement", json=payload)

    def stability_composite(self, shapes: list[dict]) -> Response[dict]:
        """Evaluate stability of a composite object assembly."""
        payload = {"shapes": shapes}
        return self._http.post("/api/v1/physics/stability/composite", json=payload)
