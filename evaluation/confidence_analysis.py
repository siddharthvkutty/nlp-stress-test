# evaluation/confidence_analysis.py

import numpy as np


def average_confidence(confidences):
    return float(np.mean(confidences))


def confidence_variance(confidences):
    return float(np.var(confidences))


def entropy(probabilities):
    """
    probabilities: list of probability distributions
    Example: [[0.7, 0.3], [0.6, 0.4]]
    """

    entropies = []

    for prob_dist in probabilities:
        prob_dist = np.array(prob_dist)
        ent = -np.sum(prob_dist * np.log(prob_dist + 1e-12))
        entropies.append(ent)

    return entropies