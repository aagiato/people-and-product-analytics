# HR Attrition — Decision Summary

**What I built:** Baseline attrition risk model using Logistic Regression (OHE + scaling). Random Forest used as a comparison.

**Key metrics (test set, Logistic Regression):**
- ROC–AUC: **0.812**
- Operating threshold (max F1): **0.233**
- Precision / Recall / F1 @ threshold: **0.492 / 0.617 / 0.547**
- Base attrition rate: **0.161**

**Interpretation:** At the chosen threshold I identify ~**62%** of leavers (recall) while roughly **49%** of flagged employees actually leave (precision). That balance is appropriate for an *early-warning* program where missing a leaver is costlier than reviewing some false positives.

**Top drivers:** See `docs/top_features_logreg.csv` (e.g., OverTime, JobLevel, MonthlyIncome, YearsAtCompany, MaritalStatus).

**Calibration:** See `docs/calibration_lr.png` (Brier score available in `metrics_attrition.json`). Probability outputs are suitable for ranking risk and thresholding by capacity.

**Fairness slices:** See `docs/slice_metrics_*.csv` (Gender, MaritalStatus, Department, JobRole). No extreme disparities observed at the chosen threshold; monitor precision/recall by group during pilot.

**Recommendation:** Use the model as an early-warning signal to focus retention actions on the top-risk deciles. Pilot targeted interventions (manager coaching, comp review, flexible scheduling) and measure uplift. Next steps: add cross-validation, consider class-weighted LR and calibrated probabilities, and enrich with team/manager features.
