"""
Cibis AI: Pure Food Recognition, 3D Volumetric Mass Estimation, and Precision Nutrition Intelligence.
"""

from cibis.nutrition.database import NutritionDatabase, NutrientProfile
from cibis.nutrition.volume import VolumeEstimationEngine, VolumetricMassEstimate
from cibis.nutrition.segmentation import ConformalFoodDetector, FoodDetection
from cibis.nutrition.analyzer import NutritionAnalyzer, ItemNutritionalReport, MealNutritionalSummary
from cibis.nutrition.ripeness import RipenessEngine, RipenessReport
from cibis.nutrition.glucose import GlycemicSimulator, GlycemicForecastReport, GlucoseCurvePoint
from cibis.nutrition.calibration import AutoReferenceCalibrator, CalibrationResult
from cibis.nutrition.optimizer import MealOptimizer, DietOptimizationPlan, SwapRecommendation
from cibis.brain import CibisNutritionBrain, CompleteFoodScanReport

__version__ = "1.0.0"
__all__ = [
    "NutritionDatabase",
    "NutrientProfile",
    "VolumeEstimationEngine",
    "VolumetricMassEstimate",
    "ConformalFoodDetector",
    "FoodDetection",
    "NutritionAnalyzer",
    "ItemNutritionalReport",
    "MealNutritionalSummary",
    "RipenessEngine",
    "RipenessReport",
    "GlycemicSimulator",
    "GlycemicForecastReport",
    "GlucoseCurvePoint",
    "AutoReferenceCalibrator",
    "CalibrationResult",
    "MealOptimizer",
    "DietOptimizationPlan",
    "SwapRecommendation",
    "CibisNutritionBrain",
    "CompleteFoodScanReport",
]
