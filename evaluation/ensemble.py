# evaluation/ensemble.py

from collections import Counter
import numpy as np


def majority_vote(predictions_list):
    """
    predictions_list: list of model predictions for ONE sample
    Example: [0, 1, 1]
    """
    return Counter(predictions_list).most_common(1)[0][0]


def ensemble_batch(predictions_dict):
    """
    predictions_dict:
    {
        "bert": [0,1,1,...],
        "roberta": [0,0,1,...],
        "distilbert": [1,1,1,...]
    }
    """

    model_names = list(predictions_dict.keys())
    num_samples = len(predictions_dict[model_names[0]])

    ensemble_preds = []

    for i in range(num_samples):
        sample_preds = [
            predictions_dict[model][i]
            for model in model_names
        ]
        ensemble_preds.append(majority_vote(sample_preds))

    return ensemble_preds


def average_confidence(confidence_dict):
    """
    confidence_dict:
    {
        "bert": [0.8, 0.7, ...],
        "roberta": [0.9, 0.6, ...],
        "distilbert": [0.75, 0.65, ...]
    }
    """

    model_names = list(confidence_dict.keys())
    num_samples = len(confidence_dict[model_names[0]])

    avg_conf = []

    for i in range(num_samples):
        confs = [confidence_dict[model][i] for model in model_names]
        avg_conf.append(float(np.mean(confs)))

    return avg_conf