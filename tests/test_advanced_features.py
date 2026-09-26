"""
Test Suite for Advanced AI Nutrition Features: Ripeness, Glycemic CGM, Auto-Calibration, and Meal Optimizer.
"""

import numpy as np
import pytest

from cibis.nutrition.ripeness import RipenessEngine
from cibis.nutrition.glucose import GlycemicSimulator
from cibis.nutrition.calibration import AutoReferenceCalibrator
from cibis.nutrition.optimizer import MealOptimizer
from cibis.nutrition.analyzer import NutritionAnalyzer, MealNutritionalSummary, ItemNutritionalReport


def test_ripeness_and_brix_estimation():
    """Verify ripeness engine computes valid Brix sweetness and Arrhenius temperature decay."""
    crop = np.full((100, 100, 3), (0, 140, 255), dtype=np.uint8)
    report = RipenessEngine.analyze_fruit_ripeness(crop, "orange", ambient_temp_c=22.0)

    assert report.food_name == "Orange"
    assert report.estimated_brix_sweetness > 8.0
    assert report.days_shelf_life_remaining > 0
    assert 0.0 <= report.firmness_score <= 1.0


def test_glycemic_cgm_simulation():
    """Verify 120-minute postprandial glucose trajectory simulation and AUC integration."""
    analyzer = NutritionAnalyzer(pixels_per_cm=40.0)
    simulator = GlycemicSimulator(default_baseline_mg_dl=90.0)

    img = np.full((720, 1280, 3), 40, dtype=np.uint8)
    meal = analyzer.analyze_scene(img)

    forecast = simulator.simulate_glucose_curve(meal, baseline_glucose=90.0)

    assert forecast.baseline_glucose_mg_dl == 90.0
    assert forecast.peak_glucose_mg_dl >= forecast.baseline_glucose_mg_dl
    assert 15 <= forecast.time_to_peak_minutes <= 120
    assert len(forecast.trajectory) == 25
    assert forecast.auc_120_mg_dl_min >= 0


def test_auto_reference_calibration():
    """Verify auto-calibrator detects geometric references and produces valid pixels-per-cm scale."""
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    import cv2
    cv2.circle(img, (640, 360), 260, (200, 200, 200), 4)

    calib = AutoReferenceCalibrator.auto_calibrate_from_image(img, expected_reference="dinner_plate")
    assert calib.pixels_per_cm > 0
    assert calib.confidence >= 0.99


def test_meal_optimizer_food_swap():
    """Verify meal optimizer solves constrained sugar reduction while preserving volume."""
    # Construct a high-sugar meal with green grapes (300g -> ~46g sugar)
    grape_item = ItemNutritionalReport(
        item_id="green_grapes_cluster",
        food_name="Green Seedless Grapes",
        mass_g=300.0,
        uncertainty_g=3.6,
        calories_kcal=207.0,
        protein_g=2.16,
        carbs_g=54.3,
        fiber_g=2.7,
        sugars_g=46.44,
        fat_g=0.48,
        vitamin_c_mg=9.6,
        potassium_mg=573.0,
        calcium_mg=30.0,
        glycemic_load=30.4,
    )
    meal = MealNutritionalSummary(
        total_items_count=1,
        total_mass_g=300.0,
        total_calories_kcal=207.0,
        total_protein_g=2.16,
        total_carbs_g=54.3,
        total_fiber_g=2.7,
        total_sugars_g=46.44,
        total_fat_g=0.48,
        total_vitamin_c_mg=9.6,
        total_potassium_mg=573.0,
        total_calcium_mg=30.0,
        average_glycemic_load=30.4,
        items=[grape_item],
    )

    plan = MealOptimizer.optimize_meal_for_target(meal, max_sugars_g=20.0)

    assert plan.optimized_sugars_g < meal.total_sugars_g
    assert plan.optimized_calories_kcal < meal.total_calories_kcal
    assert len(plan.swaps) >= 1
    assert "strawberries" in plan.swaps[0].rationale.lower() or "orange" in plan.swaps[0].rationale.lower()
