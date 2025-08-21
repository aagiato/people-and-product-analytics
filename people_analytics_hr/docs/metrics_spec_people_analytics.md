# Metrics Spec — People Analytics

## Attrition %
- **Definition**: `Attrition='Yes'` / total employees
- **Grain**: employee-level snapshot
- **Edge cases**: missing department/job role excluded from by-dimension %s

## Data Quality
- Nulls in Department/JobRole <= threshold
- Tenure non-negative; EmployeeNumber unique

## SQL⇄Pandas Parity
- Save matching outputs for audit.
