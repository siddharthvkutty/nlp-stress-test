import pandas as pd

df = pd.read_csv("results/stress_results.csv")

LABEL_MAP = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "POSITIVE",
    "negative": "NEGATIVE",
    "positive": "POSITIVE"
}

df["norm_label"] = df["label"].map(LABEL_MAP)
df["low_confidence"] = df["confidence"] < 0.65

df.to_csv("data/processed/normalized_results.csv", index=False)
print("Saved normalized results to data/processed/normalized_results.csv")
