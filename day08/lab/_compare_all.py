"""
Load all per-config scorecard CSVs and run a full comparison.
No API calls needed — reads from existing saved results.
"""
import csv
from pathlib import Path
from eval import compare_ab, RESULTS_DIR, _load_results_from_csv

# Load the big CSV that has baseline + variant1 + variant2 + variant3
big_csv = RESULTS_DIR / "ab_comparison_all-2.csv"
results_by_label = _load_results_from_csv(big_csv)

# Load variant4 from its own scorecard CSV (saved separately)
v4_csv = RESULTS_DIR / "ab_comparison_variant4.csv"
if v4_csv.exists():
    v4 = _load_results_from_csv(v4_csv)
    results_by_label.update(v4)
else:
    print(f"variant4 CSV not found at {v4_csv}, trying scorecard md fallback...")

print("Configs loaded:", list(results_by_label.keys()))

# Keep only the configs we care about, in order
wanted = ["baseline_dense", "variant2_hybrid_nuanced", "variant3_nuanced_abstain", "variant4_hybrid_rerank"]
filtered = {k: results_by_label[k] for k in wanted if k in results_by_label}
missing = [k for k in wanted if k not in results_by_label]
if missing:
    print(f"WARNING: missing configs: {missing}")

compare_ab(filtered, output_csv="ab_comparison_final.csv")
