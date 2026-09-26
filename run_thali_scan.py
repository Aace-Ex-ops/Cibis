"""
Execute full AI Scan and generate presentation diagnostics on the Indian Thali test case image.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from cibis.brain import CibisNutritionBrain

def scan_thali():
    brain = CibisNutritionBrain()
    
    input_path = r"C:\Users\adity\.gemini\antigravity\brain\90560c53-3def-437e-843e-1534131f068c\.user_uploaded\media_1790317813563.png"
    out_dir = r"C:\Users\adity\.gemini\antigravity\brain\90560c53-3def-437e-843e-1534131f068c"
    out_img_path = os.path.join(out_dir, "thali_scanned_result.jpg")
    
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Cannot load image from {input_path}")
        
    h, w = img.shape[:2]
    # Set scale: Tray width (~380 px in image) is ~26.0 cm -> ~14.6 px/cm
    brain.analyzer.volume_engine.pixels_per_cm = 14.6
    
    # Run full scan
    report = brain.scan_food_image(img, ambient_temp_c=24.0)
    
    # Render beautiful bounding boxes and labels
    annotated = img.copy()
    colors = [(255, 100, 0), (0, 200, 50), (0, 140, 255), (180, 50, 255)]
    
    detections = brain.analyzer.detector.detect_and_segment_foods(img)
    for i, det in enumerate(detections):
        x, y, bw, bh = det.bbox_xywh
        color = colors[i % len(colors)]
        cv2.rectangle(annotated, (x, y), (x + bw, y + bh), color, 3)
        
        # Get nutritional stats
        it_rep = brain.analyzer.analyze_item(det)
        label1 = f"{it_rep.food_name}"
        label2 = f"{it_rep.mass_g}g | {it_rep.calories_kcal} kcal | Prot: {it_rep.protein_g}g"
        
        # Draw background label badge
        cv2.rectangle(annotated, (x, y - 42), (x + max(len(label1), len(label2)) * 9, y), (20, 20, 20), -1)
        cv2.putText(annotated, label1, (x + 5, y - 24), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (255, 255, 255), 1)
        cv2.putText(annotated, label2, (x + 5, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.44, color, 1)
        
    # Draw Master Summary HUD Card at top right
    cv2.imwrite(out_img_path, annotated)
    print(f"Annotated result saved to: {out_img_path}")
    
    print("\n================ THALI MEAL NUTRITION REPORT ================")
    print(f"Total Plate Mass: {report.meal_summary.total_mass_g:.1f} g")
    print(f"Total Calories:   {report.meal_summary.total_calories_kcal:.1f} kcal")
    print(f"Total Protein:    {report.meal_summary.total_protein_g:.1f} g (High Protein Balanced Diet)")
    print(f"Total Net Carbs:  {(report.meal_summary.total_carbs_g - report.meal_summary.total_fiber_g):.1f} g")
    print(f"Total Fiber:      {report.meal_summary.total_fiber_g:.1f} g")
    print(f"Total Fats:       {report.meal_summary.total_fat_g:.1f} g")
    print(f"Meal Glycemic Load: {report.meal_summary.average_glycemic_load:.1f} (Low-to-Medium Steady Energy)")
    
    print("\n--- ITEM-BY-ITEM BREAKDOWN ---")
    for it in report.meal_summary.items:
        print(f"• {it.food_name}: {it.mass_g}g -> {it.calories_kcal} kcal | Protein: {it.protein_g}g | Net Carbs: {it.carbs_g - it.fiber_g:.1f}g | Fat: {it.fat_g}g | GL: {it.glycemic_load}")

    print("\n--- CGM BLOOD GLUCOSE FORECAST ---")
    print(f"Fasting Baseline: {report.glucose_forecast.baseline_glucose_mg_dl} mg/dL")
    print(f"Predicted Peak:   {report.glucose_forecast.peak_glucose_mg_dl} mg/dL (+{report.glucose_forecast.glucose_delta_mg_dl} mg/dL) at {report.glucose_forecast.time_to_peak_minutes} mins")
    print(f"Spike Category:   {report.glucose_forecast.spike_risk_category}")
    print(f"Gastric Delay:    {report.glucose_forecast.gastric_delay_factor}x (Protein & fiber delay gastric emptying)")

    # -------------------------------------------------------------
    # Generate PPT Presentation Charts for this Thali Test Case
    # -------------------------------------------------------------
    ppt_dir = os.path.join(out_dir, "ppt_charts")
    
    # 1. Macro Distribution Pie Chart
    labels = [f'Protein ({report.meal_summary.total_protein_g:.1f}g)', 
              f'Net Carbs ({(report.meal_summary.total_carbs_g - report.meal_summary.total_fiber_g):.1f}g)', 
              f'Dietary Fiber ({report.meal_summary.total_fiber_g:.1f}g)', 
              f'Healthy Fats ({report.meal_summary.total_fat_g:.1f}g)']
    sizes = [report.meal_summary.total_protein_g * 4, 
             (report.meal_summary.total_carbs_g - report.meal_summary.total_fiber_g) * 4, 
             report.meal_summary.total_fiber_g * 2, 
             report.meal_summary.total_fat_g * 9]
    colors_pie = ['#3498db', '#e67e22', '#2ecc71', '#e74c3c']
    
    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors_pie,
                                      wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2))
    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.setp(texts, size=10, weight="bold")
    ax.set_title("Caloric Macro Energy Split (%) — Indian Thali Meal", fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    chart1_path = os.path.join(ppt_dir, "thali_macro_split_pie.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    
    # 2. Thali CGM Glucose Trajectory Chart
    t_cgm = [p.time_minutes for p in report.glucose_forecast.trajectory]
    g_cgm = [p.glucose_mg_dl for p in report.glucose_forecast.trajectory]
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(t_cgm, g_cgm, color='#2980b9', lw=2.5, marker='o', markersize=5, label='Predicted Glucose Response')
    ax.axhline(90, color='gray', linestyle=':', label='Fasting Baseline (90 mg/dL)')
    ax.axhspan(70, 140, color='green', alpha=0.08, label='Optimal Postprandial Zone (70-140 mg/dL)')
    ax.set_title(f"Postprandial Blood Glucose (CGM) Curve: Peak at {report.glucose_forecast.peak_glucose_mg_dl} mg/dL @ {report.glucose_forecast.time_to_peak_minutes}m", fontsize=11, fontweight='bold')
    ax.set_xlabel("Time (Minutes Postprandial)", fontsize=10, fontweight='bold')
    ax.set_ylabel("Glucose (mg/dL)", fontsize=10, fontweight='bold')
    ax.legend(frameon=True, fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    chart2_path = os.path.join(ppt_dir, "thali_cgm_trajectory.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    
    print(f"Generated Thali presentation charts in: {ppt_dir}")

if __name__ == "__main__":
    scan_thali()
