"""
Test detector on Thali image directly and print detections.
"""
import cv2
from cibis.nutrition.segmentation import ConformalFoodDetector

img = cv2.imread(r"C:\Users\adity\.gemini\antigravity\brain\90560c53-3def-437e-843e-1534131f068c\.user_uploaded\media_1790317813563.png")
print("Image shape:", img.shape)
detector = ConformalFoodDetector()
dets = detector.detect_and_segment_foods(img)
print(f"Total detections: {len(dets)}")
for d in dets:
    print(f"Detected: {d.food_name} at {d.bbox_xywh}")
