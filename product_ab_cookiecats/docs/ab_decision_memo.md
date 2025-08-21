# Ship / Not-Ship Decision — Cookie Cats

**Decision:** **Invalidate test (re-run)**

**SRM:** **Failed** — χ² = 6.902, p = 0.0086 (A = 44,700; B = 45,489; ~+0.9 pp to B). Allocation imbalance invalidates this run.

**Primary metric (for context only; not for decision):**  
- Δ 7-day retention = −0.0082  
- 95% CI = [−0.0133, −0.0031]  
- CUPED Δ = −0.0082 (95% CI [−0.0130, −0.0034])

**Rationale:**  
Because **SRM failed**, the allocation is imbalanced and the effect estimate may be biased. We therefore **invalidate this run** and do not draw product conclusions.

**Next steps / mitigations:**  
1. Fix allocation/bucketing (stable hash key, 50/50 split).  
2. Verify identical eligibility/logging across variants.  
3. Run SRM diagnostics by **day**, **platform**, **geo** to locate the drift.  
4. **Re-run** test; proceed to effect estimation only if SRM **passes**.
