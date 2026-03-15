from praxis import Client
from praxis.core.spatial_utils import calculate_polygon_area, is_point_in_polygon

import base64
import os

def spatial_reasoning_demo():
    client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")
    
    # Path to real image
    image_path = "example.jpg"
    if not os.path.exists(image_path):
        # Using a valid base64 placeholder only for the initial variable assignment, 
        # but the logic will now rely strictly on API response.
        img_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    else:
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
    
    print("--- Robotics Spatial Reasoning Demo ---")
    
    # 1. Get Segmentation
    print("Step 1: Segmenting scene...")
    res = client.vision.segment(img_b64)
    
    if not res.success:
        print(f"FAILED: API Error: {res.data.get('error', 'Unknown Error')}")
        return

    # Find the floor
    objects = res.data.get("objects", [])
    floor = next((obj for obj in objects if obj.get("role") == "navigable_surface"), None)
    
    if floor and "points" in floor:
        floor_points = floor["points"]
        # 2. Calculate safe area
        area = calculate_polygon_area(floor_points)
        print(f"Step 2: Navigable area calculated as {area:.4f} normalized units.")
        
        # 3. Decision Making
        target_x, target_y = 0.5, 0.9
        print(f"Step 3: Checking if target ({target_x}, {target_y}) is safe for robot...")
        
        is_safe = is_point_in_polygon(target_x, target_y, floor_points)
        if is_safe:
            print(">>> STATUS: Target is within safe navigable surface. Proceeding.")
        else:
            print(">>> WARNING: Target is outside safe zone! Recalculating.")
    else:
        count = len(objects)
        print(f"No navigable surface detected among {count} objects.")
        print("Switching to obstacle avoidance mode.")

if __name__ == "__main__":
    spatial_reasoning_demo()
