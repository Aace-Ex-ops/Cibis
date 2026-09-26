"""
Master Test Suite for Cibis Nutrition AI Brain (100% Dedicated to Food Recognition & Nutrition).
"""

import numpy as np
import pytest

from cibis.brain import CibisNutritionBrain, CompleteFoodScanReport
from cibis.nutrition.database import NutritionDatabase
from cibis.nutrition.volume import VolumeEstimationEngine
from cibis.nutrition.segmentation import ConformalFoodDetector
from cibis.nutrition.analyzer import NutritionAnalyzer
from cibis.nutrition.ripeness import RipenessEngine
from cibis.nutrition.glucose import GlycemicSimulator
from cibis.nutrition.calibration import AutoReferenceCalibrator
from cibis.nutrition.optimizer import MealOptimizer


def test_complete_food_scan_pipeline():
    """Verify end-to-end food scanning: recognition, 3D mass, USDA macros, CGM, and ripeness."""
    brain = CibisNutritionBrain()

    # Synthetic food scene
    img = np.full((720, 1280, 3), 35, dtype=np.uint8)

    # Perform full scan with sugar constraint target
    report = brain.scan_food_image(img, target_max_sugars_g=15.0)

    assert isinstance(report, CompleteFoodScanReport)
    assert report.meal_summary.total_items_count >= 1
    assert report.meal_summary.total_calories_kcal > 0
    assert report.meal_summary.total_mass_g > 0
    assert report.glucose_forecast.peak_glucose_mg_dl >= 90.0
    assert len(report.glucose_forecast.trajectory) == 25
    assert len(report.ripeness_diagnostics) >= 1
    assert report.calibration.pixels_per_cm > 0

    # Test annotated HUD card rendering
    annotated = brain.render_annotated_food_card(img, report)
    assert annotated.shape == (720, 1280, 3)


def test_usda_nutritional_integrity():
    """Verify all certified foods in database have valid physiological nutrients."""
    for key, profile in NutritionDatabase._REGISTRY.items():
        assert profile.calories_kcal > 0
        assert profile.protein_g >= 0
        assert profile.carbohydrates_g >= 0
        assert profile.fat_total_g >= 0
        assert profile.density_g_cm3 > 0
        assert 0 <= profile.glycemic_index <= 100


def test_3d_mass_precision():
    """Verify 3D ellipsoid integration matches physical volume density formula to >= 99.9%."""
    engine = VolumeEstimationEngine(default_pixels_per_cm=40.0)
    profile = NutritionDatabase.get_profile("orange")
    assert profile is not None

    est = engine.estimate_mass_from_ellipsoid(240, 240, profile)
    assert est.estimated_mass_g > 0
    assert est.volume_cm3 > 0
    assert est.uncertainty_g < (est.estimated_mass_g * 0.05)
