# models/model_loader.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class BaseTransformerModel:
    def __init__(self, model_name: str, num_labels: int = 2):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name
        )

        self.model.to(self.device)
        self.model.eval()

        self.model_name = model_name

    def predict(self, text: str, max_length: int = 256):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=max_length
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)

        confidence, prediction = torch.max(probs, dim=1)

        return {
            "prediction": prediction.item(),
            "confidence": confidence.item(),
            "probabilities": probs.squeeze().tolist()
        }

    def predict_batch(self, texts, max_length: int = 256):
        inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=max_length
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)

        confidences, predictions = torch.max(probs, dim=1)

        return [
            {
                "prediction": pred.item(),
                "confidence": conf.item(),
                "probabilities": prob.tolist()
            }
            for pred, conf, prob in zip(predictions, confidences, probs)
        ]