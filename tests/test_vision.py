from praxis import Client
import pytest

client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

def test_vision_analyze():
    """Test standard object detection."""
    # Using a dummy base64 string
    img_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    res = client.vision.analyze(image=img_b64)
    
    assert res.success is True
    assert "model" in res.data
    assert "objects" in res.data

def test_vision_segment():
    """Test instance segmentation."""
    img_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    res = client.vision.segment(image=img_b64)
    
    assert res.success is True
    assert "objects" in res.data
    # Segmentation should return polygon points
    if res.data["objects"]:
        assert "points" in res.data["objects"][0]
        assert "role" in res.data["objects"][0]
