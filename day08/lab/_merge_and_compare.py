"""
Merge all per-config scorecard CSVs and print full comparison.
No API calls.
"""
import csv
from pathlib import Path
from eval import compare_ab, RESULTS_DIR, _load_results_from_csv

configs = [
    "baseline_dense",
    "variant1_hybrid",
    "variant2_hybrid_nuanced",
    "variant3_nuanced_abstain",
    "variant4_hybrid_rerank",
]

results_by_label = {}
for label in configs:
    csv_path = RESULTS_DIR / f"scorecard_{label}.csv"
    if csv_path.exists():
        data = _load_results_from_csv(csv_path)
        results_by_label.update(data)
        print(f"Loaded {len(list(data.values())[0])} rows for {label}")
    else:
        print(f"WARNING: missing {csv_path.name} — run: python eval.py --run {label.split('_')[0]}{label.split('_')[1] if len(label.split('_')) > 1 else ''}")

compare_ab(results_by_label, output_csv="ab_comparison_final.csv")
