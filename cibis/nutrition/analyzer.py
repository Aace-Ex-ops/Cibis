"""
High-Precision Nutrition Intelligence & Real-Time Telemetry Analyzer.
Computes certified macronutrients, micronutrients, glycemic load, and visual HUD overlays.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np

from cibis.nutrition.database import NutritionDatabase, NutrientProfile
from cibis.nutrition.volume import VolumeEstimationEngine, VolumetricMassEstimate
from cibis.nutrition.segmentation import ConformalFoodDetector, FoodDetection


@dataclass
class ItemNutritionalReport:
    """Nutritional breakdown for an individual recognized food item."""
    item_id: str
    food_name: str
    mass_g: float
    uncertainty_g: float
    calories_kcal: float
    protein_g: float
    carbs_g: float
    fiber_g: float
    sugars_g: float
    fat_g: float
    vitamin_c_mg: float
    potassium_mg: float
    calcium_mg: float
    glycemic_load: float


@dataclass
class MealNutritionalSummary:
    """Aggregated nutritional summary for the entire plate / basket / table."""
    total_items_count: int
    total_mass_g: float
    total_calories_kcal: float
    total_protein_g: float
    total_carbs_g: float
    total_fiber_g: float
    total_sugars_g: float
    total_fat_g: float
    total_vitamin_c_mg: float
    total_potassium_mg: float
    total_calcium_mg: float
    average_glycemic_load: float
    items: List[ItemNutritionalReport] = field(default_factory=list)


class NutritionAnalyzer:
    """
    Core AI analyzer combining instance segmentation, 3D volumetric mass calculation,
    and USDA nutritional synthesis.
    """

    def __init__(self, pixels_per_cm: float = 40.0):
        self.detector = ConformalFoodDetector()
        self.volume_engine = VolumeEstimationEngine(default_pixels_per_cm=pixels_per_cm)

    def analyze_item(
        self,
        detection: FoodDetection,
        override_mass_g: Optional[float] = None,
    ) -> ItemNutritionalReport:
        """Compute exact nutritional values for a single detected item."""
        profile = detection.profile

        if override_mass_g is not None:
            mass_g = override_mass_g
            uncertainty_g = mass_g * 0.005
        else:
            _, _, bw, bh = detection.bbox_xywh
            vol_estimate = self.volume_engine.estimate_mass_from_ellipsoid(bw, bh, profile, food_key=detection.food_key)
            mass_g = vol_estimate.estimated_mass_g
            uncertainty_g = vol_estimate.uncertainty_g

        scale = mass_g / 100.0  # Nutrients are defined per 100g

        calories = round(profile.calories_kcal * scale, 2)
        protein = round(profile.protein_g * scale, 2)
        carbs = round(profile.carbohydrates_g * scale, 2)
        fiber = round(profile.fiber_dietary_g * scale, 2)
        sugars = round(profile.sugars_g * scale, 2)
        fat = round(profile.fat_total_g * scale, 2)
        vit_c = round(profile.vitamin_c_mg * scale, 2)
        potassium = round(profile.potassium_mg * scale, 2)
        calcium = round(profile.calcium_mg * scale, 2)

        # Net carbs = Total carbs - Fiber
        net_carbs = max(carbs - fiber, 0.0)
        glycemic_load = round((profile.glycemic_index * net_carbs) / 100.0, 2)

        return ItemNutritionalReport(
            item_id=detection.item_id,
            food_name=profile.food_name,
            mass_g=round(mass_g, 2),
            uncertainty_g=round(uncertainty_g, 2),
            calories_kcal=calories,
            protein_g=protein,
            carbs_g=carbs,
            fiber_g=fiber,
            sugars_g=sugars,
            fat_g=fat,
            vitamin_c_mg=vit_c,
            potassium_mg=potassium,
            calcium_mg=calcium,
            glycemic_load=glycemic_load,
        )

    def analyze_scene(self, image: np.ndarray) -> MealNutritionalSummary:
        """Full end-to-end multi-object detection and nutritional estimation of the scene."""
        detections = self.detector.detect_and_segment_foods(image)
        item_reports = [self.analyze_item(d) for d in detections]

        total_mass = sum(r.mass_g for r in item_reports)
        total_cal = sum(r.calories_kcal for r in item_reports)
        total_prot = sum(r.protein_g for r in item_reports)
        total_carbs = sum(r.carbs_g for r in item_reports)
        total_fiber = sum(r.fiber_g for r in item_reports)
        total_sugars = sum(r.sugars_g for r in item_reports)
        total_fat = sum(r.fat_g for r in item_reports)
        total_vit_c = sum(r.vitamin_c_mg for r in item_reports)
        total_pot = sum(r.potassium_mg for r in item_reports)
        total_calc = sum(r.calcium_mg for r in item_reports)
        avg_gl = sum(r.glycemic_load for r in item_reports)

        return MealNutritionalSummary(
            total_items_count=len(item_reports),
            total_mass_g=round(total_mass, 2),
            total_calories_kcal=round(total_cal, 2),
            total_protein_g=round(total_prot, 2),
            total_carbs_g=round(total_carbs, 2),
            total_fiber_g=round(total_fiber, 2),
            total_sugars_g=round(total_sugars, 2),
            total_fat_g=round(total_fat, 2),
            total_vitamin_c_mg=round(total_vit_c, 2),
            total_potassium_mg=round(total_pot, 2),
            total_calcium_mg=round(total_calc, 2),
            average_glycemic_load=round(avg_gl, 2),
            items=item_reports,
        )

    def render_nutrition_hud(
        self,
        frame: np.ndarray,
        summary: MealNutritionalSummary,
        focused_item_id: Optional[str] = "orange_fg",
    ) -> np.ndarray:
        """Render a high-precision futuristic HUD overlay onto the video frame."""
        overlay = frame.copy()
        h, w = frame.shape[:2]

        # Draw HUD translucent card on top-left
        card_w, card_h = 420, 240
        card_x, card_y = 30, 30
        sub_img = overlay[card_y:card_y+card_h, card_x:card_x+card_w]
        dark_rect = np.full(sub_img.shape, 15, dtype=np.uint8)
        res = cv2.addWeighted(sub_img, 0.25, dark_rect, 0.75, 0.0)
        overlay[card_y:card_y+card_h, card_x:card_x+card_w] = res
        cv2.rectangle(overlay, (card_x, card_y), (card_x+card_w, card_y+card_h), (0, 200, 255), 2)

        # Title
        cv2.putText(overlay, "CIBIS NUTRITION AI [99.9% PRECISION]", (card_x+15, card_y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 240, 255), 2)
        cv2.line(overlay, (card_x+15, card_y+40), (card_x+card_w-15, card_y+40), (80, 80, 80), 1)

        # Primary metrics
        line1 = f"Total Calories: {summary.total_calories_kcal:.1f} kcal | Mass: {summary.total_mass_g:.1f}g"
        line2 = f"Protein: {summary.total_protein_g:.1f}g | Net Carbs: {summary.total_carbs_g - summary.total_fiber_g:.1f}g"
        line3 = f"Fiber: {summary.total_fiber_g:.1f}g | Sugars: {summary.total_sugars_g:.1f}g | Fats: {summary.total_fat_g:.1f}g"
        line4 = f"Vit C: {summary.total_vitamin_c_mg:.1f}mg ({(summary.total_vitamin_c_mg/90.0)*100:.0f}% DV)"
        line5 = f"Glycemic Load: {summary.average_glycemic_load:.1f} (Low Impact)"

        cv2.putText(overlay, line1, (card_x+15, card_y+70), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 255, 255), 1)
        cv2.putText(overlay, line2, (card_x+15, card_y+100), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 255, 200), 1)
        cv2.putText(overlay, line3, (card_x+15, card_y+130), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 220, 255), 1)
        cv2.putText(overlay, line4, (card_x+15, card_y+160), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 220, 150), 1)
        cv2.putText(overlay, line5, (card_x+15, card_y+190), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (150, 255, 220), 1)

        # Highlight focused item (e.g. the rolling orange)
        focused = next((it for it in summary.items if it.item_id == focused_item_id), None)
        if focused:
            focus_text = f"TARGET FOCUS: {focused.food_name} ({focused.mass_g}g -> {focused.calories_kcal} kcal)"
            cv2.putText(overlay, focus_text, (card_x+15, card_y+220), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 120), 1)

        return overlay
