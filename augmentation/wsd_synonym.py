"""Strategy B (B2): random_synonym.py, but candidates are filtered by contextual
sense similarity before sampling.

Reuses ukr-synonym-robustness/src/core/wsd.py (SenseSimilarity, threshold 0.35 default).

  S_WSD(w, c) = { s in S(w) : sim(sense(w, c), sense(s, c')) > threshold }

then sample uniformly from S_WSD instead of the full dictionary entry S(w).

Implementation note: rather than scoring every candidate and then sampling, we walk
the (already shuffled) pool and return the FIRST candidate that both inflects and
passes the threshold. Because the pool order is a uniform shuffle, that draw is
uniform over the surviving candidates -- identical in distribution to score-all-then-
sample, but it needs ~1/p sense scorings instead of all of them, which is what makes
full-corpus generation tractable. `replace_word` (cheap, CPU) is checked before the
sense score (expensive, GPU) for the same reason.
"""

from __future__ import annotations

import random

from ._common import (
    DEFAULT_WSD_THRESHOLD,
    AugmentedExample,
    replace_word,
    sample_candidate_pool,
)


def augment_wsd(
    text: str,
    label: int,
    synonym_dict: dict[str, list[str]],
    sense_sim,
    rng: random.Random,
    threshold: float = DEFAULT_WSD_THRESHOLD,
    max_tokens: int = 3,
    max_candidates: int = 6,
) -> AugmentedExample | None:
    """Same as augment_random, but the chosen synonym must have contextual sense
    similarity above `threshold`. A candidate with similarity=None (no SUM-16 sense
    entry for either word) is dropped, matching run_attack.py's --use-wsd filter."""
    pool = sample_candidate_pool(text, synonym_dict, rng, max_tokens, max_candidates)
    if not pool:
        return None

    for token, candidates in pool:
        for candidate in candidates:
            new_tokens = replace_word(text, token, candidate)
            if new_tokens is None:
                continue
            score = sense_sim.score(text, token, candidate)
            if score.similarity is None or score.similarity <= threshold:
                continue
            return AugmentedExample(
                text="".join(new_tokens),
                label=label,
                original_word=token,
                replacement=candidate,
                strategy="wsd_synonym",
                wsd_similarity=score.similarity,
            )
    return None
