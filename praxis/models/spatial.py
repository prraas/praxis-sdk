from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class Point:
    x: float
    y: float

@dataclass
class SegmentedObject:
    """Represents a single segmented object with spatial metadata."""
    id: int
    label: str
    role: str
    confidence: float
    points: List[Tuple[float, float]]

    @property
    def centroid(self) -> Tuple[float, float]:
        """Calculate the geometric center of the polygon."""
        if not self.points:
            return (0.0, 0.0)
        x_coords = [p[0] for p in self.points]
        y_coords = [p[1] for p in self.points]
        return (sum(x_coords) / len(self.points), sum(y_coords) / len(self.points))

@dataclass
class SpatialInfo:
    """High-level spatial summary of a scene."""
    has_navigable_surface: bool
    obstacle_count: int

@dataclass
class SegmentationResult:
    """Complete result from a vision segmentation request."""
    model: str
    count: int
    objects: List[SegmentedObject]
    spatial_info: SpatialInfo
    processing_time_ms: Optional[float] = None
