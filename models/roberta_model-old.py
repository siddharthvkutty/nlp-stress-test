# models/roberta_model.py

from models.model_loader import BaseTransformerModel


class RoBERTaModel(BaseTransformerModel):
    def __init__(self, num_labels: int = 2):
        super().__init__(
            model_name="roberta-base",
            num_labels=num_labels
        )