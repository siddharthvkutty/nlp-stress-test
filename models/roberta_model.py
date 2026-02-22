from models.model_loader import BaseTransformerModel

class RoBERTaModel(BaseTransformerModel):
    def __init__(self):
        super().__init__(
            model_name="textattack/roberta-base-imdb"
        )