# 🌊 Rising Waters — A Machine Learning Approach to Flood Prediction

> **Turning rainfall telemetry into instant, actionable flood-risk warnings.**

Rising Waters is an end-to-end machine learning web application that predicts regional flood risk from five key meteorological readings — cloud cover, annual rainfall, and seasonal rainfall blocks — using a trained XGBoost classifier served through a Flask backend and a custom-designed frontend.

---

## 📌 Table of Contents

1. [Overview](#-overview)
2. [Problem Statement](#-problem-statement)
3. [Key Features](#-key-features)
4. [Tech Stack](#-tech-stack)
5. [System Architecture](#-system-architecture)
6. [Project Structure](#-project-structure)
7. [Machine Learning Model](#-machine-learning-model)
8. [Getting Started](#-getting-started)
9. [Application Workflow](#-application-workflow)
10. [Routes Reference](#-routes-reference)
11. [Testing](#-testing)
12. [Deployment](#-deployment)
13. [Roadmap](#-roadmap)
14. [Acknowledgements](#-acknowledgements)
15. [License](#-license)

---

## 🌧 Overview

| | |
|---|---|
| **Project Name** | Rising Waters: A Machine Learning Approach to Flood Prediction |
| **Domain** | Artificial Intelligence & Machine Learning |
| **Type** | Full-stack ML web application |
| **Status** | ✅ Core pipeline complete · 🚧 Advanced roadmap in progress |
| **Developed By** | Nanda Gunasri |
| **Program** | APSCHE — Artificial Intelligence and Machine Learning (STB4) |
| **Trainer** | Adnan Saif |

Rising Waters takes raw regional rainfall data, trains a supervised classification model on it, and exposes that model through a clean, validated web interface — so that a non-technical user can enter a handful of numbers and immediately see a flood risk verdict with a confidence score, instead of a raw statistic.

---

## 🎯 Problem Statement

Floods are one of the most damaging and frequent natural disasters, yet many smaller regions and communities lack the infrastructure — physical gauge telemetry, dedicated forecasting teams, expensive monitoring hardware — to get an early warning before water levels rise. At the same time, historical rainfall data for most regions is often freely available but sits unused, because there is no simple tool that translates raw seasonal rainfall figures into a clear, actionable risk signal.

**Rising Waters bridges that gap**: it uses a lightweight, trained ML model to convert rainfall and cloud-cover readings into an instant flood-risk probability, deployable on ordinary web hosting with no specialized hardware.

---

## ✨ Key Features

- 🔮 **Instant ML-powered prediction** — an XGBoost classifier returns a flood-risk verdict and confidence percentage in milliseconds.
- 🖥️ **Clean, purpose-built UI** — a "Monsoon Gauge" design system with an animated SVG rain gauge, circular probability rings, and a distinct visual language for "flood likely" vs. "safe" outcomes.
- ✅ **Two-layer input validation** — client-side (JavaScript) and server-side (Python) checks ensure only realistic, well-formed values reach the model, with friendly error recovery instead of crashes.
- 📊 **Transparent results** — every prediction page recaps the exact inputs used, alongside the model's confidence score, so results are explainable rather than a black box.
- 📓 **Documented ML pipeline** — a Jupyter notebook captures the full exploratory data analysis and model comparison (Decision Tree, Random Forest, KNN, XGBoost) behind the final model choice.
- 📊 **Model Metrics**: Achieves **96.55% accuracy** on validation split, trained on the primary dataset.
- 🧩 **Modular, maintainable codebase** — configuration, validation, and prediction logic are separated from route handling for easier testing and extension.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Backend Framework** | Flask |
| **Machine Learning** | XGBoost, scikit-learn (StandardScaler) |
| **Data Handling** | Pandas, NumPy |
| **Model Persistence** | Joblib |
| **Frontend** | HTML5, custom CSS3 (no framework), Vanilla JavaScript |
| **Notebook / EDA** | Jupyter, Matplotlib, Seaborn |
| **Testing** | Python `unittest` |
| **Deployment** | Gunicorn, Render |

---

## 🏗 System Architecture

```
                 ┌─────────────────────┐
                 │   User's Browser    │
                 │  (home / form / UI) │
                 └──────────┬──────────┘
                            │  HTTP
                            ▼
                 ┌─────────────────────┐
                 │      Flask App      │
                 │       (app.py)      │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼───────────────┐
             ▼              ▼               ▼
      ┌────────────┐ ┌─────────────┐ ┌─────────────┐
      │ Validation │ │  Predictor  │ │  Templates  │
      │  (bounds)  │ │ (scale +    │ │ (home/index/│
      │            │ │  predict)   │ │ chance/no)  │
      └────────────┘ └──────┬──────┘ └─────────────┘
                            │
                 ┌──────────┴──────────┐
                 │   Saved Artifacts   │
                 │  models/floods.save │
                 │ models/transform.   │
                 │        save         │
                 └─────────────────────┘
```

**Flow:** rainfall inputs → client + server validation → StandardScaler transform → XGBoost inference → risk page render (`chance.html` or `nochance.html`).

---

## 📂 Project Structure

```
Rising-Waters/
│
├── core/                          # Backend business logic (separated from routes)
│   ├── config.py                  # Paths, directories, and input bound configuration
│   ├── predictor.py               # Model/scaler loading + prediction execution
│   └── validation.py              # Server-side input range validation
│
├── dataset/                        # Processed / training-ready data
│   └── flood_dataset.csv
│
├── models/                         # Saved ML artifacts (joblib)
│   ├── floods.save                 # Trained XGBoost classifier
│   └── transform.save              # Fitted StandardScaler
│
├── notebooks/                      # Exploratory data analysis & model training
│   └── Flood_Prediction.ipynb
│
├── raw_data/                       # Source historical datasets
│   └── rainfall in india 1901-2015.xlsx
│
├── static/                         # Frontend assets
│   ├── css/style.css               # Design system (Monsoon Gauge theme)
│   └── js/script.js                # Form validation & interactivity
│
├── templates/                      # Flask Jinja2 view templates
│   ├── home.html                   # Landing page
│   ├── index.html                  # Prediction input form
│   ├── chance.html                 # "Flood likely" result page
│   └── nochance.html               # "Safe" result page
│
├── tests/                          # Automated test suite
│   └── test_app.py
│
├── Project Documentation/          # Brainstorming, problem statements, empathy map, etc.
│
├── .env                            # Local environment variables
├── .gitignore
├── app.py                          # Flask application entry point
├── flood dataset.xlsx              # Primary training spreadsheet
├── Procfile                        # Production start command (Gunicorn)
├── render.yaml                     # Render deployment blueprint
├── requirements.txt
├── runtime.txt                     # Pinned Python version
├── train.py                        # Model training pipeline
└── Readme.md                       # You are here
```

---

## 🤖 Machine Learning Model

| Detail | Value |
|---|---|
| **Algorithm** | XGBoost Classifier (Gradient Boosted Trees) |
| **Alternatives evaluated** | Decision Tree, Random Forest, K-Nearest Neighbors |
| **Input Features** | Cloud Cover (%), Annual Rainfall (mm), Jan–Feb Rainfall (mm), March–May Rainfall (mm), June–September Rainfall (mm) |
| **Preprocessing** | StandardScaler feature scaling |
| **Target** | Binary flood classification (Flood / No Flood) |
| **Why XGBoost** | Strong performance on tabular data, built-in regularization to reduce overfitting, and fast inference suitable for real-time web use |

The model and scaler are trained via `train.py` (or the accompanying notebook) and persisted with `joblib` into `models/floods.save` and `models/transform.save`, which the Flask app loads at startup.

> Model performance figures depend on the dataset used for the most recent training run — see `notebooks/Flood_Prediction.ipynb` for the full evaluation (accuracy, confusion matrix, precision/recall) on the current model.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone or unzip the project
cd Rising-Waters

# Install dependencies
pip install -r requirements.txt
```

### Train the model

```bash
python train.py
```

This generates `models/floods.save` and `models/transform.save` from the data in `raw_data/` (or `flood dataset.xlsx`).

### Run the application

```bash
python app.py
```

Then open **http://127.0.0.1:5000/** in your browser.

---

## 🔄 Application Workflow

1. **Landing page** — the user arrives at the home page, which introduces the project and features an animated rain-gauge visual.
2. **Navigate to the form** — clicking **Predict Floods** opens the input form.
3. **Client-side validation** — `static/js/script.js` checks that all five fields are present, numeric, and within realistic bounds before submission.
4. **Submit** — the form sends a `POST` request to `/predict`.
5. **Server-side validation** — inputs are re-checked against defined bounds (e.g. Cloud Cover 0–100%) to prevent bad data from ever reaching the model.
6. **Preprocessing & inference** — the validated inputs are scaled with the saved `StandardScaler` and passed to the saved XGBoost model.
7. **Result page** — the user is routed to `chance.html` (flood risk detected) or `nochance.html` (low risk), each showing a probability gauge and a recap of the submitted values.

---

## 🔗 Routes Reference

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing / home page |
| `/predict` | GET/POST | GET renders form; POST validates inputs, runs model, renders results |
| `/Predict` | GET | Redirects legacy capitalized route to /predict |

---

## 🧪 Testing

The project includes an automated test suite (`tests/test_app.py`) covering:

- Route availability and correct template rendering
- Redirect / routing logic between form and result pages
- Boundary validation (empty fields, invalid strings, out-of-range values)
- Basic prediction pipeline sanity checks

Run tests with:

```bash
python -m unittest discover tests
```

---

## ☁️ Deployment

The project is configured to deploy on common Python-friendly hosts:

| Platform | Config File |
|---|---|
| **Render** | `render.yaml` |
| **Railway / Heroku** | `Procfile` |

Production runs are served via **Gunicorn** rather than the Flask development server, with the Python runtime pinned in `runtime.txt` for reproducible builds. Environment-specific values are kept in `.env` and excluded from version control via `.gitignore`.

---

## 🗺 Roadmap (In Future to do)

- [ ] **Live climatic data ingestion** from real-time APIs (e.g. NASA POWER, Copernicus)
- [ ] **Spatio-temporal modeling** — evolving from tabular XGBoost toward graph-based models that represent river basins and water flow
- [ ] **GIS-based hazard mapping** for live, color-coded regional risk visualization
- [ ] **SMS/email alerting** to notify at-risk users automatically

---

## 🙏 Acknowledgements

This project was developed by **Nanda Gunasri** under the guidance of **Adnan Saif (Trainer)**, as part of the **APSCHE — Artificial Intelligence and Machine Learning (STB4)** program.

Special thanks to the program mentors and reviewers for their guidance throughout the design, development, and evaluation of this project.

---

<p align="center"><i>Rising Waters — because early warning should not depend on how much a community can afford.</i></p>
