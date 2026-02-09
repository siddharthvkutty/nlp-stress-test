import pandas as pd

df = pd.read_csv("data/processed/normalized_results.csv")

# Model disagreement
disagreement = (
    df.groupby("text")["norm_label"]
      .nunique()
      .reset_index(name="unique_labels")
)

disagreement["disagreement"] = disagreement["unique_labels"] > 1
print("\nDisagreement per input:")
print(disagreement)

# Average confidence by category/model
conf_stats = (
    df.groupby(["category", "model"])["confidence"]
      .mean()
      .reset_index()
)

print("\nAverage confidence:")
print(conf_stats)
