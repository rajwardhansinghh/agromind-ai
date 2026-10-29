# AgroMind AI — Submission and Viva Guide

Institution: IPS College, Indore  
Project title: AgroMind AI — Crop Recommendation System  
Student name / roll number / guide: Fill in your actual details before submission.

## Abstract

AgroMind AI is an educational crop recommendation application. It accepts soil nutrient values (nitrogen, phosphorus and potassium), temperature, relative humidity, soil pH and rainfall. A standardized, distance-weighted k-nearest-neighbours classifier compares inputs with a bundled dataset of 2,200 examples across 22 crop classes. Transparent demonstration rules incorporate state and growing season into candidate ranking. The interface displays recommendations, matching feature ranges, contextual warnings and a downloadable analysis. A deterministic 80/20 holdout evaluation classified 429 of 440 examples correctly (97.5%). This result is limited to the seven-feature classifier and does not establish real-world agricultural accuracy. The prototype runs locally using Python's standard library and a browser.

## Problem statement

Farmers need to consider multiple soil and environmental conditions when selecting a crop. This mini project demonstrates how labelled examples can support that comparison through an accessible web interface.

## Objectives

- Collect and validate soil and climate readings.
- Use a machine-learning classifier for crop selection.
- Explain the recommendation using dataset comparisons.
- Include location/season as clearly separated contextual rules.
- Provide reproducible evaluation and a reliable local demo.

## Architecture

Browser form → POST /api/recommend → validation → standardization → weighted k-NN → context adjustment → JSON response → recommendation cards.

Data: CSV → in-memory examples + feature means/scales. No database or API key is needed. The server does not persist form submissions. A report is saved only when the user downloads it.

## Algorithm in simple Hinglish

1. User apni soil aur climate ki values enter karta hai.
2. Har feature ko standardize karte hain: `(value - mean) / standard deviation`.
3. Isse bade number wale features distance par unnecessary dominance nahi karte.
4. User ki values se sab training examples ka Euclidean distance calculate hota hai.
5. Sabse paas ke 9 examples choose hote hain — ye neighbours hain.
6. Paas wale example ka vote zyada important hota hai: `1/(distance+0.01)`.
7. Crop-wise votes add hote hain, phir season/state demo rules ranking adjust karte hain.
8. Highest ranked crop screen par show hoti hai.

## Two-minute explanation

“Good morning. Our project is AgroMind AI, a crop recommendation system. It takes seven inputs: nitrogen, phosphorus, potassium, temperature, humidity, rainfall and soil pH. It also collects state, city and growing season. The machine-learning part uses standardized distance-weighted k-nearest neighbours. It finds nine similar examples from a dataset of 2,200 labelled records across 22 crops. Closer examples have more influence on the prediction. Season and state are transparent rule-based adjustments, while city is currently a context label. Our deterministic 80/20 evaluation gave 97.5% accuracy on 440 held-out records. That evaluates dataset classification, not farm outcomes. The interface shows the recommended crop, matching ranges and warnings. It runs offline with Python and a browser. Future work includes verified Indore-region data, crops such as wheat and soybean, proper unit verification and weather integration.”

## Demo checklist for tomorrow

1. Charge your laptop and extract the project before arriving.
2. Run `python app.py` from the project folder.
3. Open http://localhost:8000.
4. Click **Load rice demo**, then **Find my recommended crop**.
5. Explain rice, neighbour support, dataset ranges and context flags.
6. Change season to Rabi and submit: the rice season-mismatch warning demonstrates the context layer.
7. Download the JSON report.
8. Run `python -m unittest discover -s tests -v` to show tests.
9. Show README, `model.py`, dataset, and `models/metrics.json` in your GitHub repository.
10. Keep an extracted offline copy and your actual GitHub URL ready.

Do not describe the rice sample as a measured Indore farm reading. It is a labelled dataset example with an Indore context label for demonstration.

## Viva questions and short answers

**1. What is the project?** A supervised-learning prototype that recommends a crop from soil and climate inputs.

**2. Which algorithm is used?** Standardized, distance-weighted k-nearest neighbours with k=9.

**3. Why standardization?** To put feature values on comparable scales before Euclidean distance is computed.

**4. What is supervised learning?** Learning from examples where the input features and correct class label are available.

**5. What is the target?** The crop label; N, P, K, temperature, humidity, pH and rainfall are features.

**6. What is k?** The number of nearby examples considered for prediction. Here k=9 is fixed as a project design choice; it has not been selected by extensive tuning.

**7. Why not a neural network?** This small tabular prototype can use a simpler, interpretable classifier with fewer deployment requirements.

**8. Does k-NN train?** It stores labelled examples and fits preprocessing statistics. It is called a lazy learner because distance-based prediction happens when a query arrives.

**9. How was accuracy measured?** Deterministic stratified 80/20 holdout split: 429 correct out of 440 held-out records. Scaling uses only the 1,760 training examples.

**10. What is data leakage?** Letting test information influence model fitting; for example, fitting the scaler on all rows before the split.

**11. Is 97.5% real farm accuracy?** No. It is one dataset holdout classification result. Geographic, temporal and field validation are still needed.

**12. Is the displayed score confidence?** It is a context-adjusted ranking indicator, not a calibrated probability or harvest success rate.

**13. How does location work?** State can apply a small hand-authored preference bonus. City is displayed as context only. No live weather or geolocation is used.

**14. How does season work?** A hand-authored calendar applies a penalty when a seasonal candidate does not match the selected season. This layer is not learned or locally validated.

**15. Why might alternatives be missing?** All nine nearest examples may belong to a single crop class. The app does not invent other recommendations.

**16. Why no soybean or wheat?** They are absent from this 22-class dataset. Adding them requires verified labelled training data.

**17. Which technologies are used?** Python standard library, CSV, HTML, CSS, JavaScript Fetch API, JSON, unittest and Git.

**18. Is there a database?** No. The classifier reads the CSV into memory. This scope does not require persistent user records.

**19. What are the main limitations?** Dataset provenance/units, region coverage, no yield prediction, no field validation, and rule-based context.

**20. What would improve the project?** Verified local observations, consistent units, cross-validation, additional crops, model comparison and field testing.

## Honest contribution statement

The dataset comes from credited external sources. The interface and standard-library classifier in this package were prepared with AI assistance. Review the implementation and disclose assistance according to your college's rules. Do not claim original collection of these 2,200 observations.
