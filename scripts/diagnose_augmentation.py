"""Label-noise diagnostic for cached augmented data.

Augmentation preserves the gold label by construction -- the substitution is *assumed*
meaning-preserving. For the synonym-dictionary strategies (B1-B5) that assumption is
enforced upstream: `read_and_clean_synonym_dict` strips antonyms from the candidate
lists. The MLM strategies (B6/B7) have no such guarantee: they inherit BERT-Attack's
filters, and fastText cosine similarity does not separate antonyms from synonyms. A
substitution like `погана -> висока` (observed during development) inverts the sentiment
while the row keeps its original label.

That matters for RQ4. B6/B7 exist to test whether augmenting from the MLM distribution
buys robustness against BERT-Attack; if they underperform, the result is ambiguous
between "wrong distribution" and "we trained on mislabelled data" unless the label-noise
rate is measured. This script measures it, reusing the same antonym resource the
dictionary cleaning uses (`augmentation/_common.py:DEFAULT_ANTONYMS`).

Rates here are a LOWER BOUND on semantic damage: they catch only substitutions the
antonym dictionary knows about, not every meaning change.

Usage:
    python scripts/diagnose_augmentation.py                       # every cached condition
    python scripts/diagnose_augmentation.py --show-examples 20    # plus flagged pairs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from augmentation._common import DEFAULT_ANTONYMS, morph  # noqa: E402

from src.core.synonym_dict import load_entries_by_lemma  # noqa: E402


def lemma(word: str) -> str:
    parses = morph.parse(word)
    return parses[0].normal_form.lower() if parses else word.lower()


def build_antonym_map(path: str) -> dict[str, set[str]]:
    entries = load_entries_by_lemma(path)
    return {
        str(k).lower(): {str(a).lower() for a in v.get("antonyms", [])}
        for k, v in entries.items()
    }


def diagnose(jsonl: Path, antonyms: dict[str, set[str]], collect: int) -> dict:
    rows = [json.loads(line) for line in open(jsonl, encoding="utf-8") if line.strip()]
    if not rows:
        return {}
    flagged, sims, drops = [], [], []
    for r in rows:
        src, dst = lemma(r["original_word"]), lemma(r["replacement"])
        if dst in antonyms.get(src, ()):  # noqa: SIM118 -- set membership, not dict
            flagged.append((r["original_word"], r["replacement"]))
        if r.get("wsd_similarity") is not None:
            sims.append(r["wsd_similarity"])
        if r.get("confidence_drop") is not None:
            drops.append(r["confidence_drop"])
    return {
        "strategy": rows[0].get("strategy", "?"),
        "n": len(rows),
        "n_antonym": len(flagged),
        "antonym_rate": len(flagged) / len(rows),
        "mean_wsd_sim": sum(sims) / len(sims) if sims else None,
        "mean_conf_drop": sum(drops) / len(drops) if drops else None,
        "examples": flagged[:collect],
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--results-root", default="results")
    p.add_argument("--antonyms", default=DEFAULT_ANTONYMS)
    p.add_argument("--show-examples", type=int, default=0,
                   help="Print up to N flagged (original -> replacement) pairs per condition.")
    p.add_argument("--out", default=None, help="Also write a markdown table here.")
    args = p.parse_args(argv)

    print(f"loading antonyms: {args.antonyms}")
    antonyms = build_antonym_map(args.antonyms)
    print(f"{len(antonyms)} lemmas with antonym entries\n")

    root = PROJECT_ROOT / args.results_root
    results = []
    for jsonl in sorted(root.glob("*/augmented/*/augmented.jsonl")):
        d = diagnose(jsonl, antonyms, args.show_examples or 5)
        if not d:
            continue
        d["cell"] = jsonl.parent.name
        results.append(d)
        sim = f"{d['mean_wsd_sim']:.3f}" if d["mean_wsd_sim"] is not None else "-"
        drop = f"{d['mean_conf_drop']:+.4f}" if d["mean_conf_drop"] is not None else "-"
        print(f"{d['cell']:58s} {d['strategy']:22s} n={d['n']:6d} "
              f"antonyms={d['n_antonym']:4d} ({d['antonym_rate']:.2%})  wsd={sim}  drop={drop}")
        if args.show_examples:
            for src, dst in d["examples"]:
                print(f"      {src} -> {dst}")

    if args.out and results:
        cols = ["cell", "strategy", "n", "n_antonym", "antonym_rate"]
        lines = ["# Augmentation label-noise diagnostic\n",
                 "Rate of substitutions whose replacement is a known antonym of the original "
                 "word, i.e. rows whose gold label is probably now wrong. A lower bound on "
                 "semantic damage: only dictionary-known antonyms are detected.\n",
                 "| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
        for d in results:
            lines.append("| " + " | ".join(
                f"{d[c]:.2%}" if c == "antonym_rate" else str(d[c]) for c in cols) + " |")
        Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
