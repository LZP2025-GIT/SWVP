from typing import Dict, List

def combine_posteriors(posteriors: List[float]) -> float:
    """
    P_combined = 1 - Π(1 - P_i) assuming conditional independence.
   """
    prod = 1.0
    for p in posteriors:
        prod *= (1.0 - max(0.0, min(1.0, p)))
    return 1.0 - prod

def tier_from_probs(p_single: float, p_combined: float, dual_threshold=0.55, tri_threshold=0.75):
    if p_combined >= tri_threshold:
        return "Tier I"
    if p_single >= dual_threshold:
        return "Tier II"
    if p_single >= 0.35:
        return "Tier III"
    return "Tier IV"
