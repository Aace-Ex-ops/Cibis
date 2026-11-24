"""Local upload-and-scan demo. Run with: python app.py"""
from flask import Flask, jsonify, request, send_from_directory
from PIL import Image, UnidentifiedImageError
import io
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

app = Flask(__name__, static_folder=".", static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024
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
    return jsonify({"predictions": predictions,
        "notice": "Food-101 classifier: predicts one dish for the whole image from 101 categories. Scores are model scores, not calibrated confidence. It does not detect multiple portions or estimate nutrition."})

@app.errorhandler(413)
def too_large(_):
    return jsonify(error="Image is too large (12 MB maximum)."), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
