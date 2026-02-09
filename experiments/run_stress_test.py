import json
import pandas as pd
from models.sentiment_models import load_models

MODELS = load_models()

with open("data/raw/stress_sentences.json") as f:
    stress_data = json.load(f)

rows = []

for category, sentences in stress_data.items():
    for text in sentences:
        for model_name, clf in MODELS.items():
            out = clf(text)[0]
            rows.append({
                "category": category,
                "text": text,
                "model": model_name,
                "label": out["label"],
                "confidence": out["score"]
            })

df = pd.DataFrame(rows)
df.to_csv("results/stress_results.csv", index=False)
print("Saved results to results/stress_results.csv")
