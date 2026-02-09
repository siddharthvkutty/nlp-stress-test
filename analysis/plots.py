import pandas as pd
import matplotlib.pyplot as plt

# Load normalized data
df = pd.read_csv("data/processed/normalized_results.csv")

# ---------------------------------
# Add main category (for aggregation)
# ---------------------------------
df["main_category"] = df["category"].str.split("_").str[0]

# ---------------------------------
# Plot 1: Confidence distribution
# (MAIN CATEGORY – CLEAN VIEW)
# ---------------------------------
plt.figure(figsize=(8, 6))
df.boxplot(column="confidence", by="main_category")
plt.title("Confidence Distribution Across Linguistic Stressors")
plt.suptitle("")
plt.ylabel("Confidence")
plt.tight_layout()
plt.savefig("results/figures/confidence_boxplot.png")
plt.close()

# ---------------------------------
# Plot 2: Model disagreement
# (MAIN CATEGORY – CLEAN VIEW)
# ---------------------------------
disagreement = (
    df.groupby("text")["norm_label"]
      .nunique()
      .reset_index(name="unique_labels")
)

disagreement["disagreement"] = disagreement["unique_labels"] > 1

merged = df.merge(disagreement, on="text")

counts = (
    merged.groupby("main_category")["disagreement"]
          .sum()
          .reset_index()
)

plt.figure(figsize=(8, 6))
plt.bar(counts["main_category"], counts["disagreement"])
plt.title("Model Disagreement by Linguistic Stress Category")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("results/figures/disagreement_bar.png")
plt.close()

print("Saved clean, aggregated plots to results/figures/")
