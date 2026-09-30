"""Pre-generate and cache augmented training data for a given
(dataset, strategy, augmentation_ratio, seed).

Augments D_train only -- never touch val/test (article_plan.md Step 0 guardrail).
Output is cached to disk (augmented.csv + augmented.jsonl diagnostics) so training
runs are deterministic and don't re-run synonym generation each time.

Usage (random / wsd strategies -- no classifier needed):
    python scripts/generate_augmented_dataset.py \
        --dataset reviews --strategy random --ratio 0.5 --seed 1914 \
        --output-dir results/augmented/reviews__random__r0.5__seed1914

Usage (adversarial / wsd_adversarial -- need a B0 checkpoint to score candidates):
    python scripts/generate_augmented_dataset.py \
        --dataset reviews --strategy wsd_adversarial --ratio 0.5 --seed 1914 \
        --target-model xlm-roberta-base \
        --target-checkpoint ../xml-roberta-finetune-reviews/trained_models/tmdk/model_tmdk_7_600 \
        --output-dir results/augmented/reviews__wsd_adversarial__xlmr__r0.5__seed1914

`--limit N` caps the number of (shuffled) training rows considered, for a quick
debug run before launching on the full train CSV.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import asdict
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from augmentation._common import (  # noqa: E402
    DEFAULT_FASTTEXT,
    DEFAULT_WSD_THRESHOLD,
    build_sense_similarity,
    load_synonym_dict,
)
from augmentation.adversarial_synonym import augment_adversarial  # noqa: E402
from augmentation.random_synonym import augment_random  # noqa: E402
from augmentation.wsd_adversarial_synonym import augment_wsd_adversarial  # noqa: E402
from augmentation.wsd_synonym import augment_wsd  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Which strategies need what. Model-dependent strategies score candidates against a
# trained M_0 checkpoint; MLM strategies additionally need the fill-mask model and
# fastText vectors that BERT-Attack uses.
STRATEGIES = ["random", "wsd", "adversarial", "wsd_adversarial",
              "anti_adversarial", "mlm_random", "mlm_adversarial"]
NEEDS_PREDICTOR = {"adversarial", "wsd_adversarial", "anti_adversarial", "mlm_adversarial"}
NEEDS_MLM = {"mlm_random", "mlm_adversarial"}

# Mirrors ukr-synonym-robustness/src/core/data.py's column/label conventions, but
# operates on the FULL train CSV (no 10k-row cap -- that cap is for attack-eval
# subsampling, not augmentation source data).
NEWS_LABELS = ["бізнес", "новини", "політика", "спорт", "технології"]
NEWS_LABEL2ID = {label: i for i, label in enumerate(NEWS_LABELS)}


def load_train_rows(dataset: str, train_csv: str) -> list[tuple[int, str, int]]:
    """Returns [(row_index, text, int_label)] for the full training CSV."""
    df = pd.read_csv(train_csv)
    rows: list[tuple[int, str, int]] = []
    if dataset == "reviews":
        for idx, row in df.iterrows():
            rows.append((idx, str(row["text"]), int(row["label"]) - 1))
    elif dataset == "news":
        df["_label_id"] = df["target"].map(NEWS_LABEL2ID)
        for idx, row in df.iterrows():
            if pd.isna(row["_label_id"]):
                continue
            rows.append((idx, str(row["title"]), int(row["_label_id"])))
    elif dataset == "unlp":
        for idx, row in df.iterrows():
            rows.append((idx, str(row["text"]), int(row["label"])))
    else:
        raise ValueError(f"unknown dataset: {dataset!r}")
    return rows


def default_train_csv(dataset: str) -> str:
    cfg_path = PROJECT_ROOT / "configs" / f"{dataset}.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg["train-path"]


def build_predictor(args):
    from src.core.predictor import Predictor  # noqa: E402 (sys.path bootstrapped by _common)

    if not args.target_model or not args.target_checkpoint or not args.nclasses:
        sys.exit(f"--strategy {args.strategy} requires --target-model, "
                 "--target-checkpoint, and --nclasses")
    return Predictor(
        target_model=args.target_model,
        target_checkpoint=args.target_checkpoint,
        nclasses=args.nclasses,
    )


def build_augment_fn(args):
    caps = {"max_tokens": args.max_tokens, "max_candidates": args.max_candidates}

    # ---- MLM-distribution strategies (B6/B7): no synonym dictionary involved ----
    if args.strategy in NEEDS_MLM:
        from augmentation.mlm_synonym import (
            DEFAULT_MLM_MODEL,
            MlmCandidateSource,
            augment_mlm_adversarial,
            augment_mlm_random,
        )

        source = MlmCandidateSource(
            mlm_model=args.mlm_model or DEFAULT_MLM_MODEL,
            fasttext_path=args.fasttext_path,
        )
        rng = random.Random(args.seed)
        if args.strategy == "mlm_random":
            return lambda text, label: augment_mlm_random(text, label, source, rng, **caps)
        predictor = build_predictor(args)
        return lambda text, label: augment_mlm_adversarial(
            text, label, source, predictor, rng, **caps
        )

    # ---- synonym-dictionary strategies (B1-B5) ----
    synonym_dict = load_synonym_dict()

    if args.strategy == "random":
        rng = random.Random(args.seed)
        return lambda text, label: augment_random(text, label, synonym_dict, rng, **caps)

    if args.strategy == "wsd":
        rng = random.Random(args.seed)
        sense_sim = build_sense_similarity()
        return lambda text, label: augment_wsd(
            text, label, synonym_dict, sense_sim, rng, threshold=args.wsd_threshold, **caps
        )

    if args.strategy in ("adversarial", "anti_adversarial", "wsd_adversarial"):
        predictor = build_predictor(args)
        rng = random.Random(args.seed)
        if args.strategy in ("adversarial", "anti_adversarial"):
            # B3 and B5 share one implementation and differ only in argmax vs argmin,
            # so the control is guaranteed to be identical in every other respect.
            objective = "max" if args.strategy == "adversarial" else "min"
            return lambda text, label: augment_adversarial(
                text, label, synonym_dict, predictor, rng, objective=objective, **caps
            )

        sense_sim = build_sense_similarity()
        return lambda text, label: augment_wsd_adversarial(
            text, label, synonym_dict, sense_sim, predictor, rng,
            threshold=args.wsd_threshold, **caps
        )

    raise ValueError(f"unknown strategy: {args.strategy!r}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", choices=["reviews", "news", "unlp"], required=True)
    p.add_argument("--strategy", choices=STRATEGIES, required=True)
    p.add_argument("--train-csv", type=str, default=None, help="Defaults to configs/<dataset>.yaml train-path.")
    p.add_argument("--ratio", type=float, default=0.5, help="|D_aug| / |D_train| target.")
    p.add_argument("--seed", type=int, default=1914)
    p.add_argument("--limit", type=int, default=None, help="Debug cap on rows considered (before ratio sampling).")
    p.add_argument("--wsd-threshold", type=float, default=DEFAULT_WSD_THRESHOLD)
    p.add_argument("--max-tokens", type=int, default=3,
                   help="Max eligible tokens per example in the shared candidate pool.")
    p.add_argument("--max-candidates", type=int, default=6,
                   help="Max synonym candidates per token in the shared candidate pool. "
                        "Must be identical across strategies for a fair B1-B4 comparison.")
    p.add_argument("--target-model", type=str, default=None, help="Required for adversarial/wsd_adversarial.")
    p.add_argument("--target-checkpoint", type=str, default=None, help="Required for adversarial/wsd_adversarial.")
    p.add_argument("--nclasses", type=int, default=None, help="Required for adversarial/wsd_adversarial.")
    p.add_argument("--mlm-model", type=str, default=None,
                   help="fill-mask model for mlm_* strategies; defaults to run_attack.py's.")
    p.add_argument("--fasttext-path", type=str, default=DEFAULT_FASTTEXT,
                   help="Ukrainian fastText vectors, used by mlm_* candidate filtering.")
    p.add_argument("--output-dir", type=str, required=True)
    args = p.parse_args(argv)

    train_csv = args.train_csv or default_train_csv(args.dataset)
    print(f"loading full train set: {train_csv}")
    rows = load_train_rows(args.dataset, train_csv)
    print(f"{len(rows)} training rows")

    rng_order = random.Random(args.seed)
    rng_order.shuffle(rows)
    if args.limit is not None:
        rows = rows[: args.limit]

    target_n = int(round(args.ratio * len(rows)))
    print(f"target augmented rows: {target_n} (ratio={args.ratio})")

    augment_fn = build_augment_fn(args)

    augmented_rows = []
    diagnostics = []
    n_attempted = 0
    for row_idx, text, label in rows:
        if len(augmented_rows) >= target_n:
            break
        n_attempted += 1
        result = augment_fn(text, label)
        if result is None:
            continue
        augmented_rows.append({"text": result.text, "label": result.label})
        diagnostics.append({
            "sample_id": int(row_idx),
            "original_text": text,
            "augmented_text": result.text,
            "original_word": result.original_word,
            "replacement": result.replacement,
            "strategy": result.strategy,
            "wsd_similarity": result.wsd_similarity,
            "confidence_drop": result.confidence_drop,
            "gold_label": label,
        })

    coverage = len(augmented_rows) / n_attempted if n_attempted else 0.0
    print(f"attempted {n_attempted} rows, produced {len(augmented_rows)} augmented rows "
          f"(coverage={coverage:.1%})")
    if len(augmented_rows) < target_n:
        print(f"WARNING: exhausted available rows before hitting target_n={target_n}; "
              f"only {len(augmented_rows)} produced.")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    aug_csv = out_dir / "augmented.csv"
    pd.DataFrame(augmented_rows).to_csv(aug_csv, index=False)

    diag_path = out_dir / "augmented.jsonl"
    with open(diag_path, "w", encoding="utf-8") as f:
        for d in diagnostics:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    meta_path = out_dir / "meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "dataset": args.dataset,
            "strategy": args.strategy,
            "train_csv": train_csv,
            "ratio": args.ratio,
            "seed": args.seed,
            "n_train_rows": len(rows),
            "n_attempted": n_attempted,
            "n_augmented": len(augmented_rows),
            "coverage": coverage,
            "wsd_threshold": args.wsd_threshold if args.strategy in ("wsd", "wsd_adversarial") else None,
            "max_tokens": args.max_tokens,
            "max_candidates": args.max_candidates,
            "mlm_model": (args.mlm_model or "default") if args.strategy in NEEDS_MLM else None,
            "target_model": args.target_model,
            "target_checkpoint": args.target_checkpoint,
        }, f, ensure_ascii=False, indent=2)

    print(f"wrote {aug_csv}")
    print(f"wrote {diag_path}")
    print(f"wrote {meta_path}")


if __name__ == "__main__":
    main()
