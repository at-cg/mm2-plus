import re

def get_variant_count(file):
    with open(file) as f:
        for line in f:
            if line.startswith("SN"):
                if "number of records:" in line:
                    return int(line.split()[-1])
    return 0

tp = get_variant_count("out_dir/tp_stats.txt")
fp = get_variant_count("out_dir/fp_stats.txt")
fn = get_variant_count("out_dir/fn_stats.txt")

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1_score:.4f}")
