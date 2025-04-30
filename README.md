# Predicting Chronic Diseases from Lifestyle and Mental Health Data

This project leverages AI and large-scale health survey data to predict chronic disease risk and deliver personalized healthcare advice. Built on the California Health Interview Survey (CHIS) 2023 dataset, it combines robust machine learning pipelines with an integrated large language model (LLM) for actionable recommendations.

---

## Project Goals

- **Predict** risk for five chronic diseases: hypertension, high cholesterol, diabetes, heart disease, and asthma.
- **Address** challenges including data leakage, high-dimensional features, mixed data types, and class imbalance.
- **Translate** predictions into user-friendly, actionable health advice using an LLM-powered system.

---

## Methodology Overview

### 🔹 Data Pipeline
- **Data Source**: CHIS 2023 (Mental Health, Health Behaviors, Demographics)
- **Cleaning**: Dropped incomplete responses, handled ordinal encodings
- **EDA**: Spearman correlation, chi-square tests, and leakage detection
- **Feature Engineering**: Statistical filtering, target encoding, domain-driven pruning
- **Resampling**: SMOTE applied on training set for minority class balancing

### 🔹 Modeling
- **Algorithms Explored**: Logistic Regression, KNN, CNN, Random Forest, XGBoost
- **Best Models**: Ensemble of Random Forest and XGBoost
- **Tuning**: Grid Search + Bayesian Optimization
- **Combining Models**: Blending and stacking strategies

### 🔹 Evaluation
- Metrics: Precision, Recall, F1-Score (focus on minority classes)
- Validation: Stratified k-fold cross-validation
- Interpretability: Feature importances via SHAP and partial dependence plots

---

## Data Product

### Predictive Dashboard
- Web-based interface accepts user input and provides disease risk predictions in real-time.

### Health Advisory System
- Uses a large language model to generate health advice based on predicted risks, aligned with clinical guidelines.

---

## Lessons Learned

- Avoid data leakage through rigorous domain filtering.
- Ensemble models outperform deep learning in sparse survey data.
- Interpretability is critical for healthcare adoption.
- Cross-disciplinary collaboration ensures clinical relevance.

---

## Technologies

- **Python**, **scikit-learn**, **XGBoost**, **pandas**, **SHAP**
- **SMOTE** for imbalanced classification
- **Large Language Model** (OpenAI/GPT-style) for health advisory generation
- **Flask/Streamlit** (if used) for dashboard deployment
