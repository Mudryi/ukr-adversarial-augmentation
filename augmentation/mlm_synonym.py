"""MLM-based augmentation (conditions B6 / B7) -- the second half of the RQ4 matrix.

The Stage-A pilot showed that augmentation built from the *synonym-dictionary*
distribution (B1-B5) buys robustness against the TextFooler family and nothing
against BERT-Attack. That result on its own cannot distinguish two explanations:

  (a) synonym augmentation in general does not transfer across attack families, or
  (b) TextFooler-style candidates specifically are too narrow.

To separate them we need the mirror experiment: augment from the distribution
BERT-Attack itself samples from (masked-LM fill-in), and evaluate under TextFooler.
That is what this module generates.

Candidates therefore come from exactly the machinery the attack uses -- the
`fill-mask` pipeline over `FacebookAI/xlm-roberta-large` (run_attack.py's default
--mlm-model) and the same four admissibility filters as
`BertAttack._candidate_passes_filters` (src/attacks/bert_attack.py), at run_attack's
own thresholds. Nothing about the candidate distribution is reinvented here.

Two differences from the synonym-dictionary strategies, both intrinsic to the method
rather than choices:

  * No morphological inflection step. `replace_word` exists because a synonym
    dictionary stores lemmas; an MLM predicts an already-inflected surface form in
    context, so there is nothing to inflect and no inflection-failure skip.
  * The per-token candidate cap keeps the MLM's top-scoring survivors rather than a
    random subset, because the MLM's ranking is part of what BERT-Attack exploits.
    (For B1-B5 the pool is a uniform random subset -- there is no meaningful ranking
    over dictionary synonyms.)
"""

from __future__ import annotations

import random

from ._common import (  # noqa: F401 (also bootstraps sys.path)
    DEFAULT_FASTTEXT,
    UKR_SYNONYM_ROBUSTNESS,
    AugmentedExample,
)

from src.core.morphology import compare_normal_forms  # noqa: E402
from src.core.stopwords import get_stopwords  # noqa: E402
from src.core.tokenization import (  # noqa: E402
    filter_not_words,
    has_foreign_letters,
    tokenize_with_whitespace,
)

# run_attack.py's actual BERT-Attack defaults (src/cli/run_attack.py), not
# BertAttack.__init__'s -- these are the values the published attack cells were run
# with, so augmentation and attack see the same candidate distribution.
DEFAULT_MLM_MODEL = "FacebookAI/xlm-roberta-large"
DEFAULT_NUM_SUBS = 128
DEFAULT_THRESHOLD_SCORE = 0.04
DEFAULT_COS_SIM_THRESHOLD = 0.33


class MlmCandidateSource:
    """Loads the fill-mask pipeline + fastText vectors once and generates filtered
    substitution candidates. Expensive to construct (an XLM-R-large MLM and an 8.8GB
    fastText model), so build it once per generation run, never per example."""

    def __init__(
        self,
        mlm_model: str = DEFAULT_MLM_MODEL,
        fasttext_path: str | None = DEFAULT_FASTTEXT,
        num_subs: int = DEFAULT_NUM_SUBS,
        threshold_score: float = DEFAULT_THRESHOLD_SCORE,
        cos_sim_threshold: float = DEFAULT_COS_SIM_THRESHOLD,
    ):
        import torch
        from transformers import AutoTokenizer, pipeline

        from src.core.similarity import FastTextSim

        tokenizer = AutoTokenizer.from_pretrained(mlm_model, truncation=True)
        tokenizer.model_max_length = 512
        device = 0 if torch.cuda.is_available() else -1
        self.unmasker = pipeline("fill-mask", model=mlm_model, tokenizer=tokenizer, device=device)
        self.mask_token = tokenizer.mask_token
        self.ft_sim = FastTextSim(fasttext_path)
        self.stopwords = set(get_stopwords())
        self.num_subs = num_subs
        self.threshold_score = threshold_score
        self.cos_sim_threshold = cos_sim_threshold

    def _passes(self, candidate: str, target_word: str) -> bool:
        """Identical predicate set to BertAttack._candidate_passes_filters."""
        if has_foreign_letters(candidate):
            return False
        if filter_not_words(candidate, target_word, stopwords=self.stopwords):
            return False
        if not self.ft_sim.is_semantic_near(target_word, candidate, self.cos_sim_threshold):
            return False
        if compare_normal_forms(target_word, candidate):
            return False
        return True

    def pool(
        self, text: str, rng: random.Random, max_tokens: int = 3, max_candidates: int = 6
    ) -> list[tuple[str, str, str]]:
        """Return [(original_word, replacement, augmented_text)] for up to
        `max_tokens` randomly chosen maskable positions."""
        words = tokenize_with_whitespace(text)
        positions = [
            i for i, w in enumerate(words)
            if not filter_not_words(w, stopwords=self.stopwords)
        ]
        if not positions:
            return []
        rng.shuffle(positions)
        positions = positions[:max_tokens]

        masked_texts = [
            "".join(self.mask_token if k == i else w for k, w in enumerate(words))
            for i in positions
        ]
        try:
            batched = self.unmasker(masked_texts, top_k=self.num_subs)
        except Exception:  # noqa: BLE001 -- a malformed/over-long row must not kill the run
            return []
        # A single-element input list can come back flat; normalise to list-of-lists.
        if batched and isinstance(batched[0], dict):
            batched = [batched]

        out: list[tuple[str, str, str]] = []
        for i, results in zip(positions, batched):
            target = words[i]
            kept = 0
            for r in results:
                if r["score"] < self.threshold_score:
                    break  # results are score-ordered
                # XLM-R's sentencepiece token_str carries a leading space for
                # word-initial pieces; splicing it in verbatim would double the space.
                candidate = r["token_str"].strip()
                if not candidate or not self._passes(candidate, target):
                    continue
                augmented = "".join(candidate if k == i else w for k, w in enumerate(words))
                out.append((target, candidate, augmented))
                kept += 1
                if kept >= max_candidates:
                    break
        return out


def augment_mlm_random(
    text: str,
    label: int,
    source: MlmCandidateSource,
    rng: random.Random,
    max_tokens: int = 3,
    max_candidates: int = 6,
) -> AugmentedExample | None:
    """B6 -- the MLM-distribution mirror of B1 (random selection)."""
    pool = source.pool(text, rng, max_tokens, max_candidates)
    if not pool:
        return None
    token, replacement, augmented_text = rng.choice(pool)
    return AugmentedExample(
        text=augmented_text,
        label=label,
        original_word=token,
        replacement=replacement,
        strategy="mlm_random",
    )


def augment_mlm_adversarial(
    text: str,
    label: int,
    source: MlmCandidateSource,
    predictor,
    rng: random.Random,
    max_tokens: int = 3,
    max_candidates: int = 6,
) -> AugmentedExample | None:
    """B7 -- the MLM-distribution mirror of B3 (max confidence drop)."""
    pool = source.pool(text, rng, max_tokens, max_candidates)
    if not pool:
        return None

    probs = predictor([text] + [augmented for _, _, augmented in pool])
    p_orig = probs[0, label].item()
    drops = [p_orig - probs[i + 1, label].item() for i in range(len(pool))]

    best_idx = max(range(len(drops)), key=lambda i: drops[i])
    token, replacement, augmented_text = pool[best_idx]
    return AugmentedExample(
        text=augmented_text,
        label=label,
        original_word=token,
        replacement=replacement,
        strategy="mlm_adversarial",
        confidence_drop=drops[best_idx],
    )
