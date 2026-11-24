"""A small color-heuristic detector for the demo's supported produce categories.

This is not a trained recognition model. Results are candidates for user review.
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple
import cv2
import numpy as np
from cibis.nutrition.database import NutritionDatabase, NutrientProfile

@dataclass
class FoodDetection:
    item_id: str
    food_key: str
    food_name: str
    confidence: float
    bbox_xywh: Tuple[int, int, int, int]
    conformal_prediction_set: List[str]
    profile: NutrientProfile
    mask: Optional[np.ndarray] = None

class ConformalFoodDetector:
    """Detect orange-colored regions only; other foods are reported as unsupported."""
    def __init__(self, significance_level: float = 0.05):
        self.alpha = significance_level

    def detect_and_segment_foods(self, image: np.ndarray) -> List[FoodDetection]:
        if image is None or image.size == 0 or len(image.shape) != 3 or image.shape[2] != 3:
            return []
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([5, 100, 80]), np.array([28, 255, 255]))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        profile = NutritionDatabase.get_profile("orange")
        if not profile:
            return []
        found = []
        for i, contour in enumerate(sorted(contours, key=cv2.contourArea, reverse=True)):
            if cv2.contourArea(contour) < max(400, image.shape[0] * image.shape[1] * 0.001):
                continue
            x, y, w, h = cv2.boundingRect(contour)
            found.append(FoodDetection(f"orange_{i+1}", "orange", profile.food_name,
                0.35, (x, y, w, h), ["orange (color heuristic; unverified)"], profile, mask[y:y+h, x:x+w]))
        return found
