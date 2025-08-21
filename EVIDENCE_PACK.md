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

## 2) People Analytics — IBM HR (Attrition & KPIs)
**Dataset:** IBM HR Attrition CSV (Kaggle).  
**Focus:** Attrition %, by Department/JobRole; tenure banding; DQ checks; SQL↔Pandas parity.

**Headline KPIs (fill after running `hr_eda.ipynb`):**  
- Overall attrition %: **[TBD]**  
- Top 3 by attrition: **[Dept/Role + %]**  
- Tenure distribution: **[TBD]**

**Data quality checks:**  
- Nulls in Department/JobRole within threshold: **[TBD]**  
- Non-negative tenure; unique EmployeeNumber: **[TBD]**

**Links:**  
- Notebook: `people_analytics_hr/notebooks/hr_eda.ipynb`  
- SQL: `people_analytics_hr/sql/hr_basics.sql`  
- Metrics spec: `people_analytics_hr/docs/metrics_spec_people_analytics.md`

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
