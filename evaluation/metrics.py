# evaluation/metrics.py

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)


def compute_basic_metrics(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="weighted"
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


def generate_classification_report(y_true, y_pred):
    return classification_report(y_true, y_pred)


def generate_confusion_matrix(y_true, y_pred):
    return confusion_matrix(y_true, y_pred)