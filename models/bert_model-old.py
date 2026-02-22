# models/bert_model.py

from models.model_loader import BaseTransformerModel


class BERTModel(BaseTransformerModel):
    def __init__(self, num_labels: int = 2):
        super().__init__(
            model_name="bert-base-uncased",
            num_labels=num_labels
        )