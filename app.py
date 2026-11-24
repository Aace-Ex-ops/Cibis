"""Local upload-and-scan demo. Run with: python app.py"""
from flask import Flask, jsonify, request, send_from_directory
from PIL import Image, UnidentifiedImageError
import io
import os
from pathlib import Path
import requests
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

app = Flask(__name__, static_folder=".", static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024

# Read local secrets without a dotenv dependency. Existing process variables win.
for line in Path(".env").read_text().splitlines() if Path(".env").exists() else []:
    key, separator, value = line.partition("=")
    if separator and key.strip() and key.strip() not in os.environ:
        os.environ[key.strip()] = value.strip().strip('"').strip("'")
MODEL_ID = "nateraw/vit-base-food101"
_processor = None
_model = None

def classify_food(image):
    """Lazy-load Food-101 classifier and return its five best dish labels."""
    global _processor, _model
    if _processor is None:
        _processor = AutoImageProcessor.from_pretrained(MODEL_ID)
        _model = AutoModelForImageClassification.from_pretrained(MODEL_ID)
        _model.eval()
    inputs = _processor(images=image.convert("RGB"), return_tensors="pt")
    with torch.inference_mode():
        logits = _model(**inputs).logits[0]
        scores = torch.softmax(logits, dim=-1)
        values, indices = torch.topk(scores, k=5)
    return [{"name": _model.config.id2label[int(i)].replace("_", " "), "score": round(float(v), 4)}
            for v, i in zip(values, indices)]

def lookup_macros(food_label):
    """Find a USDA per-100g match; return None when data are unavailable."""
    api_key = os.environ.get("USDA_FDC_API_KEY", "DEMO_KEY")
    response = requests.post(
        f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}",
        json={"query": food_label, "dataType": ["Foundation", "SR Legacy", "Survey (FNDDS)"], "pageSize": 5},
        timeout=10,
    )
    response.raise_for_status()
    foods = response.json().get("foods", [])
    if not foods:
        return None
    food = foods[0]
    nutrients = {n.get("nutrientName", "").lower(): n.get("value") for n in food.get("foodNutrients", [])}
    def get(*names):
        return next((nutrients[n] for n in names if nutrients.get(n) is not None), None)
    macros = {"calories_kcal": get("energy", "energy (atwater general factors)"),
              "protein_g": get("protein"), "carbs_g": get("carbohydrate, by difference"),
              "fat_g": get("total lipid (fat)")}
    if all(v is None for v in macros.values()):
        return None
    return {"food_name": food.get("description", food_label), "fdc_id": food.get("fdcId"), "per_100g": macros}

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.post("/api/scan")
def scan():
    upload = request.files.get("image")
    if upload is None:
        return jsonify(error="Choose an image file."), 400
    raw = upload.read()
    try:
        image = Image.open(io.BytesIO(raw))
        image.verify()
        image = Image.open(io.BytesIO(raw))
    except (UnidentifiedImageError, OSError, AttributeError):
        return jsonify(error="Could not decode that image."), 400
    try:
        predictions = classify_food(image)
    except Exception as exc:
        app.logger.exception("Food classifier could not load or run")
        return jsonify(error=f"Food model unavailable: {type(exc).__name__}. Check internet access on first run."), 503
    macros = None
    try:
        macros = lookup_macros(predictions[0]["name"])
    except requests.RequestException:
        app.logger.warning("USDA FoodData Central lookup failed")
    return jsonify({"predictions": predictions, "macro_match": macros,
        "notice": "Food-101 predicts one dish for the whole image. Macro values, when found, are USDA values per 100 g for a possible text match, not measured values for your uploaded portion. Confirm the food and enter its weight for portion totals."})

@app.errorhandler(413)
def too_large(_):
    return jsonify(error="Image is too large (12 MB maximum)."), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
