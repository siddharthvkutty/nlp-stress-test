from models.model_loader import BaseTransformerModel

class DistilBERTModel(BaseTransformerModel):
    def __init__(self):
        super().__init__(
            model_name="textattack/distilbert-base-uncased-imdb"
        )