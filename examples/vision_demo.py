
import base64
import os
from praxis import Client

# Configuration
# Replace with your image path
IMAGE_PATH = "example.jpg"

def main():
    client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

    # Use existing example image if available
    image_path = "example.jpg"
    if not os.path.exists(image_path):
        # Fallback for demo: use a 1x1 black dot if image missing
        print(f"Warning: {image_path} not found. Using placeholder.")
        image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    else:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

    print("\n--- Phase 3: Object Detection (Analyze) ---")
    response = client.vision.analyze(image=image_data)
    if response.success:
        print(f"Detected: {response.data.get('count')} objects.")
    
    print("\n--- Phase 3: Spatial Mapping (Segment) ---")
    seg_response = client.vision.segment(image=image_data, model_tier="nano")
    if seg_response.success:
        data = seg_response.data
        print(f"Segmentation Complete. Found {data.get('count')} segments.")
        for obj in data.get("objects", []):
            label = obj['label']
            role = obj['role']
            print(f"• {label:<10} | Role: {role}")
        
        spatial = data.get("spatial_info", {})
        print(f"Navigable Surface: {'Detected' if spatial.get('has_navigable_surface') else 'Not Found'}")
    else:
        print(f"Error: {seg_response.data.get('error')}")

if __name__ == "__main__":
    main()
