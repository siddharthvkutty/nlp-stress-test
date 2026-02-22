# models/distilbert_model.py

from models.model_loader import BaseTransformerModel


class DistilBERTModel(BaseTransformerModel):
    def __init__(self, num_labels: int = 2):
        super().__init__(
            model_name="distilbert-base-uncased",
            num_labels=num_labels
        )