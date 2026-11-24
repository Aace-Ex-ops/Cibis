"""
Cibis Nutrition AI - One-Click Zero-Touch Diagnostic Scanner
Drop any image into the project folder and just run: python scan.py
"""

import os
import sys
import glob
import cv2
from cibis.brain import CibisNutritionBrain


def find_target_image(project_dir: str) -> str:
    """Auto-detect image from arguments, common names, or latest added file."""
    # 1. Command-line argument (e.g. python scan.py custom.jpg)
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        return sys.argv[1]

    # 2. Preferred default filenames in root
    preferred_names = ["input.jpg", "input.png", "input.jpeg", "food.jpg", "food.png", "test.jpg", "test.png"]
    for name in preferred_names:
        p = os.path.join(project_dir, name)
        if os.path.exists(p):
            return p

    # 3. Find newest image in project root (excluding output results)
    extensions = ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"]
    image_files = []
    for ext in extensions:
        for f in glob.glob(os.path.join(project_dir, ext)):
            base = os.path.basename(f).lower()
            if not base.startswith("scanned_") and not base.startswith("output_") and not base.startswith("cibis_"):
                image_files.append(f)

    if image_files:
        # Sort by latest modified time
        image_files.sort(key=os.path.getmtime, reverse=True)
        return image_files[0]

    raise FileNotFoundError(
        "No image found! Please drop any photo (e.g., 'input.jpg' or any .png/.jpg) into this folder and run again."
    )


def run_auto_scan():
    project_dir = os.path.abspath(os.path.dirname(__file__))
    
    try:
        input_image_path = find_target_image(project_dir)
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        return

    print("=" * 68)
    print("           CIBIS NUTRITION AI - LIVE DIAGNOSTIC SCANNER")
    print("=" * 68)
    print(f"[*] Processing Image: {os.path.basename(input_image_path)}")
    print("[*] Running Spatial Calibration, 3D Mass Integration & CGM Simulation...")

    img = cv2.imread(input_image_path)
    if img is None:
        print(f"[ERROR] Could not read image file: {input_image_path}")
        return

    # Initialize AI Brain and Scan
    brain = CibisNutritionBrain()
    report = brain.scan_food_image(img, ambient_temp_c=22.0, target_max_sugars_g=15.0)

    # Render HUD Card
    annotated = brain.render_annotated_food_card(img, report)
    out_path = os.path.join(project_dir, "scanned_result.jpg")
    cv2.imwrite(out_path, annotated)

    # 1. MEAL SUMMARY
    print("\n" + "-" * 28 + " 1. MEAL SUMMARY " + "-" * 28)
    print(f"• Total Recognized Items : {report.meal_summary.total_items_count}")
    print(f"• Rough estimated mass    : {report.meal_summary.total_mass_g:.1f} g (unvalidated; no scale reference)")
    print(f"• Total Calories          : {report.meal_summary.total_calories_kcal:.1f} kcal")
    print(f"• Protein / Total Fats    : {report.meal_summary.total_protein_g:.1f} g / {report.meal_summary.total_fat_g:.1f} g")
    print(f"• Net Carbs / Fiber       : {(report.meal_summary.total_carbs_g - report.meal_summary.total_fiber_g):.1f} g / {report.meal_summary.total_fiber_g:.1f} g")
    print(f"• Total Sugars            : {report.meal_summary.total_sugars_g:.1f} g")
    print(f"• Vitamin C               : {report.meal_summary.total_vitamin_c_mg:.1f} mg ({(report.meal_summary.total_vitamin_c_mg/90.0)*100:.0f}% DV)")
    print(f"• Average Glycemic Load   : {report.meal_summary.average_glycemic_load:.1f}")

    # 2. ITEM BREAKDOWN
    print("\n" + "-" * 27 + " 2. ITEM BREAKDOWN " + "-" * 27)
    for it in report.meal_summary.items:
        print(f"• {it.food_name:<26}: {it.mass_g:>5.1f}g -> {it.calories_kcal:>5.1f} kcal | Sugars: {it.sugars_g:>4.1f}g | GL: {it.glycemic_load:>4.1f}")

    # 3. 120-MIN BLOOD GLUCOSE FORECAST
    print("\n" + "-" * 22 + " 3. 120-MIN GLUCOSE (CGM) FORECAST " + "-" * 22)
    print(f"• Baseline Fasting Glucose: {report.glucose_forecast.baseline_glucose_mg_dl:.1f} mg/dL")
    print(f"• Predicted Peak Glucose  : {report.glucose_forecast.peak_glucose_mg_dl:.1f} mg/dL (+{report.glucose_forecast.glucose_delta_mg_dl:.1f} mg/dL) at {report.glucose_forecast.time_to_peak_minutes} mins")
    print(f"• Gastric Delay Factor    : {report.glucose_forecast.gastric_delay_factor:.2f}x (Modulated by Protein & Fiber)")
    print(f"• Spike Risk Category     : {report.glucose_forecast.spike_risk_category}")

    # 4. RIPENESS & SHELF-LIFE
    print("\n" + "-" * 24 + " 4. RIPENESS & SHELF-LIFE " + "-" * 24)
    for r in report.ripeness_diagnostics:
        print(f"• {r.food_name:<20}: {r.ripeness_stage:<28} | Sweetness: {r.estimated_brix_sweetness:>4.1f} °Bx | Shelf Life: {r.days_shelf_life_remaining:>4.1f} days")

    # 5. SMART FOOD SWAP OPTIMIZATION
    if report.optimization_plan and report.optimization_plan.swaps:
        print("\n" + "-" * 22 + " 5. SMART FOOD SWAP OPTIMIZATION " + "-" * 22)
        print(f"• Goal Target            : Sugar ≤ 15.0g (Original: {report.optimization_plan.original_sugars_g:.1f}g -> Optimized: {report.optimization_plan.optimized_sugars_g:.1f}g)")
        for s in report.optimization_plan.swaps:
            print(f"• Recommendation         : {s.rationale}")

    print("\n" + "=" * 68)
    print(f"[SUCCESS] Annotated HUD Result Saved to: scanned_result.jpg")
    print("=" * 68 + "\n")

if __name__ == "__main__":
    run_auto_scan()
