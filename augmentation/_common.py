"""Shared bootstrap + candidate-generation pipeline for all four augmentation
strategies (random_synonym, wsd_synonym, adversarial_synonym, wsd_adversarial_synonym).

Every strategy goes through the same three steps so differences between B1-B4 come
only from *selection* logic, not implementation drift (article_plan.md Step 2):
  1. tokenize + find eligible content-word tokens (not stopwords, in the synonym dict)
  2. look up candidate synonym lemmas for each eligible token
  3. try `replace_word` for a candidate; if it returns None (POS/inflection
     mismatch), move on to the next candidate/token instead of giving up outright.

Reuses ukr-synonym-robustness/src/core/{synonym_dict,morphology,tokenization,
stopwords,wsd,predictor}.py rather than reimplementing any of it.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path

UKR_SYNONYM_ROBUSTNESS = Path(__file__).resolve().parents[2] / "ukr-synonym-robustness"
if str(UKR_SYNONYM_ROBUSTNESS) not in sys.path:
    sys.path.insert(0, str(UKR_SYNONYM_ROBUSTNESS))

from src.core.morphology import morph, replace_word  # noqa: E402
from src.core.stopwords import get_stopwords  # noqa: E402
from src.core.synonym_dict import read_and_clean_synonym_dict  # noqa: E402
from src.core.tokenization import tokenize_ukrainian  # noqa: E402

# Exact paths run_attack.py's saved configs used to build the paper-grid synonym
# dictionary (see CURRENT_STATE.md) -- reused here so augmentation candidates come
# from the same resource the attacks were evaluated against.
DEFAULT_SYNONYM_DICT = "/home/mudryi/phd_projects/synonym_attack/synonyms_dictionaries/synonimy_info_clean.json"
DEFAULT_HAND_PARSED = "/home/mudryi/phd_projects/textfooler_ukr/hand_parsed_top_100.json"
DEFAULT_ANTONYMS = "/home/mudryi/phd_projects/synonym_attack/synonyms_dictionaries/antonimy.jsonlines"

# BERT-Attack (and MLM-based augmentation) needs Ukrainian fastText vectors.
# run_attack.py resolves them relative to CWD, which doesn't exist under this
# project, so both callers pass this absolute path explicitly.
DEFAULT_FASTTEXT = "/home/mudryi/phd_projects/bert_attack_uk/fasttext_uk_cbow/cbow.uk.300.bin"

DEFAULT_WSD_DICT = str(UKR_SYNONYM_ROBUSTNESS / "data" / "sum_16.jsonlines")
DEFAULT_WSD_MANUAL = str(UKR_SYNONYM_ROBUSTNESS / "data" / "manual_senses.json")
DEFAULT_WSD_MODEL = "lang-uk/ukr-paraphrase-multilingual-mpnet-base"
DEFAULT_WSD_THRESHOLD = 0.35

_STOPWORDS = set(get_stopwords())


def load_synonym_dict(
    path: str = DEFAULT_SYNONYM_DICT,
    hand_parsed_path: str | None = DEFAULT_HAND_PARSED,
    antonyms_path: str | None = DEFAULT_ANTONYMS,
) -> dict[str, list[str]]:
    return read_and_clean_synonym_dict(
        path, hand_parsed_path=hand_parsed_path, antonyms_path=antonyms_path
    )


def build_sense_similarity(
    dict_path: str = DEFAULT_WSD_DICT,
    manual_path: str = DEFAULT_WSD_MANUAL,
    model_name: str = DEFAULT_WSD_MODEL,
):
    from src.core.wsd import SenseSimilarity

    return SenseSimilarity(model_name=model_name, dict_path=dict_path, manual_path=manual_path)


@dataclass
class AugmentedExample:
    text: str
    label: int
    original_word: str
    replacement: str
    strategy: str
    wsd_similarity: float | None = None
    confidence_drop: float | None = None


def eligible_tokens(text: str, synonym_dict: dict[str, list[str]]) -> list[tuple[str, list[str]]]:
    """Return [(token, candidate_lemmas)] for every content-word token in `text`
    that has at least one synonym candidate. Order follows token order in the text."""
    out: list[tuple[str, list[str]]] = []
    seen_tokens: set[str] = set()
    for tok in tokenize_ukrainian(text):
        low = tok.lower()
        if not tok.isalpha() or low in _STOPWORDS or low in seen_tokens:
            continue
        seen_tokens.add(low)
        parses = morph.parse(tok)
        if not parses:
            continue
        lemma = parses[0].normal_form
        candidates = synonym_dict.get(lemma, [])
        if candidates:
            out.append((tok, list(candidates)))
    return out


def sample_candidate_pool(
    text: str,
    synonym_dict: dict[str, list[str]],
    rng: random.Random,
    max_tokens: int = 3,
    max_candidates: int = 6,
) -> list[tuple[str, list[str]]]:
    """The capped candidate space that EVERY strategy consumes, so B1-B4 differ only
    in their selection rule and not in the space they select from (article_plan.md
    Step 2). Caps keep the adversarial/WSD strategies tractable: they must score
    every candidate, so an uncapped pool (up to ~300 candidates/example) makes
    generation cost hours per 1k rows.

    Tokens and candidates are shuffled before truncation, so the surviving pool is a
    uniform random subset."""
    tokens = eligible_tokens(text, synonym_dict)
    if not tokens:
        return []
    rng.shuffle(tokens)
    pool: list[tuple[str, list[str]]] = []
    for token, candidates in tokens[:max_tokens]:
        shuffled = list(candidates)
        rng.shuffle(shuffled)
        pool.append((token, shuffled[:max_candidates]))
    return pool


def try_replacements(
    text: str, token: str, candidates: list[str], rng: random.Random
) -> tuple[str, str] | None:
    """Shuffle `candidates` and return the first (candidate, augmented_text) for
    which `replace_word` succeeds, or None if none of them inflect cleanly."""
    shuffled = candidates.copy()
    rng.shuffle(shuffled)
    for candidate in shuffled:
        new_tokens = replace_word(text, token, candidate)
        if new_tokens is not None:
            return candidate, "".join(new_tokens)
    return None


def expand_pool_with_replacements(
    text: str, token_candidates: list[tuple[str, list[str]]]
) -> list[tuple[str, str, str]]:
    """Expand every (token, candidate) pair that survives `replace_word` into
    (token, candidate, augmented_text). Used by the adversarial strategies, which
    need to score *every* surviving candidate against the classifier rather than
    stopping at the first success (unlike random_synonym/wsd_synonym, which only
    need one valid replacement)."""
    pool: list[tuple[str, str, str]] = []
    for token, candidates in token_candidates:
        for candidate in candidates:
            new_tokens = replace_word(text, token, candidate)
            if new_tokens is not None:
                pool.append((token, candidate, "".join(new_tokens)))
    return pool
