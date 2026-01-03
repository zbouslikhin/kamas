import numpy as np

def weighted_vote(
    *signals: np.ndarray,
    weights: list[float],
    threshold: float,
) -> np.ndarray:
    """
    Combine multiple boolean signals into a confidence score.
    Returns True where confidence >= threshold.
    """

    if len(signals) != len(weights):
        raise ValueError("Signals and weights length mismatch")

    # Convert bool -> int (True=1, False=0)
    score = np.zeros_like(signals[0], dtype=float)
    total_weight = sum(weights)

    for sig, w in zip(signals, weights):
        score += sig.astype(float) * w

    confidence = (score / total_weight) * 100.0
    return confidence >= threshold