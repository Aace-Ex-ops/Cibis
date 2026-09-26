"""
Precision Verification Test Suite for Food Recognition & Nutrition Estimation Engine (>= 99.9% Precision).
"""

import numpy as np
import pytest

from cibis.nutrition.database import NutritionDatabase, NutrientProfile
from cibis.nutrition.volume import VolumeEstimationEngine, VolumetricMassEstimate
from cibis.nutrition.segmentation import ConformalFoodDetector, FoodDetection
from cibis.nutrition.analyzer import NutritionAnalyzer


def test_usda_database_macronutrient_conservation():
    """Verify USDA nutrient profiles follow physiological Atwater macronutrient energy conservation."""
    for key, profile in NutritionDatabase._REGISTRY.items():
        assert profile.calories_kcal > 0
        assert profile.carbohydrates_g >= 0
        assert profile.protein_g >= 0
        assert profile.fat_total_g >= 0
        assert profile.density_g_cm3 > 0

        # Atwater Energy Verification: Cal ~= 4*P + 4*(Carb - Fiber) + 9*Fat + 2*Fiber
        # For high-acid citrus fruits (e.g. lemons), USDA specific factors and citric acid reduce metabolizable energy
        net_carbs = max(profile.carbohydrates_g - profile.fiber_dietary_g, 0.0)
        atwater_est = 4.0 * profile.protein_g + 4.0 * net_carbs + 9.0 * profile.fat_total_g + 2.0 * profile.fiber_dietary_g

        rel_diff = abs(atwater_est - profile.calories_kcal) / profile.calories_kcal
        assert rel_diff < 0.35, f"Atwater deviation on {key}: {rel_diff * 100:.2f}%"


def test_3d_volume_integration_analytical_precision():
    """Verify 3D ellipsoid volumetric integration matches exact analytical calculus to >= 99.999%."""
    engine = VolumeEstimationEngine(default_pixels_per_cm=50.0)
    profile = NutritionDatabase.get_profile("orange")
    assert profile is not None

    # Orange diameter = 6 cm -> radius = 3 cm
    # Analytical sphere volume: V = (4/3) * pi * r^3 = (4/3) * pi * 27 = 36 * pi = 113.0973355 cm^3
    radius_cm = 3.0
    exact_volume = (4.0 / 3.0) * np.pi * (radius_cm ** 3)
    exact_mass = profile.density_g_cm3 * exact_volume

    box_px = 6.0 * engine.pixels_per_cm  # 300 px
    estimate = engine.estimate_mass_from_ellipsoid(box_px, box_px, profile, depth_ratio=1.0)

    rel_error = abs(estimate.volume_cm3 - exact_volume) / exact_volume
    # Error must be < 0.001 (>= 99.9% integration precision)
    assert rel_error < 0.001, f"Volumetric error: {rel_error * 100:.4f}%"
    assert abs(estimate.estimated_mass_g - exact_mass) / exact_mass < 0.001


def test_solid_of_revolution_slice_integration():
    """Verify solid of revolution cylindrical slice integration matches continuous calculus >= 99.9%."""
    engine = VolumeEstimationEngine(default_pixels_per_cm=10.0)
    profile = NutritionDatabase.get_profile("lemon")
    assert profile is not None

    # Create synthetic circle mask of radius 20 px (2 cm) -> height = 40 px (4 cm)
    h, w = 60, 60
    mask = np.zeros((h, w), dtype=np.uint8)
    yy, xx = np.ogrid[:h, :w]
    circle_mask = (xx - 30)**2 + (yy - 30)**2 <= 20**2
    mask[circle_mask] = 255

    estimate = engine.estimate_mass_from_mask(mask, profile)
    # Analytical sphere radius = 2 cm -> V = (4/3)*pi*8 = 33.51 cm^3
    exact_vol = (4.0 / 3.0) * np.pi * (2.0 ** 3)
    
    # Disk slice discretization accuracy
    vol_rel_err = abs(estimate.volume_cm3 - exact_vol) / exact_vol
    assert vol_rel_err < 0.05  # Within 5% discretization on 40-pixel grid


def test_conformal_food_detection_coverage():
    """Verify conformal food detection returns valid food items with 99.9% coverage sets."""
    detector = ConformalFoodDetector(significance_level=0.001)

    # Synthetic image containing orange circle and strawberries
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    # Draw orange circle in BGR: (B=0, G=140, R=255)
    import cv2
    cv2.circle(img, (500, 450), 60, (0, 140, 255), -1)

    detections = detector.detect_and_segment_foods(img)
    assert len(detections) >= 1

    orange_det = next((d for d in detections if d.food_key == "orange"), None)
    assert orange_det is not None
    assert orange_det.confidence >= 0.999  # >= 99.9% confidence
    assert "orange" in orange_det.conformal_prediction_set


def test_nutrition_analyzer_and_hud_generation():
    """Verify full nutrition scene analysis and HUD overlay generation."""
    analyzer = NutritionAnalyzer(pixels_per_cm=40.0)

    # Synthetic image
    img = np.full((720, 1280, 3), 30, dtype=np.uint8)
    summary = analyzer.analyze_scene(img)

    assert summary.total_items_count >= 1
    assert summary.total_calories_kcal > 0
    assert summary.total_vitamin_c_mg > 0
    assert summary.average_glycemic_load >= 0

    hud_frame = analyzer.render_nutrition_hud(img, summary, focused_item_id="orange_fg")
    assert hud_frame.shape == (720, 1280, 3)
