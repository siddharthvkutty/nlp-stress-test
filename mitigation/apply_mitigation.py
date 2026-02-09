import pandas as pd
from .ensemble import ensemble_vote
from .confidence_rejection import apply_confidence_rejection

# Load normalized results
df = pd.read_csv("data/processed/normalized_results.csv")

# ----------------------------
# 1. Ensemble Voting
# ----------------------------
ensemble_df = ensemble_vote(df)
ensemble_df.to_csv("results/ensemble_results.csv", index=False)

print("Saved ensemble results to results/ensemble_results.csv")

# ----------------------------
# 2. Confidence-Based Rejection
# ----------------------------
df["rejection_label"] = df.apply(
    apply_confidence_rejection,
    axis=1
)

df.to_csv("results/rejection_results.csv", index=False)

print("Saved confidence rejection results to results/rejection_results.csv")
