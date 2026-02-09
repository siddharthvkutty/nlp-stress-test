import json
import torch
import pandas as pd
from transformers import pipeline

MODELS = {
    "DistilBERT": "distilbert-base-uncased-finetuned-sst-2-english",
    "BERT": "textattack/bert-base-uncased-SST-2",
    "RoBERTa": "cardiffnlp/twitter-roberta-base-sentiment-latest"
}

device = 0 if torch.cuda.is_available() else -1

pipelines = {
    name: pipeline("sentiment-analysis", model=ckpt, device=device)
    for name, ckpt in MODELS.items()
}

with open("data/stress_sentences.json") as f:
    stress_data = json.load(f)

rows = []

for category, sentences in stress_data.items():
    for text in sentences:
        for model_name, clf in pipelines.items():
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
print(df)
