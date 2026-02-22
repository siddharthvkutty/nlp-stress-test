# evaluation/agreement.py

import numpy as np


def agreement_score(predictions_dict):
    """
    Returns percentage of samples where all models agree.
    """

    model_names = list(predictions_dict.keys())
    num_samples = len(predictions_dict[model_names[0]])

    agreement_count = 0

    for i in range(num_samples):
        sample_preds = [
            predictions_dict[model][i]
            for model in model_names
        ]

        if len(set(sample_preds)) == 1:
            agreement_count += 1

    return agreement_count / num_samples


def pairwise_agreement(model_a_preds, model_b_preds):
    matches = np.sum(np.array(model_a_preds) == np.array(model_b_preds))
    return matches / len(model_a_preds)