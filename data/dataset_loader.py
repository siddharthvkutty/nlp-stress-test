# data/dataset_loader.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class DatasetLoader:
    def __init__(
        self,
        file_path: str,
        text_column: str = "text",
        label_column: str = "label",
        test_size: float = 0.2,
        random_state: int = 42
    ):
        self.file_path = file_path
        self.text_column = text_column
        self.label_column = label_column
        self.test_size = test_size
        self.random_state = random_state

        self.df = None
        self.label_encoder = None

    # -----------------------------
    # Load Dataset
    # -----------------------------
    def load(self):
        if self.file_path.endswith(".csv"):
            self.df = pd.read_csv(self.file_path)

        elif self.file_path.endswith(".json"):
            self.df = pd.read_json(self.file_path)

        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")

        self._validate_columns()
        self._clean_data()

        return self.df

    # -----------------------------
    # Validate Required Columns
    # -----------------------------
    def _validate_columns(self):
        if self.text_column not in self.df.columns:
            raise ValueError(f"Text column '{self.text_column}' not found.")

        if self.label_column not in self.df.columns:
            raise ValueError(f"Label column '{self.label_column}' not found.")

    # -----------------------------
    # Clean Data
    # -----------------------------
    def _clean_data(self):
        self.df = self.df[[self.text_column, self.label_column]]
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    # -----------------------------
    # Encode Labels
    # -----------------------------
    def encode_labels(self):
        self.label_encoder = LabelEncoder()
        self.df[self.label_column] = self.label_encoder.fit_transform(
            self.df[self.label_column]
        )
        return self.df

    # -----------------------------
    # Decode Labels (NEW)
    # -----------------------------
    def decode_labels(self, encoded_labels):
        if self.label_encoder is None:
            raise ValueError("Labels have not been encoded yet.")
        return self.label_encoder.inverse_transform(encoded_labels)

    # -----------------------------
    # Train/Test Split
    # -----------------------------
    def split(self):
        X = self.df[self.text_column].tolist()
        y = self.df[self.label_column].tolist()

        return train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y
        )

    # -----------------------------
    # Dataset Summary
    # -----------------------------
    def summary(self):
        return {
            "num_samples": len(self.df),
            "num_classes": self.df[self.label_column].nunique(),
            "class_distribution": {
                int(k): int(v)
                for k, v in self.df[self.label_column].value_counts().to_dict().items()
            },
            "label_mapping": {
                int(k): str(v)
                for k, v in (
                    zip(
                        self.label_encoder.transform(self.label_encoder.classes_),
                        self.label_encoder.classes_
                    )
                )
            } if self.label_encoder else None
        }

    # -----------------------------
    # Get Raw Data
    # -----------------------------
    def get_texts_and_labels(self):
        X = self.df[self.text_column].tolist()
        y = self.df[self.label_column].tolist()
        return X, y