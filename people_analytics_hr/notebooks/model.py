# people_analytics_hr/notebooks/model.py
# End-to-end HR Attrition modeling with saved artifacts for portfolio

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, precision_recall_fscore_support,
    classification_report, confusion_matrix, ConfusionMatrixDisplay,
    precision_recall_curve, roc_curve, brier_score_loss
)
from sklearn.calibration import CalibrationDisplay

# ---------- Paths ----------
# model.py is in .../people_analytics_hr/notebooks
ROOT = Path(__file__).resolve().parents[1]            # .../people_analytics_hr
DATA = ROOT / "data"
DOCS = ROOT / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

csv_path = DATA / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
assert csv_path.exists(), f"CSV not found at: {csv_path}"

# ---------- Load & target ----------
df = pd.read_csv(csv_path)
df['Churn'] = (df['Attrition'] == 'Yes').astype(int)

drop_cols = [c for c in ['Attrition','EmployeeNumber','Over18','EmployeeCount','StandardHours'] if c in df.columns]
X = df.drop(columns=drop_cols + ['Churn'])
y = df['Churn']

# ---------- Split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# ---------- Preprocess ----------
num_cols = X_train.select_dtypes(include='number').columns.tolist()
cat_cols = [c for c in X_train.columns if c not in num_cols]

pre = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols),
    ('num', StandardScaler(), num_cols),
])

# ---------- Models ----------
logreg = Pipeline([
    ('pre', pre),
    ('clf', LogisticRegression(max_iter=2000, solver='lbfgs'))
])

rf = Pipeline([
    ('pre', pre),
    ('clf', RandomForestClassifier(n_estimators=300, random_state=42))
])

# ---------- Train ----------
logreg.fit(X_train, y_train)
rf.fit(X_train, y_train)

# ---------- Predict probs ----------
proba_lr = logreg.predict_proba(X_test)[:, 1]
proba_rf = rf.predict_proba(X_test)[:, 1]

# ---------- Threshold search (maximize F1 for LR) ----------
prec, rec, thr = precision_recall_curve(y_test, proba_lr)
f1 = (2*prec*rec) / (prec+rec + 1e-12)
best_idx = np.nanargmax(f1)
best_thr = thr[max(best_idx-1,0)] if best_idx < len(thr) else 0.5

def metrics_at_threshold(y_true, y_score, thr):
    y_pred = (y_score >= thr).astype(int)
    pr, rc, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary', zero_division=0)
    auc = roc_auc_score(y_true, y_score)
    cm = confusion_matrix(y_true, y_pred)
    brier = brier_score_loss(y_true, y_score)
    return dict(precision=pr, recall=rc, f1=f1, roc_auc=auc, brier=brier, cm=cm.tolist(), threshold=float(thr))

lr_stats = metrics_at_threshold(y_test, proba_lr, best_thr)
rf_stats = metrics_at_threshold(y_test, proba_rf, 0.5)

# ---------- Feature importance ----------
# For LogReg on OHE features: map coefficients back to feature names
ohe = logreg.named_steps['pre'].named_transformers_['cat']
ohe_names = ohe.get_feature_names_out(cat_cols).tolist()
feature_names = ohe_names + num_cols
coefs = logreg.named_steps['clf'].coef_[0]
feat_imp_lr = pd.DataFrame({'feature': feature_names, 'weight': coefs, 'abs_weight': np.abs(coefs)})
feat_imp_lr.sort_values('abs_weight', ascending=False).head(25).to_csv(DOCS / "top_features_logreg.csv", index=False)

# For RF: use feature_importances_ on processed matrix (approx by permutation would be better; keep simple)
# NOTE: Getting post-transform names for RF is non-trivial; we reuse feature_names above (same preprocessor)
try:
    rf_clf = rf.named_steps['clf']
    imp = getattr(rf_clf, "feature_importances_", None)
    if imp is not None and len(imp) == len(feature_names):
        pd.DataFrame({'feature': feature_names, 'importance': imp}).sort_values(
            'importance', ascending=False
        ).head(25).to_csv(DOCS / "top_features_rf.csv", index=False)
except Exception as e:
    print("RF importance skipped:", e)

# ---------- Plots ----------
# Confusion matrix (LR at best_thr)
y_pred_lr = (proba_lr >= best_thr).astype(int)
cm = confusion_matrix(y_test, y_pred_lr)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
fig_cm, ax_cm = plt.subplots()
disp.plot(ax=ax_cm)
ax_cm.set_title(f"Confusion Matrix (LogReg @ thr={best_thr:.3f})")
fig_cm.tight_layout()
fig_cm.savefig(DOCS / "confusion_matrix_lr.png", dpi=150)
plt.close(fig_cm)

# ROC curve (LR)
fpr, tpr, _ = roc_curve(y_test, proba_lr)
fig_roc, ax_roc = plt.subplots()
ax_roc.plot(fpr, tpr, label=f"LogReg (AUC={roc_auc_score(y_test, proba_lr):.3f})")
ax_roc.plot([0,1],[0,1],'--', label="Chance")
ax_roc.set_xlabel("FPR"); ax_roc.set_ylabel("TPR"); ax_roc.legend()
ax_roc.set_title("ROC Curve — Logistic Regression")
fig_roc.tight_layout()
fig_roc.savefig(DOCS / "roc_lr.png", dpi=150)
plt.close(fig_roc)

# Calibration curve (LR)
fig_cal, ax_cal = plt.subplots()
CalibrationDisplay.from_predictions(y_test, proba_lr, n_bins=10, ax=ax_cal)
ax_cal.set_title("Calibration — Logistic Regression")
fig_cal.tight_layout()
fig_cal.savefig(DOCS / "calibration_lr.png", dpi=150)
plt.close(fig_cal)

# ---------- Group fairness slices (quick view) ----------
def slice_metric(df_test, score, group_col, thr):
    out = []
    tmp = df_test[[group_col]].copy()
    tmp['y'] = y_test.values
    tmp['p'] = (score >= thr).astype(int)
    for g, sub in tmp.groupby(group_col):
        pr, rc, f1, _ = precision_recall_fscore_support(sub['y'], sub['p'], average='binary', zero_division=0)
        out.append({'group': str(g), 'precision': pr, 'recall': rc, 'f1': f1, 'count': int(len(sub))})
    return pd.DataFrame(out).sort_values('count', ascending=False)

df_test = X_test.copy()
# Try a few common cols if present:
slice_cols = [c for c in ['Gender','MaritalStatus','Department','JobRole'] if c in df_test.columns]
slices = {}
for col in slice_cols:
    slices[col] = slice_metric(df_test, proba_lr, col, best_thr)
    slices[col].to_csv(DOCS / f"slice_metrics_{col}.csv", index=False)

# ---------- Save metrics ----------
summary = {
    "dataset_rows": int(len(df)),
    "target_positive_rate": float(y.mean()),
    "logreg": lr_stats | {"threshold": best_thr},
    "random_forest": rf_stats,
    "top_features_logreg_csv": "top_features_logreg.csv",
    "artifacts": [
        "confusion_matrix_lr.png",
        "roc_lr.png",
        "calibration_lr.png",
        "top_features_logreg.csv",
    ] + [f"slice_metrics_{c}.csv" for c in slice_cols]
}
with open(DOCS / "metrics_attrition.json", "w") as f:
    json.dump(summary, f, indent=2)

print("✅ Done. Artifacts written to:", DOCS)
print(json.dumps(summary, indent=2))
