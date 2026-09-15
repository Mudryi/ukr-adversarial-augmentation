"""Evaluate a trained checkpoint on clean + TextFooler + BERT-Attack + WSD-TextFooler,
reusing ukr-synonym-robustness/src/cli/run_attack.py's main() directly (no
reimplementation, no subprocess) as the attack runner.

Clean accuracy/macro-F1 don't need a separate run: every attack's examples.jsonl
already carries `orig_label` (the classifier's clean prediction) per row, so
scripts/aggregate_results.py derives clean metrics from whichever attack cell it reads.

Writes into results/<attack>/<dataset>__<model>__<condition>__seed<seed>[__wsd035]/,
mirroring ukr-synonym-robustness's own directory convention so aggregate_results.py
can process old B0 cells and new B1-B4 cells uniformly.

Usage:
    python scripts/evaluate_robustness.py \
        --dataset reviews --model xlmr_base --condition B2 --seed 1914 \
        --checkpoint results/checkpoints/reviews__xlmr_base__B2__seed1914 \
        [--n-samples 50]   # smoke-test idiom, matches run_attack.py's own convention
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from augmentation._common import (  # noqa: E402
    DEFAULT_ANTONYMS,
    DEFAULT_FASTTEXT,
    DEFAULT_HAND_PARSED,
    DEFAULT_SYNONYM_DICT,
    DEFAULT_WSD_DICT,
    DEFAULT_WSD_MANUAL,
    DEFAULT_WSD_MODEL,
    DEFAULT_WSD_THRESHOLD,
    UKR_SYNONYM_ROBUSTNESS,
)

from src.cli import run_attack  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NCLASSES = {"reviews": 5, "news": 5, "unlp": 2}
CONDITIONS = ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"]


def load_config(dataset: str) -> dict:
    with open(PROJECT_ROOT / "configs" / f"{dataset}.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cell_name(dataset: str, model: str, condition: str, seed: int,
              wsd: bool = False, variant: str = "") -> str:
    """`variant` distinguishes ablation runs (pool10x20, r0.25, full78k, ...) that
    share a dataset/model/condition/seed with the main grid. Empty for the main grid.
    aggregate_results.py parses this position as its own field."""
    name = f"{dataset}__{model}__{condition}__seed{seed}"
    if variant:
        name += f"__{variant}"
    return name + "__wsd035" if wsd else name


def run_one_attack(*, attack: str, use_wsd: bool, args, cfg) -> Path:
    results_root = Path(args.results_root)
    if not results_root.is_absolute():
        results_root = PROJECT_ROOT / results_root
    output_dir = results_root / attack / cell_name(
        args.dataset, args.model, args.condition, args.seed, wsd=use_wsd, variant=args.variant
    )
    argv = [
        "--attack", attack,
        "--dataset", args.dataset,
        "--dataset-path", cfg["test-path"],
        "--target-model", cfg["models"][args.model]["hf-name"],
        "--target-checkpoint", args.checkpoint,
        "--nclasses", str(NCLASSES[args.dataset]),
        "--output-dir", str(output_dir),
        "--seed", str(args.seed),
        "--synonym-dict", DEFAULT_SYNONYM_DICT,
        "--hand-parsed", DEFAULT_HAND_PARSED,
        "--antonyms", DEFAULT_ANTONYMS,
    ]
    if args.n_samples is not None:
        argv += ["--n-samples", str(args.n_samples)]
    if attack == "bert_attack":
        argv += ["--fasttext-path", args.fasttext_path]
    if attack == "textfooler" and use_wsd:
        argv += [
            "--use-wsd",
            "--wsd-threshold", str(DEFAULT_WSD_THRESHOLD),
            "--wsd-dict-path", DEFAULT_WSD_DICT,
            "--wsd-manual-path", DEFAULT_WSD_MANUAL,
            "--wsd-model", DEFAULT_WSD_MODEL,
        ]
    print(f"\n=== running {attack}{' +wsd' if use_wsd else ''} -> {output_dir} ===")
    run_attack.main(argv)
    return output_dir


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", choices=["reviews", "news", "unlp"], required=True)
    p.add_argument("--model", choices=["ukr_roberta", "xlmr_base"], required=True)
    p.add_argument("--condition", choices=CONDITIONS, required=True)
    p.add_argument("--checkpoint", type=str, required=True)
    p.add_argument("--seed", type=int, default=1914)
    p.add_argument("--n-samples", type=int, default=None, help="Smoke-test cap, matches run_attack.py.")
    p.add_argument("--skip-bert-attack", action="store_true", help="TextFooler(+wsd) only, for a quick check.")
    p.add_argument("--only", choices=["textfooler", "textfooler_wsd", "bert_attack"], default=None,
                   help="Run a single attack instead of all three (used by run_pilot.py to "
                        "order cells attack-major, so partial results stay interpretable).")
    p.add_argument("--fasttext-path", type=str, default=DEFAULT_FASTTEXT)
    p.add_argument("--variant", type=str, default="",
                   help="Ablation tag folded into the cell name (e.g. pool10x20, r0.25).")
    p.add_argument("--results-root", type=str, default="results",
                   help="Root for attack cells; relative paths resolve against the project root.")
    args = p.parse_args(argv)

    cfg = load_config(args.dataset)

    if args.only == "textfooler":
        run_one_attack(attack="textfooler", use_wsd=False, args=args, cfg=cfg)
    elif args.only == "textfooler_wsd":
        run_one_attack(attack="textfooler", use_wsd=True, args=args, cfg=cfg)
    elif args.only == "bert_attack":
        run_one_attack(attack="bert_attack", use_wsd=False, args=args, cfg=cfg)
    else:
        run_one_attack(attack="textfooler", use_wsd=False, args=args, cfg=cfg)
        run_one_attack(attack="textfooler", use_wsd=True, args=args, cfg=cfg)
        if not args.skip_bert_attack:
            run_one_attack(attack="bert_attack", use_wsd=False, args=args, cfg=cfg)

    print("\ndone. Run scripts/aggregate_results.py --root results to compute macro-F1/cASR/flip-rate.")


if __name__ == "__main__":
    main()
