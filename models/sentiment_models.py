import torch
from transformers import pipeline

MODELS = {
    "DistilBERT": "distilbert-base-uncased-finetuned-sst-2-english",
    "BERT": "textattack/bert-base-uncased-SST-2",
    "RoBERTa": "cardiffnlp/twitter-roberta-base-sentiment-latest"
}

def load_models():
    device = 0 if torch.cuda.is_available() else -1
    return {
        name: pipeline("sentiment-analysis", model=ckpt, device=device)
        for name, ckpt in MODELS.items()
    }
