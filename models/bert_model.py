from models.model_loader import BaseTransformerModel

class BERTModel(BaseTransformerModel):
    def __init__(self):
        super().__init__(
            model_name="textattack/bert-base-uncased-imdb"
        )