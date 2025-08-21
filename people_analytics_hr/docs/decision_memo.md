# HR Attrition — Decision Summary

**What I built:** Baseline attrition risk model using Logistic Regression (OHE + scaling). Random Forest as a comparison.

**Key metrics (test set):**
- ROC-AUC (LR): <fill from docs/metrics_attrition.json>
- Best threshold (F1): <thr>
- Precision/Recall/F1 @ thr: <P>/<R>/<F1>
- Base positive rate (attrition): <rate>

**Top drivers:** See `docs/top_features_logreg.csv` (e.g., OverTime, JobLevel, MonthlyIncome, YearsAtCompany, MaritalStatus).

**Calibration:** See `docs/calibration_lr.png` (Brier in `metrics_attrition.json`).

**Fairness slices:** See `docs/slice_metrics_*.csv` (Gender, MaritalStatus, Department, JobRole).

**Recommendation:** Use model as an early-warning signal (focus on top-decile risk). Pilot targeted interventions and measure uplift. Next: cross-validate, calibrate thresholds by org unit, and add team-level/manager features.
