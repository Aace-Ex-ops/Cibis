# Cibis

Cibis is an experimental food-image demo. The browser page includes a 3D-themed showcase and an upload endpoint. The current detector only finds orange-colored regions using HSV thresholds; it is not a trained food-recognition model. Nutrient values come from the bundled per-100 g lookup table, while portion mass depends on rough image geometry and cannot be trusted without a known scale and validated model.

## Run locally

Requires Python 3.10+ and the packages in `requirements.txt`.

```sh
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 and upload a JPG or PNG (maximum 12 MB). Images are processed in memory and are not saved by the web endpoint. The UI currently supports an experimental orange color heuristic; no match means the item is unsupported, not absent. Nutrition and mass estimates are illustrative and should not guide medical decisions.

`python scan.py path/to/image.jpg` runs the command-line report and writes `scanned_result.jpg` in the project folder.

## What is and is not validated

There is no trained detection model, labeled evaluation dataset, reference-scale calibration workflow, or clinical validation for the glucose simulation. Confidence, mass, ripeness, and glucose predictions must not be presented as measured accuracy. A reliable product needs a licensed food dataset, a trained and independently evaluated model, user-confirmed portions or a physical scale reference, sourced nutrient data with provenance, and validation for any health-related predictions.

The files under `tests/` cover internal/demo calculations; passing them would not establish real-world food recognition or nutrition accuracy. The browser showcase retains sample visual assets for illustration.
