
import base64
import os
from praxis import Client

# Add image paths here
IMAGES = [
    "example.jpg"
]

def analyze_image(client, image_path):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    # Load and Encode
    with open(image_path, "rb") as f:
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
        print(f"Analyzed {image_path} ({data.get('processing_time_ms')}ms)")
        print(f"Objects: {data.get('count')}")
        
        for obj in data.get("objects", []):
            label = obj['label']
            conf = obj['confidence']
            bbox = obj['bbox']
            # Simple one-line output per object
            print(f"• {label:<10} {conf:.1%} [x={bbox['x']:.0f}, y={bbox['y']:.0f}]")
    else:
        print(f"Error: {response.data.get('error')}")
    print("-" * 40)

def main():
    # Initialize Production Client
    client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")
    
    for img in IMAGES:
        analyze_image(client, img)

if __name__ == "__main__":
    main()
