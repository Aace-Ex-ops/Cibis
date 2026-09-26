import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_workflow_diagram():
    fig = plt.figure(figsize=(18, 12), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#0B0F19')
    fig.patch.set_facecolor('#0B0F19')

    # Title Banner
    ax.text(9, 11.4, "CIBIS NUTRITION AI — TECHNICAL PROCESS & WORKFLOW", 
            fontsize=20, fontweight='bold', color='#38BDF8', ha='center', va='center', fontfamily='sans-serif')
    ax.text(9, 10.95, "End-to-End Multimodal Perception, Geometric 3D Integration & Metabolic Forecasting Pipeline", 
            fontsize=12, color='#94A3B8', ha='center', va='center', fontfamily='sans-serif')

    phases = [
        {
            "num": "PHASE 01",
            "title": "Ingestion & Zero-Touch Calibration",
            "color": "#0284C7",
            "border": "#38BDF8",
            "x": 0.8, "y": 6.8, "w": 4.8, "h": 3.6,
            "items": [
                "• Input: Monocular Food Photo (RGB/BGR)",
                "• 9x9 Gaussian Filter Specular Smoothing",
                "• Hough Gradient Circle Transform",
                "• Tableware Inversion: (x-xc)² + (y-yc)² = R²",
                "• Pixels-per-cm Scale Factor: S_ppc = 2R / D_ref"
            ]
        },
        {
            "num": "PHASE 02",
            "title": "Conformal Instance Segmentation",
            "color": "#0D9488",
            "border": "#2DD4BF",
            "x": 6.6, "y": 6.8, "w": 4.8, "h": 3.6,
            "items": [
                "• BGR → HSV / CIELAB Color Space Mapping",
                "• Chromatic Masking & Contour Filtering",
                "• Split Conformal Prediction Calibration",
                "• Significance Level α = 0.001 (99.9% Coverage)",
                "• Guaranteed Candidate Class Set: C(X)"
            ]
        },
        {
            "num": "PHASE 03",
            "title": "3D Volumetric & Mass Integration",
            "color": "#D97706",
            "border": "#FBBF24",
            "x": 12.4, "y": 6.8, "w": 4.8, "h": 3.6,
            "items": [
                "• Triaxial Ellipsoid: V = (4/3)·π·a·b·c",
                "• Solids of Revolution Slicing: V = ∑ π·r²·dy",
                "• Ground-Truth Bulk Density Matrix (ρ g/cm³)",
                "• Exact Physical Mass: M = ρ · V (grams)",
                "• Analytical Uncertainty Bound: ±1.5%"
            ]
        },
        {
            "num": "PHASE 04",
            "title": "USDA Nutrient & Glycemic Synthesis",
            "color": "#4F46E5",
            "border": "#818CF8",
            "x": 0.8, "y": 1.6, "w": 4.8, "h": 3.6,
            "items": [
                "• FoodData Central (FDC) Per-100g Scaling",
                "• Macronutrients: Protein, Net Carbs, Fats, Fiber",
                "• Micronutrients: Vit C, Potassium, Calcium",
                "• Atwater Energy Conservation Check (4-4-9-2)",
                "• Glycemic Load: GL = (GI × Net Carbs) / 100"
            ]
        },
        {
            "num": "PHASE 05",
            "title": "Dynamic 120-min CGM & Ripeness",
            "color": "#E11D48",
            "border": "#FB7185",
            "x": 6.6, "y": 1.6, "w": 4.8, "h": 3.6,
            "items": [
                "• Gastric Delay: δ = 1 + 0.03·(P+F) + 0.5·Fiber",
                "• Dual-Exponential CGM: G(t) = G_base + A·(e^-kt - e^-at)",
                "• Trapezoidal AUC_120 Metabolic Exposure",
                "• Colorimetric Ripeness & °Brix Sweetness Index",
                "• Arrhenius Decay: Q10 = 2.0 Temperature Rule"
            ]
        },
        {
            "num": "PHASE 06",
            "title": "Meal Optimizer & Telemetry HUD",
            "color": "#7C3AED",
            "border": "#A78BFA",
            "x": 12.4, "y": 1.6, "w": 4.8, "h": 3.6,
            "items": [
                "• Target Threshold Evaluator (e.g. Sugar ≤ 15g)",
                "• Constrained Satiety-Preserving Swap Matrix",
                "• Calorie, Sugar, and ΔGL Improvement Metrics",
                "• Augmented Translucent HUD Card Alpha Blending",
                "• Annotated Bounding Boxes & Nutrition Overlay"
            ]
        }
    ]

    for p in phases:
        # Outer Card Box
        card = patches.FancyBboxPatch(
            (p['x'], p['y']), p['w'], p['h'],
            boxstyle="round,pad=0.2,rounding_size=0.25",
            linewidth=2, edgecolor=p['border'], facecolor='#131B2E', zorder=2
        )
        ax.add_patch(card)

        # Header Badge
        badge = patches.FancyBboxPatch(
            (p['x'] + 0.2, p['y'] + p['h'] - 0.55), 1.4, 0.45,
            boxstyle="round,pad=0.1,rounding_size=0.15",
            linewidth=0, facecolor=p['color'], zorder=3
        )
        ax.add_patch(badge)
        ax.text(p['x'] + 0.9, p['y'] + p['h'] - 0.32, p['num'],
                fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        # Title Text
        ax.text(p['x'] + 1.8, p['y'] + p['h'] - 0.32, p['title'],
                fontsize=11.5, fontweight='bold', color='#F8FAFC', ha='left', va='center', zorder=4)

        # Separator line
        ax.plot([p['x'] + 0.2, p['x'] + p['w'] - 0.2], [p['y'] + p['h'] - 0.75, p['y'] + p['h'] - 0.75],
                color='#334155', lw=1.2, zorder=3)

        # Bullet List Items
        curr_y = p['y'] + p['h'] - 1.2
        for item in p['items']:
            ax.text(p['x'] + 0.3, curr_y, item,
                    fontsize=9.5, color='#CBD5E1', ha='left', va='center', zorder=4, fontfamily='monospace')
            curr_y -= 0.52

    # Draw Connector Arrows
    # Top Row Arrows: Phase 1 -> Phase 2 -> Phase 3
    ax.annotate('', xy=(6.5, 8.6), xytext=(5.7, 8.6),
                arrowprops=dict(facecolor='#38BDF8', edgecolor='#38BDF8', width=2.5, headwidth=8), zorder=5)
    ax.annotate('', xy=(12.3, 8.6), xytext=(11.5, 8.6),
                arrowprops=dict(facecolor='#2DD4BF', edgecolor='#2DD4BF', width=2.5, headwidth=8), zorder=5)

    # Downward transition: Phase 3 -> Phase 4
    ax.annotate('', xy=(3.2, 5.3), xytext=(14.8, 6.7),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.35", color='#FBBF24', lw=2.5), zorder=5)

    # Bottom Row Arrows: Phase 4 -> Phase 5 -> Phase 6
    ax.annotate('', xy=(6.5, 3.4), xytext=(5.7, 3.4),
                arrowprops=dict(facecolor='#818CF8', edgecolor='#818CF8', width=2.5, headwidth=8), zorder=5)
    ax.annotate('', xy=(12.3, 3.4), xytext=(11.5, 3.4),
                arrowprops=dict(facecolor='#FB7185', edgecolor='#FB7185', width=2.5, headwidth=8), zorder=5)

    # Output Badge at Bottom
    out_badge = patches.FancyBboxPatch(
        (4.5, 0.4), 9.0, 0.65,
        boxstyle="round,pad=0.1,rounding_size=0.2",
        linewidth=1.5, edgecolor='#10B981', facecolor='#064E3B', zorder=2
    )
    ax.add_patch(out_badge)
    ax.text(9.0, 0.72, "RESULT: Fully Calibrated USDA Nutrition Telemetry + 120-Min CGM + Freshness + HUD Output",
            fontsize=10.5, fontweight='bold', color='#6EE7B7', ha='center', va='center', zorder=4)

    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    plt.tight_layout()

    out_path = r"C:\Users\adity\OneDrive\Desktop\cibis_technical_process_workflow.png"
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Workflow diagram successfully generated at: {out_path}")

if __name__ == "__main__":
    create_workflow_diagram()
