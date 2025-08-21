# Evidence Pack — People & Product Analytics
_Last updated: 2025-08-21_ · Repo root: `people-and-product-analytics`

This one-pager summarizes results for quick screening (no setup required). Deep links to code & artifacts are included.

---

## 1) Product Analytics — Cookie Cats (A/B Test Readout)
**Dataset:** Kaggle “Cookie Cats” (mobile game A/B).  
**Primary metric:** 7-day retention (Bernoulli).  
**Guardrails:** SRM; basic health checks.

**SRM:** **Failed** — χ² = **6.902**, p = **0.0086** (A = **44,700**; B = **45,489**; ~+0.9 pp to B).  
**Effect (context only; not used for decision):**  
- Δ 7-day retention = **−0.0082**  
- 95% CI = **[−0.0133, −0.0031]**  
- **CUPED** Δ = **−0.0082** (95% CI **[−0.0130, −0.0034]**)

**Decision:** **Invalidate test (re-run)** — SRM failed, so allocation imbalance may bias effect estimates.

**Links:**  
- Notebooks (rendered): `product_ab_cookiecats/notebooks/`  
- Artifacts: `product_ab_cookiecats/docs/srm_counts.csv`, `srm_result.txt`, `effect_size_ci.txt`  
- Memo: `product_ab_cookiecats/docs/ab_decision_memo.md`

---

## 2) People Analytics — IBM HR (Attrition Model)
**Dataset:** IBM HR Attrition CSV (Kaggle).  
**Approach:** Logistic Regression baseline (OHE + scaling) with Random Forest comparison; fairness slice reports by Gender/MaritalStatus/Department/JobRole.

**Model results (test set — Logistic Regression):**  
- **AUC:** **0.812**  
- **Operating threshold (max F1):** **0.233**  
- **Precision / Recall / F1 @ thr:** **0.492 / 0.617 / 0.547**  
- **Base attrition rate:** **0.161**

**Drivers:** See `top_features_logreg.csv` (examples often include OverTime, JobLevel, MonthlyIncome, YearsAtCompany, MaritalStatus).  
**Fairness slices:** `slice_metrics_Gender.csv`, `slice_metrics_MaritalStatus.csv`, `slice_metrics_Department.csv`, `slice_metrics_JobRole.csv`.  
**Calibration:** `calibration_lr.png` (Brier in `metrics_attrition.json`).

**Links & Artifacts:**  
- Notebook / script: `people_analytics_hr/notebooks/model.py` (plus any `.ipynb`)  
- Artifacts: `people_analytics_hr/docs/roc_lr.png`, `confusion_matrix_lr.png`, `calibration_lr.png`, `top_features_logreg.csv`, `top_features_rf.csv`, `metrics_attrition.json`, `slice_metrics_*.csv`  
- Memo: `people_analytics_hr/docs/decision_memo.md`  
- (EDA & SQL, if desired): `people_analytics_hr/notebooks/hr_attrition_eda.ipynb`, `people_analytics_hr/sql/hr_basics.sql`

---

## 3) Marketplace — Airbnb (Funnel & Retention)
**Dataset:** Airbnb New User Bookings (Kaggle).  
**Focus:** signup → search → view → booking funnel; cohort retention.

**Funnel snapshot (fill after running):**  
- Signups: **[TBD]** · Searches: **[TBD]** · Views: **[TBD]** · Bookings: **[TBD]**

**Cohort retention (first 8 weeks):**  
- Week-1: **[TBD]%** · Week-4: **[TBD]%** · Notes: **[TBD]**

**Links:**  
- Notebook: `marketplace_airbnb_funnel/notebooks/retention_cohorts.ipynb`  
- SQL: `marketplace_airbnb_funnel/sql/marketplace_funnel.sql`  
- Metrics spec: `marketplace_airbnb_funnel/docs/metrics_spec_marketplace.md`

---

### Tooling snapshot
**Python/Pandas**, **SQL (CTEs/windows)**, **DuckDB**, **scikit-learn**, **Jupyter**. All raw datasets are local-only (not committed); notebooks render outputs on GitHub; small result artifacts live under each project’s `docs/`.
