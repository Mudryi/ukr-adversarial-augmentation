"""Stage-A pilot orchestrator (RESEARCH_PLAN.md): XLM-R + UA Reviews, one seed,
five training conditions B0-B4, evaluated under TextFooler / WSD-TextFooler /
BERT-Attack.

Design decisions that make this fit an overnight window on one RTX 3090:

  * Clean train is a fixed deterministic SUBSAMPLE (default 20k of 78k rows), written
    once to results/pilot/clean_train_subsample.csv and reused by every condition,
    including a **retrained B0**. The published B0 checkpoint is NOT the comparison
    point -- it was trained on all 78k rows by a different pipeline and selected on
    accuracy, so comparing against it would confound "augmentation helped" with
    "our training pipeline differs". Retraining B0 here makes the five conditions
    differ only in their training data.
  * Augmentation ratio r is identical across B1-B4 (article_plan.md section 12), as
    are the candidate-pool caps (--max-tokens/--max-candidates), so the conditions
    differ only in the SELECTION rule.
  * B3/B4 score candidates against the retrained B0 -- i.e. M_0 = Train(D), matching
    article_plan.md section 10's offline adversarial augmentation.
  * Attacks are evaluated on the first N test examples (default 400) of the same
    seeded test load, so every condition sees identical examples.
  * Evaluation is ordered ATTACK-MAJOR (all conditions under TextFooler, then
    WSD-TextFooler, then BERT-Attack) so that if the run is cut short, the completed
    part is still a full cross-condition comparison rather than a few complete
    conditions and nothing for the rest.

Every step runs as its own subprocess (frees GPU memory between stages) and is
skipped if its output already exists, so the pilot is resumable after a crash.

Usage:
    python scripts/run_pilot.py                 # full pilot
    python scripts/run_pilot.py --dry-run       # print the plan and exit
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from augmentation._common import DEFAULT_FASTTEXT  # noqa: E402
PYTHON = "/home/mudryi/phd_projects/ukr-synonym-robustness/dev_env/bin/python3"

STRATEGY_FOR_CONDITION = {
    "B1": "random",
    "B2": "wsd",
    "B3": "adversarial",
    "B4": "wsd_adversarial",
    "B5": "anti_adversarial",   # RQ3 control: argmin confidence drop
    "B6": "mlm_random",         # BERT-Attack-family distribution, random selection
    "B7": "mlm_adversarial",    # BERT-Attack-family distribution, argmax drop
}
# Strategies that must be generated AFTER B0 exists, because they score candidates
# against it (M_0 = Train(D)).
MODEL_DEPENDENT = ("B3", "B4", "B5", "B7")
MODEL_INDEPENDENT = ("B1", "B2", "B6")
AUGMENTED_CONDITIONS = MODEL_INDEPENDENT + MODEL_DEPENDENT
NCLASSES = {"reviews": 5, "news": 5, "unlp": 2}


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


def run_step(name: str, argv: list[str], log_dir: Path, dry_run: bool) -> bool:
    """Run one pipeline step, streaming its output to log_dir/<name>.log."""
    if dry_run:
        log(f"DRY-RUN {name}: {' '.join(argv)}")
        return True

    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{name}.log"
    log(f"START {name}  (log: {log_path})")
    started = time.time()
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(" ".join(argv) + "\n\n")
        f.flush()
        proc = subprocess.run(argv, stdout=f, stderr=subprocess.STDOUT, cwd=PROJECT_ROOT)
    elapsed = time.time() - started
    if proc.returncode != 0:
        log(f"FAILED {name} after {elapsed/60:.1f} min (exit {proc.returncode}) -- see {log_path}")
        return False
    log(f"DONE  {name} in {elapsed/60:.1f} min")
    return True


def read_best_macro_f1(log_path: Path) -> float | None:
    """Pull the `best eval macro_f1: X` line that train_augmented.py prints last."""
    if not log_path.exists():
        return None
    best = None
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "best eval macro_f1:" in line:
            try:
                best = float(line.split("best eval macro_f1:")[1].strip())
            except (IndexError, ValueError):
                continue
    return best


def make_subsample(dataset: str, cfg: dict, out_csv: Path, n: int, seed: int, dry_run: bool) -> None:
    """Deterministic clean-train subsample, written in the dataset's NATIVE schema so
    both generate_augmented_dataset.py (--train-csv) and train_augmented.py
    (--clean-csv) can read it with their existing loaders."""
    if out_csv.exists():
        log(f"SKIP subsample (exists: {out_csv})")
        return
    if dry_run:
        log(f"DRY-RUN subsample -> {out_csv} (n={n}, seed={seed})")
        return
    df = pd.read_csv(cfg["train-path"])
    if n < len(df):
        df = df.sample(n=n, random_state=seed)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    log(f"wrote clean subsample: {out_csv} ({len(df)} rows of {cfg['train-path']})")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", default="reviews", choices=["reviews", "news", "unlp"])
    p.add_argument("--model", default="xlmr_base", choices=["ukr_roberta", "xlmr_base"])
    p.add_argument("--seed", type=int, default=1914)
    p.add_argument("--clean-n", type=int, default=20000, help="Clean train subsample size.")
    p.add_argument("--ratio", type=float, default=0.5, help="|D_aug| / |D_train_subsample|.")
    p.add_argument("--max-tokens", type=int, default=3)
    p.add_argument("--max-candidates", type=int, default=6)
    p.add_argument("--eval-n", type=int, default=400, help="Test examples per attack cell.")
    p.add_argument("--num-epochs", type=int, default=3)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--lr", type=float, default=2e-5)
    p.add_argument("--grad-accum-steps", type=int, default=2)
    p.add_argument("--eval-every", type=int, default=200)
    p.add_argument("--eval-limit", type=int, default=None,
                   help="Cap rows used for the in-training eval/checkpoint-selection split "
                        "(smoke runs only; the full split is what makes macro-F1 selection "
                        "meaningful).")
    p.add_argument("--early-stopping", type=int, default=6)
    p.add_argument("--conditions", default="B0,B1,B2,B3,B4")
    p.add_argument("--variant", default="",
                   help="Ablation tag (e.g. pool10x20, r0.25). Folded into the augmented-data, "
                        "checkpoint and attack-cell names so an ablation can reuse a seed's "
                        "clean subsample and B0 without colliding with the main grid. A "
                        "variant that omits B0 from --conditions borrows (and never renames) "
                        "the main grid's baseline, so every such ablation is compared against "
                        "the identical B0.")
    p.add_argument("--min-baseline-macro-f1", type=float, default=0.28,
                   help="Abort if the retrained B0 baseline underfits below this eval "
                        "macro-F1 (majority-class collapse on Reviews is ~0.19; the "
                        "published full-data XLM-R baseline is 0.475).")
    p.add_argument("--fasttext-path", default=DEFAULT_FASTTEXT,
                   help="Ukrainian fastText vectors (BERT-Attack + MLM augmentation).")
    p.add_argument("--mlm-model", default=None,
                   help="fill-mask model for B6/B7; defaults to run_attack.py's xlm-roberta-large.")
    p.add_argument("--skip-bert-attack", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--pilot-root", default=None,
                   help="Where subsample/augmented/checkpoints/logs live. Defaults to "
                        "results/pilot_seed<seed>, so a bare run reuses that seed's existing "
                        "clean subsample and B0 instead of silently retraining a second "
                        "baseline. Override to run an isolated smoke test.")
    p.add_argument("--results-root", default="results",
                   help="Where attack cells are written and aggregated from.")
    args = p.parse_args(argv)

    conditions = [c.strip() for c in args.conditions.split(",") if c.strip()]
    if args.pilot_root is None:
        args.pilot_root = f"results/pilot_seed{args.seed}"
    pilot_root = PROJECT_ROOT / args.pilot_root
    results_root = PROJECT_ROOT / args.results_root
    log_dir = pilot_root / "logs"
    manifest_path = pilot_root / "manifest.json"

    with open(PROJECT_ROOT / "configs" / f"{args.dataset}.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    hf_name = cfg["models"][args.model]["hf-name"]

    clean_csv = pilot_root / "clean_train_subsample.csv"
    tag = f"{args.dataset}__{args.model}__seed{args.seed}"

    def _suffix(condition: str) -> str:
        """A variant run that does NOT list B0 in --conditions is BORROWING the main
        grid's baseline, so B0's checkpoint and cells must keep their unsuffixed names
        (aggregate_results.py then inherits that B0 into the variant's comparison
        group). A variant run that DOES train its own B0 -- e.g. the full-78k re-run,
        whose baseline is genuinely a different model -- suffixes it like everything
        else, or it would silently overwrite the main grid's baseline cells."""
        if not args.variant:
            return ""
        if condition == "B0" and "B0" not in conditions:
            return ""
        return f"__{args.variant}"

    def aug_dir(condition: str) -> Path:
        return pilot_root / "augmented" / f"{tag}__{condition}__r{args.ratio}{_suffix(condition)}"

    def ckpt_dir(condition: str) -> Path:
        name = f"{args.dataset}__{args.model}__{condition}__seed{args.seed}{_suffix(condition)}"
        return pilot_root / "checkpoints" / name

    def cell_dir(condition: str, attack: str, wsd: bool) -> Path:
        name = (f"{args.dataset}__{args.model}__{condition}__seed{args.seed}"
                f"{_suffix(condition)}" + ("__wsd035" if wsd else ""))
        return results_root / attack / name

    log("=" * 78)
    log(f"Stage-A pilot: {args.dataset} x {args.model} x seed {args.seed}")
    log(f"clean_n={args.clean_n} ratio={args.ratio} caps=({args.max_tokens},{args.max_candidates}) "
        f"eval_n={args.eval_n} conditions={conditions}")
    log("=" * 78)

    make_subsample(args.dataset, cfg, clean_csv, args.clean_n, args.seed, args.dry_run)

    statuses: dict[str, str] = {}

    def record(step: str, ok: bool) -> None:
        statuses[step] = "ok" if ok else "failed"
        if not args.dry_run:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump({"config": vars(args), "steps": statuses,
                           "updated": datetime.now().isoformat()}, f, indent=2)

    def train_condition(condition: str) -> bool:
        out = ckpt_dir(condition)
        if (out / "TRAINING_COMPLETE").exists():
            log(f"SKIP train {condition} (finished checkpoint: {out})")
            statuses[f"train_{condition}"] = "skipped"
            return True
        if (out / "model.safetensors").exists():
            # Weights without the marker = training was interrupted partway. The
            # checkpoint is loadable but undertrained, so retrain rather than let it
            # quietly become one condition's result.
            log(f"RETRAIN {condition}: checkpoint exists but training never finished "
                f"(no TRAINING_COMPLETE marker in {out})")
        argv_train = [
            PYTHON, "scripts/train_augmented.py",
            "--dataset", args.dataset, "--model", args.model,
            "--condition", condition, "--seed", str(args.seed),
            "--clean-csv", str(clean_csv),
            "--batch-size", str(args.batch_size), "--lr", str(args.lr),
            "--num-epochs", str(args.num_epochs),
            "--grad-accum-steps", str(args.grad_accum_steps),
            "--eval-every", str(args.eval_every),
            "--early-stopping", str(args.early_stopping),
            "--no-wandb", "--output-dir", str(out),
        ]
        if args.eval_limit is not None:
            argv_train += ["--eval-limit", str(args.eval_limit)]
        if condition != "B0":
            argv_train += ["--augmented-csv", str(aug_dir(condition) / "augmented.csv")]
        ok = run_step(f"train_{condition}", argv_train, log_dir, args.dry_run)
        record(f"train_{condition}", ok)
        return ok

    def generate_condition(condition: str) -> bool:
        out = aug_dir(condition)
        if (out / "augmented.csv").exists() and (out / "meta.json").exists():
            log(f"SKIP generate {condition} (exists: {out})")
            statuses[f"generate_{condition}"] = "skipped"
            return True
        strategy = STRATEGY_FOR_CONDITION[condition]
        argv_gen = [
            PYTHON, "scripts/generate_augmented_dataset.py",
            "--dataset", args.dataset, "--strategy", strategy,
            "--train-csv", str(clean_csv),
            "--ratio", str(args.ratio), "--seed", str(args.seed),
            "--max-tokens", str(args.max_tokens), "--max-candidates", str(args.max_candidates),
            "--output-dir", str(out),
        ]
        if condition in MODEL_DEPENDENT:
            argv_gen += [
                "--target-model", hf_name,
                "--target-checkpoint", str(ckpt_dir("B0")),
                "--nclasses", str(NCLASSES[args.dataset]),
            ]
        if strategy.startswith("mlm_"):
            argv_gen += ["--fasttext-path", args.fasttext_path]
            if args.mlm_model:
                argv_gen += ["--mlm-model", args.mlm_model]
        ok = run_step(f"generate_{condition}", argv_gen, log_dir, args.dry_run)
        record(f"generate_{condition}", ok)
        return ok

    def evaluate_cell(condition: str, attack_key: str) -> bool:
        wsd = attack_key == "textfooler_wsd"
        attack_dir_name = "bert_attack" if attack_key == "bert_attack" else "textfooler"
        cell = cell_dir(condition, attack_dir_name, wsd)
        step = f"eval_{condition}_{attack_key}"
        if (cell / "summary.json").exists():
            log(f"SKIP {step} (exists: {cell})")
            statuses[step] = "skipped"
            return True
        argv_eval = [
            PYTHON, "scripts/evaluate_robustness.py",
            "--dataset", args.dataset, "--model", args.model,
            "--condition", condition, "--seed", str(args.seed),
            "--checkpoint", str(ckpt_dir(condition)),
            "--n-samples", str(args.eval_n),
            "--only", attack_key,
            "--results-root", str(results_root),
        ]
        if args.variant:
            argv_eval += ["--variant", args.variant]
        ok = run_step(step, argv_eval, log_dir, args.dry_run)
        record(step, ok)
        return ok

    # ---- Phase 1: baseline must exist first (B3/B4 score candidates against it) ----
    if "B0" in conditions and not train_condition("B0"):
        log("ABORT: baseline B0 training failed; B3/B4 generation depends on it")
        return 1

    # Guard against an underfit baseline. A model that collapses to the majority class
    # scores macro-F1 ~0.19 on Reviews and makes every attack trivially fail, which
    # would make all five conditions look identical -- i.e. a wasted run. Fail loudly
    # now instead of producing a degenerate table hours later.
    if "B0" in conditions and not args.dry_run:
        baseline_f1 = read_best_macro_f1(log_dir / "train_B0.log")
        if baseline_f1 is None:
            log("WARNING: could not read B0's best macro-F1 from its log; continuing anyway")
        elif baseline_f1 < args.min_baseline_macro_f1:
            log(f"ABORT: baseline B0 macro-F1 {baseline_f1:.3f} < "
                f"{args.min_baseline_macro_f1} -- the baseline underfit, so the whole "
                f"comparison would be degenerate. Raise --num-epochs/--lr and rerun "
                f"(delete {ckpt_dir('B0')} first).")
            record("baseline_sanity_check", False)
            return 1
        else:
            log(f"baseline sanity check OK: B0 eval macro-F1 = {baseline_f1:.3f}")
            record("baseline_sanity_check", True)

    # ---- Phase 2: model-independent augmentation (B1 random, B2 WSD, B6 MLM-random) ----
    for condition in [c for c in MODEL_INDEPENDENT if c in conditions]:
        generate_condition(condition)

    # ---- Phase 3: model-dependent augmentation (B3, B4, B5, B7) against B0 ----
    for condition in [c for c in MODEL_DEPENDENT if c in conditions]:
        generate_condition(condition)

    # ---- Phase 4: train the augmented conditions ----
    for condition in [c for c in AUGMENTED_CONDITIONS if c in conditions]:
        if (aug_dir(condition) / "augmented.csv").exists() or args.dry_run:
            train_condition(condition)
        else:
            log(f"SKIP train {condition}: no augmented data (generation failed?)")
            record(f"train_{condition}", False)

    # ---- Phase 5: evaluation, attack-major ordering ----
    attack_keys = ["textfooler", "textfooler_wsd"]
    if not args.skip_bert_attack:
        attack_keys.append("bert_attack")
    for attack_key in attack_keys:
        for condition in conditions:
            if (ckpt_dir(condition) / "model.safetensors").exists() or args.dry_run:
                evaluate_cell(condition, attack_key)
            else:
                log(f"SKIP eval {condition} {attack_key}: no checkpoint")

    # ---- Phase 6: aggregate ----
    run_step("aggregate", [
        PYTHON, "scripts/aggregate_results.py",
        "--root", str(results_root),
        "--out", str(results_root / "pilot_metrics"),
    ], log_dir, args.dry_run)

    log("=" * 78)
    log("PILOT COMPLETE")
    for step, status in statuses.items():
        log(f"  {step}: {status}")
    log(f"metrics table: {results_root / 'pilot_metrics.md'}")
    log("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
