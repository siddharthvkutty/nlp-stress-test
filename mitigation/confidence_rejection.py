def apply_confidence_rejection(row, threshold=0.65):
    """
    Returns 'UNCERTAIN' if confidence < threshold,
    otherwise returns the normalized label.
    """
    if row["confidence"] < threshold:
        return "UNCERTAIN"
    return row["norm_label"]
