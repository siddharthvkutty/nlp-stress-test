import torch
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

test_sentence = "Great product. Broke in two hours."

for name, clf in pipelines.items():
    print(name, clf(test_sentence))
