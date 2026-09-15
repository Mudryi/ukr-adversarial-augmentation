"""Strategy A (B1): replace one content word with a randomly chosen dictionary synonym.

Reuses ukr-synonym-robustness/src/core/{synonym_dict,morphology}.py for candidate
generation and inflection. No classifier or WSD signal used.
"""

from __future__ import annotations

import random

from ._common import AugmentedExample, sample_candidate_pool, try_replacements


def augment_random(
    text: str,
    label: int,
    synonym_dict: dict[str, list[str]],
    rng: random.Random,
    max_tokens: int = 3,
    max_candidates: int = 6,
) -> AugmentedExample | None:
    """Pick one eligible content word at random and replace it with a random
    dictionary synonym (correctly inflected). Returns None if no candidate in the
    pool survives morphological inflection (coverage miss)."""
    pool = sample_candidate_pool(text, synonym_dict, rng, max_tokens, max_candidates)
    if not pool:
        return None

    for token, candidates in pool:
        result = try_replacements(text, token, candidates, rng)
        if result is not None:
            replacement, augmented_text = result
            return AugmentedExample(
                text=augmented_text,
                label=label,
                original_word=token,
                replacement=replacement,
                strategy="random_synonym",
            )
    return None
