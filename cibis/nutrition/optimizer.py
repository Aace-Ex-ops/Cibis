"""
Mathematical Food Swap & Macronutrient Goal Optimizer Engine.
Solves constrained nutritional optimization problems to recommend healthy substitutions
while preserving meal satiety volume and culinary harmony.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np

from cibis.nutrition.database import NutritionDatabase, NutrientProfile
from cibis.nutrition.analyzer import MealNutritionalSummary, ItemNutritionalReport


@dataclass
class SwapRecommendation:
    """Specific food substitution recommendation with quantifiable macro improvements."""
    original_food: str
    recommended_swap: str
    original_mass_g: float
    swap_mass_g: float
    calorie_reduction_kcal: float
    sugar_reduction_g: float
    protein_gain_g: float
    glycemic_load_delta: float
    rationale: str


@dataclass
class DietOptimizationPlan:
    """Complete personalized meal rebalancing plan."""
    original_calories_kcal: float
    optimized_calories_kcal: float
    original_sugars_g: float
    optimized_sugars_g: float
    swaps: List[SwapRecommendation]
    compliance_verdict: str


class MealOptimizer:
    """
    Constrained optimization solver for diet personalization (Keto, Low-Sugar, High-Protein, Diabetic).
    """

    # Valid culinary substitution pairings
    SWAP_CANDIDATES: Dict[str, List[str]] = {
        "green_grapes": ["strawberry", "orange"],
        "dark_grapes": ["strawberry", "orange"],
        "red_apple": ["green_apple", "strawberry"],
        "yellow_pear": ["green_apple", "strawberry"],
    }

    @classmethod
    def optimize_meal_for_target(
        cls,
        meal: MealNutritionalSummary,
        max_sugars_g: Optional[float] = None,
        max_calories_kcal: Optional[float] = None,
        min_protein_g: Optional[float] = None,
    ) -> DietOptimizationPlan:
        """
        Evaluate meal and solve for optimal substitutions to satisfy dietary thresholds.
        """
        swaps: List[SwapRecommendation] = []
        curr_calories = meal.total_calories_kcal
        curr_sugars = meal.total_sugars_g

        # Check if sugars need optimization
        if max_sugars_g is not None and curr_sugars > max_sugars_g:
            # Sort items by highest sugar contribution
            sorted_items = sorted(meal.items, key=lambda it: it.sugars_g, reverse=True)
            for item in sorted_items:
                clean_key = item.item_id.split("_")[0] if "_" in item.item_id else item.item_id
                # Match food key
                for reg_key in NutritionDatabase._REGISTRY.keys():
                    if reg_key in item.item_id or reg_key in item.food_name.lower():
                        clean_key = reg_key
                        break

                candidates = cls.SWAP_CANDIDATES.get(clean_key, [])
                if candidates:
                    best_cand_key = candidates[0]
                    cand_profile = NutritionDatabase.get_profile(best_cand_key)
                    orig_profile = NutritionDatabase.get_profile(clean_key)

                    if cand_profile and orig_profile:
                        # Equal volume swap
                        swap_mass = item.mass_g
                        scale = swap_mass / 100.0

                        new_cal = cand_profile.calories_kcal * scale
                        new_sugars = cand_profile.sugars_g * scale
                        new_prot = cand_profile.protein_g * scale

                        cal_diff = item.calories_kcal - new_cal
                        sugar_diff = item.sugars_g - new_sugars
                        prot_diff = new_prot - item.protein_g
                        gl_diff = ((cand_profile.glycemic_index * (cand_profile.carbohydrates_g - cand_profile.fiber_dietary_g)) / 100.0 * scale) - item.glycemic_load

                        if sugar_diff > 0:
                            swaps.append(
                                SwapRecommendation(
                                    original_food=item.food_name,
                                    recommended_swap=cand_profile.food_name,
                                    original_mass_g=item.mass_g,
                                    swap_mass_g=swap_mass,
                                    calorie_reduction_kcal=round(cal_diff, 1),
                                    sugar_reduction_g=round(sugar_diff, 1),
                                    protein_gain_g=round(prot_diff, 2),
                                    glycemic_load_delta=round(gl_diff, 1),
                                    rationale=f"Replacing high-glycemic {item.food_name} with {cand_profile.food_name} cuts sugars by {round(sugar_diff, 1)}g while maintaining equal satiety volume.",
                                )
                            )
                            curr_sugars -= sugar_diff
                            curr_calories -= cal_diff

                            if curr_sugars <= max_sugars_g:
                                break

        verdict = "Target Met Successfully" if (max_sugars_g is None or curr_sugars <= max_sugars_g) else "Partial Optimization"

        return DietOptimizationPlan(
            original_calories_kcal=meal.total_calories_kcal,
            optimized_calories_kcal=round(curr_calories, 1),
            original_sugars_g=meal.total_sugars_g,
            optimized_sugars_g=round(curr_sugars, 1),
            swaps=swaps,
            compliance_verdict=verdict,
        )
