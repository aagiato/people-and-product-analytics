# People & Product Analytics — Portfolio

Actively building ML/AI skills via CMU MSBA + focused projects. This repo shows skills for three role families:

- **People Analytics** — workforce KPIs (attrition, hiring funnel, tenure), SQL⇄Pandas parity, data-quality checks
- **Product Analytics / Experiments** — SRM, effect sizes/95% CIs, guardrails, **CUPED**, funnels & retention
- **Model-Quality Ops (GenAI)** — evaluation signals, annotation/feedback workflows, pre/post-launch quality readouts

## Projects
1. **People Analytics (IBM HR)** → [`people_analytics_hr/`](people_analytics_hr/)
2. **A/B Test Readout (Cookie Cats)** → [`product_ab_cookiecats/`](product_ab_cookiecats/)
3. **Marketplace Funnel & Retention (Airbnb)** → [`marketplace_airbnb_funnel/`](marketplace_airbnb_funnel/)

## How to run
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
jupyter notebook
```
Then open a notebook in `notebooks/` and run cells top-to-bottom.
