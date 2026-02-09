import pandas as pd
from collections import Counter

def ensemble_vote(df):
    """
    Performs majority voting over normalized labels.
    Returns a DataFrame with one row per input text.
    """

    results = []

    grouped = df.groupby("text")

    for text, group in grouped:
        labels = group["norm_label"].tolist()
        counts = Counter(labels)

        final_label, votes = counts.most_common(1)[0]
        agreement_ratio = votes / len(labels)

        results.append({
            "text": text,
            "ensemble_label": final_label,
            "vote_strength": agreement_ratio
        })

    return pd.DataFrame(results)
