from typing import List, Tuple
import math

def calculate_polygon_area(points: List[Tuple[float, float]]) -> float:
    """
    Calculate the area of a polygon using the Shoelace formula.
    Useful for determining if a navigable area is large enough for the robot.
    """
    if len(points) < 3:
        return 0.0
    
    area = 0.0
    for i in range(len(points)):
        j = (i + 1) % len(points)
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    
    return abs(area) / 2.0

def is_point_in_polygon(x: float, y: float, polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if a point (x, y) is inside a polygon using ray-casting algorithm.
    Used to verify if a robot's target coordinate is within a safe zone.
    """
    inside = False
    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def get_closest_navigable_point(current_pos: Tuple[float, float], surface_points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """ Find the point on the edge of a navigable surface closest to the current position."""
    best_dist = float('inf')
    best_point = surface_points[0]
    
    for px, py in surface_points:
        dist = math.sqrt((current_pos[0] - px)**2 + (current_pos[1] - py)**2)
        if dist < best_dist:
            best_dist = dist
            best_point = (px, py)
            
    return best_point
