🚀 **Live Demo:** [kredi-riski-analizi.streamlit.app](https://kredi-riski-analizi.streamlit.app)
# 🏦 End-to-End Credit Risk Modeling: Econometrics, ML, SHAP & Counterfactual Fairness

This project provides a comprehensive credit risk assessment pipeline using the UCI German Credit Dataset. It bridges classical econometric modeling with advanced machine learning techniques, explainable AI (XAI), algorithmic bias mitigation, and financial cost-sensitive evaluation.

## 📌 Executive Summary
- **Domain:** Credit Risk & Financial Inclusion
- **Core Methodology:** Classical Logit Baseline vs. XGBoost Classifier
- **Key Features:** Marginal Effects ($dY/dX$), Multicollinearity (VIF) Diagnostics, SHAP Interpretability, Counterfactual Fairness Testing, Sample Reweighing, and Cost-Sensitive Matrices.

---

## 🛠️ Project Architecture & Workflow

### 1. Econometric Foundation & Diagnostic Testing
- Tested for multicollinearity using **Variance Inflation Factor (VIF)** to ensure valid parameter estimation.
- Estimated a **Binary Logit Model** as a baseline to compute Odds Ratios and **Marginal Effects ($dY/dX$)** for direct economic interpretation.

### 2. Predictive Performance (XGBoost vs. Logit)
- Trained an XGBoost classifier to capture non-linearities and interactions.
- Evaluated models using **ROC-AUC** metrics and validated temporal/distributional stability via **Out-of-Time (OOT)** testing.

### 3. Explainable AI (XAI) with SHAP
- Computed **SHAP Summary Plots** to measure global feature importance across the portfolio.
- Generated **SHAP Waterfall Plots** to provide local, instance-level explanations for individual credit approval/rejection decisions.

### 4. Algorithmic Bias & Counterfactual Fairness
- Conducted **Demographic Parity** checks across age and demographic groups.
- Performed **Counterfactual Fairness Simulations**: Verified whether modifying sensitive attributes (e.g., age) while keeping financial attributes constant alters individual decisions.
- Applied **Sample Reweighing / Weight Adjustment** to mitigate algorithmic bias without compromising predictive accuracy.

### 5. Business & Financial Cost Matrix Evaluation
- Evaluated model predictions using a financial cost-benefit framework ($10,000 average loan size, 15% net profit margin):
  - **Type I Error (False Positive / Default Approved):** Principal Loss (-$10,000)
  - **Type II Error (False Negative / Good Rejected):** Opportunity Cost (-$1,500)
  - **True Negative (Good Approved):** Net Interest Income (+$1,500)

---

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/credit-risk-fairness-econometrics.git](https://github.com/your-username/credit-risk-fairness-econometrics.git)
