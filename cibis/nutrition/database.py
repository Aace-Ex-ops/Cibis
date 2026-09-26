"""
USDA & ICMR/IFCT Certified Nutrition Matrix & Physical Density Database.
Expanded with Indian meal standards (Roti, Egg Curry, Spiced Meat/Sabzi, Kachumber Salad).
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class NutrientProfile:
    """Certified nutritional breakdown per 100g of edible food portion."""
    food_name: str
    calories_kcal: float        # kcal per 100g
    protein_g: float            # grams per 100g
    carbohydrates_g: float      # grams per 100g
    fat_total_g: float          # grams per 100g
    fiber_dietary_g: float      # grams per 100g
    sugars_g: float             # grams per 100g
    potassium_mg: float         # mg per 100g
    vitamin_c_mg: float         # mg per 100g
    calcium_mg: float           # mg per 100g
    density_g_cm3: float        # Physical bulk density in g/cm^3
    glycemic_index: int         # GI scale 0-100


class NutritionDatabase:
    """
    Certified ground-truth nutritional dictionary for precision nutrition calculation.
    Sources: USDA FoodData Central & ICMR-NIN Indian Food Composition Tables (IFCT).
    """

    _REGISTRY: Dict[str, NutrientProfile] = {
        # Indian Thali & Main Course Standards
        "roti": NutrientProfile(
            food_name="Whole Wheat Roti / Chapati (2 pieces)",
            calories_kcal=297.0,
            protein_g=9.30,
            carbohydrates_g=55.80,
            fat_total_g=3.70,
            fiber_dietary_g=9.60,
            sugars_g=1.20,
            potassium_mg=285.0,
            vitamin_c_mg=0.0,
            calcium_mg=45.0,
            density_g_cm3=0.72,
            glycemic_index=52,
        ),
        "egg_curry": NutrientProfile(
            food_name="Egg Masala / Boiled Egg Curry",
            calories_kcal=155.0,
            protein_g=11.20,
            carbohydrates_g=3.80,
            fat_total_g=10.50,
            fiber_dietary_g=1.10,
            sugars_g=2.10,
            potassium_mg=195.0,
            vitamin_c_mg=4.2,
            calcium_mg=56.0,
            density_g_cm3=1.04,
            glycemic_index=15,
        ),
        "spiced_meat_sabzi": NutrientProfile(
            food_name="Spiced Shredded Meat / Soya Bhurji",
            calories_kcal=185.0,
            protein_g=21.50,
            carbohydrates_g=4.50,
            fat_total_g=9.20,
            fiber_dietary_g=1.80,
            sugars_g=1.50,
            potassium_mg=340.0,
            vitamin_c_mg=5.5,
            calcium_mg=38.0,
            density_g_cm3=0.92,
            glycemic_index=20,
        ),
        "cucumber_salad": NutrientProfile(
            food_name="Diced Cucumber & Onion Salad (Kachumber)",
            calories_kcal=18.0,
            protein_g=0.80,
            carbohydrates_g=3.60,
            fat_total_g=0.20,
            fiber_dietary_g=1.20,
            sugars_g=1.90,
            potassium_mg=160.0,
            vitamin_c_mg=7.8,
            calcium_mg=22.0,
            density_g_cm3=0.88,
            glycemic_index=15,
        ),
        # Produce Standards
        "orange": NutrientProfile(
            food_name="Mandarin / Clementine Orange",
            calories_kcal=47.0,
            protein_g=0.94,
            carbohydrates_g=11.75,
            fat_total_g=0.12,
            fiber_dietary_g=2.4,
            sugars_g=9.35,
            potassium_mg=181.0,
            vitamin_c_mg=53.2,
            calcium_mg=40.0,
            density_g_cm3=0.96,
            glycemic_index=43,
        ),
        "strawberry": NutrientProfile(
            food_name="Fresh Strawberries",
            calories_kcal=32.0,
            protein_g=0.67,
            carbohydrates_g=7.68,
            fat_total_g=0.30,
            fiber_dietary_g=2.0,
            sugars_g=4.89,
            potassium_mg=153.0,
            vitamin_c_mg=58.8,
            calcium_mg=16.0,
            density_g_cm3=0.88,
            glycemic_index=41,
        ),
        "green_grapes": NutrientProfile(
            food_name="Green Seedless Grapes",
            calories_kcal=69.0,
            protein_g=0.72,
            carbohydrates_g=18.10,
            fat_total_g=0.16,
            fiber_dietary_g=0.9,
            sugars_g=15.48,
            potassium_mg=191.0,
            vitamin_c_mg=3.2,
            calcium_mg=10.0,
            density_g_cm3=0.98,
            glycemic_index=59,
        ),
        "red_apple": NutrientProfile(
            food_name="Red Gala / Fuji Apple",
            calories_kcal=52.0,
            protein_g=0.26,
            carbohydrates_g=13.81,
            fat_total_g=0.17,
            fiber_dietary_g=2.4,
            sugars_g=10.39,
            potassium_mg=107.0,
            vitamin_c_mg=4.6,
            calcium_mg=6.0,
            density_g_cm3=0.82,
            glycemic_index=36,
        ),
        "green_apple": NutrientProfile(
            food_name="Granny Smith Green Apple",
            calories_kcal=58.0,
            protein_g=0.44,
            carbohydrates_g=13.61,
            fat_total_g=0.19,
            fiber_dietary_g=2.8,
            sugars_g=9.59,
            potassium_mg=120.0,
            vitamin_c_mg=4.6,
            calcium_mg=5.0,
            density_g_cm3=0.84,
            glycemic_index=38,
        ),
        "yellow_pear": NutrientProfile(
            food_name="Yellow Bartlett Pear",
            calories_kcal=57.0,
            protein_g=0.36,
            carbohydrates_g=15.23,
            fat_total_g=0.14,
            fiber_dietary_g=3.1,
            sugars_g=9.75,
            potassium_mg=116.0,
            vitamin_c_mg=4.3,
            calcium_mg=9.0,
            density_g_cm3=0.93,
            glycemic_index=38,
        ),
        "lemon": NutrientProfile(
            food_name="Fresh Lemon",
            calories_kcal=29.0,
            protein_g=1.10,
            carbohydrates_g=9.32,
            fat_total_g=0.30,
            fiber_dietary_g=2.8,
            sugars_g=2.50,
            potassium_mg=138.0,
            vitamin_c_mg=53.0,
            calcium_mg=26.0,
            density_g_cm3=0.95,
            glycemic_index=20,
        ),
    }

    @classmethod
    def get_profile(cls, food_key: str) -> Optional[NutrientProfile]:
        clean_key = food_key.lower().strip().replace(" ", "_")
        return cls._REGISTRY.get(clean_key)

    @classmethod
    def list_foods(cls) -> Dict[str, str]:
        return {k: v.food_name for k, v in cls._REGISTRY.items()}
