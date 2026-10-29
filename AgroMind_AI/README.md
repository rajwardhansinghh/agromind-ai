# AgroMind AI 🌱

**A crop recommendation mini project for IPS College, Indore.**

A Python web application that recommends crops from nitrogen, phosphorus, potassium, temperature, humidity, rainfall and soil pH. State and growing season apply transparent ranking adjustments; city is a context label, not a learned predictor.

## Run on Windows — no installation required beyond Python

1. Download and extract this repository.
2. Open the extracted project folder in VS Code.
3. Open **Terminal → New Terminal** and run:

```powershell
python app.py
```

If Windows does not recognize `python`, use `py app.py`.
Open **http://localhost:8000** in your browser. Keep the terminal open.
Use **Load rice demo**, then **Find my recommended crop**.
Press Ctrl+C to stop. If port 8000 is busy: `python app.py --port 8001`.

**Python 3.10 or newer. No pip packages, internet connection, weather account or API key is required to run the included project.** Do not open `index.html` directly: it needs the Python API.

## Features

- Responsive web interface, with local CSS and JavaScript.
- Standardized, distance-weighted k-nearest-neighbours classifier, k=9.
- 2,200 bundled dataset examples covering 22 crop classes.
- Top recommendation and up to two additional classes when present among the nine neighbours.
- Per-feature comparison with the predicted crop's dataset ranges.
- Input validation on both the browser and server.
- Kharif/Rabi/Zaid context and illustrative state preferences.
- Low-familiarity warning for inputs distant from training examples.
- Downloadable JSON analysis.
- Reproducible evaluation, API tests and GitHub Actions workflow.

## How prediction works

1. Validate seven numeric inputs and location/season selections.
2. Standardize each feature using training-set mean and population standard deviation.
3. Compute Euclidean distance from the standardized input to training examples.
4. Select the closest nine examples; vote with weight `1 / (distance + 0.01)`.
5. Normalize neighbour weights per crop.
6. Apply a `0.65` season-mismatch multiplier and a `1.08` illustrative state-preference multiplier.
7. Sort candidate crops and display the result with transparent context flags.

The adjusted ranking score is `100 × min(neighbour_share × season_factor × state_factor, 1)`. It is **not** a calibrated probability, yield estimate or percentage chance of a successful harvest. State and season preferences are hand-authored demonstration rules, not locally validated agricultural advice. Perennial crops do not receive a season penalty. City does not influence the score. No location-specific weather is fetched.

## Evaluation

```bash
python train.py
python -m unittest discover -s tests -v
```

The committed run uses a deterministic stratified 80/20 split, random seed 42: **1,760 training rows, 440 test rows, 429 correct, accuracy 97.5%**. Means and standard deviations are fitted only on the training subset. Full confusion matrix and dataset checksum are in `models/metrics.json`. These results evaluate the seven-feature classifier only; the context rules have not been evaluated. The local app fits on all 2,200 examples after evaluation, which is normal for the final demo model. No serialized binary model is required: k-NN is a lazy-learning algorithm.

## Supported classes

Apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean, muskmelon, orange, papaya, pigeonpeas, pomegranate, rice, watermelon.

**Wheat and soybean are not in the dataset** despite being important in Madhya Pradesh. The application does not claim to recommend every crop available around Indore.

## Dataset source, attribution and limits

The CSV is copied unchanged from the public [Harvestify repository](https://github.com/Gladiator07/Harvestify/blob/master/Data-processed/crop_recommendation.csv). Harvestify credits the [Crop Recommendation Dataset on Kaggle](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset). Credit to those dataset contributors; this project implements its own Python k-NN engine and web UI. The repository's GPL-3.0 license is preserved in `DATASET_LICENSE.txt`; this distribution uses GPL-3.0 as well. Original dataset licensing and collection methodology should be independently checked before further redistribution or commercial use.

**Unit limitation:** source headers do not establish nutrient units or rainfall aggregation period. N/P/K are therefore labelled dataset-scale readings; rainfall uses the conventional mm label but its time basis is unverified. Do not silently equate fertilizer dosage, laboratory mg/kg, and kg/ha. Proper unit harmonization is required before real deployment.

Data quality, sampling, geographic coverage and actual farm outcomes are not independently verified. This is an academic proof of concept. No production yield, profit, fertilizer dosage or field suitability claims are made.

## Project files

```text
app.py                        Local HTTP server and JSON API
model.py                      Input validation, classifier and context rules
train.py                      Reproducible holdout evaluation
static/                       Browser interface, CSS and JS
data/crop_recommendation.csv  Labelled dataset
models/metrics.json           Measured evaluation and confusion matrix
tests/test_app.py             Model and HTTP API tests
docs/SUBMISSION_AND_VIVA.md    Explanation, demo steps and viva answers
.github/workflows/tests.yml   Automatic tests on GitHub
```

## API

`GET /api/health` returns model status and dataset counts.

`POST /api/recommend` accepts:

```json
{"N":90,"P":42,"K":43,"temperature":20.88,"humidity":82,"ph":6.5,"rainfall":203,"state":"Madhya Pradesh","city":"Indore","season":"Kharif"}
```

Response includes `recommendations`, `warnings`, `model`, `location`, `season`, and a limitations notice. Unknown/missing/out-of-range values return HTTP 400. The server binds to localhost for a local demo; it is not a hardened public server.

## Put it on GitHub tonight

**Easiest:** create an empty repository named `agromind-ai` in your GitHub account. Click **Add file → Upload files** and upload all files and folders *inside* the extracted project folder, keeping their structure. Include the dataset. GitHub browser upload may omit hidden folders; use Git below to include the workflow.

**Using Git** (inside the extracted project folder):

```bash
git init
git add .
git commit -m "Build AgroMind AI crop recommendation system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agromind-ai.git
git push -u origin main
```

Replace `YOUR_USERNAME`. If Git asks for your identity, configure your actual name and email using `git config user.name` and `git config user.email`, then retry the commit. If a remote already exists, use `git remote set-url origin ...`. Share the resulting GitHub URL with your teacher. A ZIP or a local Git commit is not itself an online GitHub repository.

## Future work

Verified local datasets including wheat/soybean, properly defined input units, trained regional/season features, cross-validation, field validation, weather integration with consent, and richer model comparisons.
