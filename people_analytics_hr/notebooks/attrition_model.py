# — 1) Imports & Load —
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report

# Load the dataset
p = Path("../data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
df = pd.read_csv(p)
print("Rows:", len(df))
print("Attrition distribution:\n", df['Attrition'].value_counts(normalize=True))

# — 2) Define X, y —
df['Churn'] = (df['Attrition'] == 'Yes').astype(int)
drop_cols = ['Attrition', 'EmployeeNumber', 'Over18', 'EmployeeCount', 'StandardHours']
X = df.drop(columns=[c for c in drop_cols if c in df.columns])
y = df['Churn']

# — 3) Split —
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# — 4) Preprocessing Pipeline —
num_cols = X.select_dtypes(include='number').columns.tolist()
cat_cols = [c for c in X.columns if c not in num_cols]
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("num", StandardScaler(), num_cols)
])

clf = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

# — 5) Train & Evaluate —
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]

print("ROC-AUC:", round(roc_auc_score(y_test, y_proba), 3))
print(classification_report(y_test, y_pred))

# — 6) Feature importance —
import numpy as np
features = preprocessor.named_transformers_['cat'].get_feature_names_out(cat_cols).tolist() + num_cols
coefs = clf.named_steps['classifier'].coef_[0]
top10 = pd.Series(np.abs(coefs), index=features).sort_values(ascending=False).head(10)
print("Top 10 predictors:\n", top10)
