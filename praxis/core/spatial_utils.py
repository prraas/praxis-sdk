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

def _get_closest_point_on_segment(p: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> Tuple[float, float]:
    """Mathematical helper: find the point on segment AB closest to point P."""
    ax, ay = a
    bx, by = b
    px, py = p
    
    # Vector AB
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return a
        
    # Project P onto AB line: dot product t
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    
    # Clamp t to [0, 1] to stay on segment
    t = max(0.0, min(1.0, t))
    
    return (ax + t * dx, ay + t * dy)

def get_closest_navigable_point(current_pos: Tuple[float, float], surface_points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """ 
    Find the exact point on the perimeter of a navigable surface closest to the current position.
    Instead of just checking vertices, this checks every edge for high precision.
    """
    if not surface_points:
        return current_pos
        
    best_dist = float('inf')
    best_point = surface_points[0]
    
    n = len(surface_points)
    for i in range(n):
        p1 = surface_points[i]
        p2 = surface_points[(i + 1) % n]
        
        # Find closest point on this specific edge segment
        closest = _get_closest_point_on_segment(current_pos, p1, p2)
        
        dist = math.sqrt((current_pos[0] - closest[0])**2 + (current_pos[1] - closest[1])**2)
        if dist < best_dist:
            best_dist = dist
            best_point = closest
            
    return best_point
