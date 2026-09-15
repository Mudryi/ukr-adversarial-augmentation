"""Strategy D (B4) -- Sense-Aware Adversarial Augmentation (SAAA), the proposed
method. WSD-filter the candidate pool (as in wsd_synonym.py) then pick the most
confidence-reducing survivor (as in adversarial_synonym.py):

  s* = argmax_{s in S_WSD(w, c)} [ p(y|x) - p(y|x_s) ]

This is the paper's main candidate method. Unlike wsd_synonym it cannot early-exit
on the first surviving candidate -- the argmax needs every survivor scored -- which
is why the shared pool caps (max_tokens/max_candidates) matter most here.
"""

from __future__ import annotations

import random

from ._common import (
    DEFAULT_WSD_THRESHOLD,
    AugmentedExample,
    replace_word,
    sample_candidate_pool,
)


def augment_wsd_adversarial(
    text: str,
    label: int,
    synonym_dict: dict[str, list[str]],
    sense_sim,
    predictor,
    rng: random.Random,
    threshold: float = DEFAULT_WSD_THRESHOLD,
    max_tokens: int = 3,
    max_candidates: int = 6,
) -> AugmentedExample | None:
    pool = sample_candidate_pool(text, synonym_dict, rng, max_tokens, max_candidates)
    if not pool:
        return None

    survivors: list[tuple[str, str, str, float]] = []  # token, candidate, text, similarity
    for token, candidates in pool:
        for candidate in candidates:
            new_tokens = replace_word(text, token, candidate)
            if new_tokens is None:
                continue
            score = sense_sim.score(text, token, candidate)
            if score.similarity is None or score.similarity <= threshold:
                continue
            survivors.append((token, candidate, "".join(new_tokens), score.similarity))

    if not survivors:
        return None

    probs = predictor([text] + [s[2] for s in survivors])
    p_orig = probs[0, label].item()
    drops = [p_orig - probs[i + 1, label].item() for i in range(len(survivors))]

    best_idx = max(range(len(drops)), key=lambda i: drops[i])
    token, replacement, augmented_text, similarity = survivors[best_idx]
    return AugmentedExample(
        text=augmented_text,
        label=label,
        original_word=token,
        replacement=replacement,
        strategy="wsd_adversarial_synonym",
        wsd_similarity=similarity,
        confidence_drop=drops[best_idx],
    )
