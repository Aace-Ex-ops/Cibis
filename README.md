# Cibis

Cibis is an experimental food-image demo. The browser page includes a 3D-themed showcase and an upload endpoint. Upload predictions use the pretrained `nateraw/vit-base-food101` image classifier, which predicts one dish from Food-101's 101 categories for the whole image. It does not locate multiple foods or recognize every food. First use downloads the model weights from Hugging Face. See the model card for its dataset and reported evaluation: https://huggingface.co/nateraw/food.

## Run locally

Requires Python 3.10+ and the packages in `requirements.txt`.

```sh
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 and upload a JPG or PNG (maximum 12 MB). Images are processed in memory and are not saved by the web endpoint. The first scan downloads model weights and may take a few minutes; subsequent requests use the local cache. Prediction scores are not calibrated confidence. For the top predicted label, the app queries USDA FoodData Central and displays a possible match with macros per 100 g. Check the match; it is not verified against the photo and is not a portion total. USDA's `DEMO_KEY` is used by default with low rate limits; set `USDA_FDC_API_KEY` to your own key for regular use. A measured portion weight is needed to estimate macros for the serving. Nutrition, portion mass, ripeness, and glucose estimates remain unvalidated and should not guide medical decisions.

`python scan.py path/to/image.jpg` runs the command-line report and writes `scanned_result.jpg` in the project folder.

## What is and is not validated

There is no trained detection model, labeled evaluation dataset, reference-scale calibration workflow, or clinical validation for the glucose simulation. Confidence, mass, ripeness, and glucose predictions must not be presented as measured accuracy. A reliable product needs a licensed food dataset, a trained and independently evaluated model, user-confirmed portions or a physical scale reference, sourced nutrient data with provenance, and validation for any health-related predictions.

The files under `tests/` cover internal/demo calculations; passing them would not establish real-world food recognition or nutrition accuracy. The browser showcase retains sample visual assets for illustration.
