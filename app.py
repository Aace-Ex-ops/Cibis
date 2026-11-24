"""Local upload-and-scan demo. Run with: python app.py"""
from flask import Flask, jsonify, request, send_from_directory
import cv2
import numpy as np
from cibis.brain import CibisNutritionBrain

app = Flask(__name__, static_folder=".", static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.post("/api/scan")
def scan():
    upload = request.files.get("image")
    if upload is None:
        return jsonify(error="Choose an image file."), 400
    raw = np.frombuffer(upload.read(), dtype=np.uint8)
    image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    if image is None:
        return jsonify(error="Could not decode that image."), 400
    report = CibisNutritionBrain().scan_food_image(image)
    summary = report.meal_summary
    return jsonify({
        "items": [{"name": i.food_name, "mass_g": i.mass_g, "calories_kcal": i.calories_kcal,
                   "protein_g": i.protein_g, "carbs_g": i.carbs_g, "confidence": 0.35}
                  for i in summary.items],
        "total_mass_g": summary.total_mass_g, "calories_kcal": summary.total_calories_kcal,
        "protein_g": summary.total_protein_g, "carbs_g": summary.total_carbs_g,
        "notice": "Experimental color-based estimate. No food model or scale reference is used; verify all results."
    })

@app.errorhandler(413)
def too_large(_):
    return jsonify(error="Image is too large (12 MB maximum)."), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
