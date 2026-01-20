
import base64
import os
from praxis import Client

# Configuration
# Replace with your image path
IMAGE_PATH = "example.jpg"

def main():
    client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

    if not os.path.exists(IMAGE_PATH):
        print(f"File not found: {IMAGE_PATH}")
        return

    # Load and Encode
    with open(IMAGE_PATH, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Execute Analysis
    response = client.vision.analyze(
        image=image_data,
        model="auto",
        min_confidence=0.5
    )

    # Output Results
    if response.success:
        data = response.data
        print(f"Analysis Complete ({data.get('processing_time_ms')}ms)")
        print(f"Objects Detected: {data.get('count')}")
        
        for obj in data.get("objects", []):
            label = obj['label']
            conf = obj['confidence']
            bbox = obj['bbox']
            print(f"• {label:<10} {conf:.1%} [x={bbox['x']:.0f}, y={bbox['y']:.0f}]")
    else:
        print(f"Error: {response.data.get('error')}")

if __name__ == "__main__":
    main()
