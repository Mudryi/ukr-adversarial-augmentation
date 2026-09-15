"""Strategy C (B3): among all valid synonym candidates in the pool (unfiltered by
WSD), pick the one that most reduces the target classifier's confidence in the gold
label -- the "hardest synonym-preserving example available for this input"
(article_plan.md Step 4). The replacement need not flip the prediction.

  s* = argmax_s [ p_M(y|x) - p_M(y|x_s) ]

The same function also implements the B5 CONTROL by flipping the objective to
argmin: the *least* damaging valid substitution, i.e. the one the model is most
comfortable with. B3 and B5 then differ in exactly one character of logic, which is
the point -- if B5 also improves robustness over B0, then "adversarial selection"
is not what is doing the work and RQ3's interpretation is wrong.

Reuses ukr-synonym-robustness/src/core/predictor.py (Predictor) to score every
surviving candidate in one batched forward pass.
"""

from __future__ import annotations

import random

from ._common import AugmentedExample, expand_pool_with_replacements, sample_candidate_pool

OBJECTIVES = ("max", "min")
STRATEGY_NAME = {"max": "adversarial_synonym", "min": "anti_adversarial_synonym"}


def augment_adversarial(
    text: str,
    label: int,
    synonym_dict: dict[str, list[str]],
    predictor,
    rng: random.Random,
    max_tokens: int = 3,
    max_candidates: int = 6,
    objective: str = "max",
) -> AugmentedExample | None:
    if objective not in OBJECTIVES:
        raise ValueError(f"objective must be one of {OBJECTIVES}, got {objective!r}")

    pool = sample_candidate_pool(text, synonym_dict, rng, max_tokens, max_candidates)
    if not pool:
        return None

    expanded = expand_pool_with_replacements(text, pool)
    if not expanded:
        return None

    probs = predictor([text] + [augmented for _, _, augmented in expanded])
    p_orig = probs[0, label].item()
    drops = [p_orig - probs[i + 1, label].item() for i in range(len(expanded))]

    pick = max if objective == "max" else min
    best_idx = pick(range(len(drops)), key=lambda i: drops[i])
    token, replacement, augmented_text = expanded[best_idx]
    return AugmentedExample(
        text=augmented_text,
        label=label,
        original_word=token,
        replacement=replacement,
        strategy=STRATEGY_NAME[objective],
        confidence_drop=drops[best_idx],
    )
