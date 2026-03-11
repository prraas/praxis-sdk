from praxis.core.http import HttpClient
from praxis.models.response import Response


class VisionAPI:
    """
    Vision API for analyzing real images.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def analyze(
        self,
        image: str,
        model: str = "auto",
        min_confidence: float = 0.5,
        max_objects: int = 20,
    ) -> Response[dict]:
        """
        Analyze an image for object detection.
        
        Args:
            image: Base64-encoded image data
            model: Detection model - "yolo", "simple", or "auto"
            min_confidence: Minimum confidence threshold (0.0-1.0)
            max_objects: Maximum number of objects to return
            
        Returns:
            Response with detected objects, confidence scores, and bounding boxes
        """
        payload = {
            "image": image,
            "model": model,
            "min_confidence": min_confidence,
            "max_objects": max_objects,
        }

        return self._http.post(
            "/api/v1/vision/analyze",
            json=payload,
        )

    def segment(
        self,
        image: str,
        model_tier: str = "nano",
        min_confidence: float = 0.5,
    ) -> Response[dict]:
        """
        Perform image segmentation to identify precise object shapes and spatial roles.

        Args:
            image: Base64-encoded image data
            model_tier: YOLO model tier ("nano" or "small")
            min_confidence: Minimum confidence threshold (0.0-1.0)

        Returns:
            Response with polygons, roles (e.g. navigable_surface), and spatial info.
        """
        payload = {
            "image": image,
            "model_tier": model_tier,
            "min_confidence": min_confidence,
        }

        return self._http.post(
            "/api/v1/vision/segment",
            json=payload,
        )
