# Ship / Not-Ship Decision — Cookie Cats

**Decision:** **Invalid (SRM failed) — re-run test**

**SRM:** χ² = 6.902, **p = 0.0086** (A = 44,700; B = 45,489). Allocation is imbalanced (~+0.9 pp to B). Because p < 0.05, we treat this run as **invalid** and do not draw product conclusions.

**Primary metric (for context only; do not use for decision):**  
- Δ 7-day retention = **−0.0082**  
- 95% CI = **[−0.0133, −0.0031]**  
- CUPED Δ = **−0.0082** (95% CI **[−0.0130, −0.0034]**)

**Rationale:**  
The sample-ratio mismatch (SRM) indicates the randomization/traffic split is off. With this imbalance, the observed negative effect may be **biased** by allocation or instrumentation issues. Even small imbalances can test significant at this scale, so we **invalidate** the run and recommend a clean re-randomized experiment.

**Next steps / mitigations:**  
1. **Fix allocation/bucketing:** verify consistent hash key, stable bucketing, and 50/50 split at source.  
2. **Check filtering & instrumentation:** confirm identical eligibility rules, event logging, and gate defaults across variants.  
3. **SRM diagnostics:** compute SRM by **day**, **platform/geo**, and **entry point** to locate when/where imbalance appears.  
4. **Re-run** the test and re-evaluate SRM before reading outcomes; proceed to effect estimation only if SRM passes.
