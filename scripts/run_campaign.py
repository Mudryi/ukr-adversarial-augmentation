"""Campaign orchestrator: the full sequence of experiments that turns the Stage-A
pilot's directional findings into claims that survive review.

The pilot (2026-09-13) established, on ONE training run and 400 eval examples, that
WSD filtering rescues naive augmentation (RQ2), that adversarial selection is the
strongest condition (RQ3), that SAAA does not beat plain adversarial selection, and
that nothing transfers to BERT-Attack (RQ4). None of that is claimable yet: a single
seed measures no training-run variance, and 400 examples can only detect
|delta cASR| >= 0.058 -- wider than most of the gaps of interest.

This campaign addresses that, plus the three open questions the pilot raised:

  S1  Three seeds of the main grid, at 1500 eval examples. Turns every existing
      finding into a mean-with-range instead of a point estimate, and adds B5, the
      argmin-confidence-drop control: if the LEAST adversarial substitution also
      improves robustness, RQ3's interpretation is wrong.
  S2  The MLM conditions (B6/B7), which augment from the distribution BERT-Attack
      samples from. RQ4 currently tests one direction only; this completes the matrix.
  S3  Pool-size ablation. The pilot capped candidates at 3 tokens x 6 -- a regime in
      which adversarial selection has little room to pick sense-violating
      substitutions, i.e. little for the WSD filter to fix. If SAAA never separates
      from B3 even at 10 x 20, that is a real finding about the method.
  S4  Augmentation-ratio ablation (r = 0.25, 1.0 against the pilot's 0.5).
  S5  Full 78k training set instead of the 20k subsample.
  S6  Generality: second architecture (Ukr-RoBERTa) and second/third dataset.

Each stage is one `run_pilot.py` invocation, which is itself resumable step-by-step,
so this script only needs to track which stages have finished. Interrupting it is
safe: rerunning picks up at the first unfinished stage, and `run_pilot.py` skips the
steps inside that stage whose outputs already exist.

Stages within a seed SHARE a pilot root, so the clean subsample and the B0 baseline
are trained once per seed and reused by every later stage for that seed (see
run_pilot.py --variant).

Usage:
    python scripts/run_campaign.py --list          # show the queue and exit
    python scripts/run_campaign.py --smoke         # tiny end-to-end test of new code
    python scripts/run_campaign.py                 # run the whole campaign
    python scripts/run_campaign.py --only S1_main_seed1914
    python scripts/run_campaign.py --from S3_pool_seed1914
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON = "/home/mudryi/phd_projects/ukr-synonym-robustness/dev_env/bin/python3"

SEEDS = [1914, 2024, 7]
EVAL_N = "1500"          # up from the pilot's 400: min detectable |delta cASR| ~0.058 -> ~0.030
NUM_EPOCHS = "4"
MAIN_CONDITIONS = "B0,B1,B2,B3,B4,B5"

# Weight files worth deleting when a checkpoint is pruned; the config/tokenizer JSONs
# stay so a pruned directory still documents what was trained.
WEIGHT_FILES = ("model.safetensors", "pytorch_model.bin")


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


def reviews_base() -> list[str]:
    return ["--dataset", "reviews", "--model", "xlmr_base",
            "--eval-n", EVAL_N, "--num-epochs", NUM_EPOCHS]


def seed_root(seed: int) -> str:
    return f"results/pilot_seed{seed}"


def build_stages() -> list[dict]:
    stages: list[dict] = []

    # ---- S1: main grid, three seeds. Trains each seed's B0, which every later
    # stage for that seed borrows. ----
    for seed in SEEDS:
        stages.append({
            "name": f"S1_main_seed{seed}",
            "desc": f"Main grid B0-B5, seed {seed} (adds the argmin control B5)",
            "argv": reviews_base() + [
                "--seed", str(seed), "--pilot-root", seed_root(seed),
                "--conditions", MAIN_CONDITIONS,
            ],
        })

    # ---- S2: MLM family. Borrows each seed's B0 (B0 not in --conditions). ----
    for seed in SEEDS:
        stages.append({
            "name": f"S2_mlm_seed{seed}",
            "desc": f"MLM-distribution conditions B6/B7, seed {seed} (completes RQ4)",
            "argv": reviews_base() + [
                "--seed", str(seed), "--pilot-root", seed_root(seed),
                "--conditions", "B6,B7",
            ],
        })

    # ---- S3: pool-size ablation. Seed 1914 first -- it answers the SAAA question on
    # its own; the other two seeds are queued at the very end, since they only add
    # variance estimates to a question S4-S6 do not depend on. ----
    def pool_stage(seed: int) -> dict:
        return {
            "name": f"S3_pool_seed{seed}",
            "desc": f"Pool-size ablation 10x20 (B3/B4/B5), seed {seed}",
            "argv": reviews_base() + [
                "--seed", str(seed), "--pilot-root", seed_root(seed),
                "--variant", "pool10x20", "--max-tokens", "10", "--max-candidates", "20",
                "--conditions", "B3,B4,B5",
            ],
        }

    stages.append(pool_stage(SEEDS[0]))

    # ---- S4: augmentation-ratio ablation, seed 1914 ----
    for ratio, label in ((0.25, "r0.25"), (1.0, "r1.0")):
        stages.append({
            "name": f"S4_ratio_{label}",
            "desc": f"Augmentation ratio r={ratio} (B2/B3/B4), seed {SEEDS[0]}",
            "argv": reviews_base() + [
                "--seed", str(SEEDS[0]), "--pilot-root", seed_root(SEEDS[0]),
                "--variant", label, "--ratio", str(ratio),
                "--conditions", "B2,B3,B4",
            ],
        })

    # ---- S5: full 78k train. Its own root AND its own B0 (a genuinely different
    # baseline), so run_pilot.py suffixes the baseline too. ----
    stages.append({
        "name": "S5_full78k",
        "desc": "Full 78k train split instead of the 20k subsample (B0/B2/B3/B4)",
        "argv": reviews_base() + [
            "--seed", str(SEEDS[0]), "--pilot-root", "results/pilot_full78k",
            "--variant", "full78k", "--clean-n", "78146",
            "--conditions", "B0,B2,B3,B4",
        ],
        "prune": True,
    })

    # ---- S6: generality. Each cell names a different dataset/model, so no variant
    # tag is needed to keep them apart. The baseline guard is dataset-specific:
    # majority-class collapse scores ~0.19 macro-F1 on 5-class Reviews but much
    # higher on binary UNLP, so a single threshold would not catch an underfit run. ----
    for name, extra, guard in (
        ("ukrroberta_reviews",
         ["--dataset", "reviews", "--model", "ukr_roberta",
          "--pilot-root", "results/pilot_ukrroberta_reviews"], "0.28"),
        ("news",
         ["--dataset", "news", "--model", "xlmr_base",
          "--pilot-root", "results/pilot_news"], "0.50"),
        ("unlp",
         ["--dataset", "unlp", "--model", "xlmr_base",
          "--pilot-root", "results/pilot_unlp"], "0.50"),
    ):
        stages.append({
            "name": f"S6_scale_{name}",
            "desc": f"Scale to {name} (B0/B2/B3/B4), seed {SEEDS[0]}",
            "argv": extra + [
                "--eval-n", EVAL_N, "--num-epochs", NUM_EPOCHS,
                "--seed", str(SEEDS[0]), "--conditions", "B0,B2,B3,B4",
                "--min-baseline-macro-f1", guard,
            ],
            "prune": True,
        })

    # ---- S3 continued: remaining seeds, last (see pool_stage) ----
    for seed in SEEDS[1:]:
        stages.append({**pool_stage(seed), "prune": True})

    stages += build_followup_stages()
    return stages


def build_followup_stages() -> list[dict]:
    """Round 2, added 2026-09-18 after the first 15 stages completed.

    The 3-seed main grid is settled and needs no more compute. What is not settled is
    everything that ran at a single seed -- which is where the three largest effects in
    the project live. Worse, inventorying them turned up that the largest, the full-78k
    result, is flagged for prediction collapse (its B3 loses 0.057 eval macro-F1 and
    concentrates 78.7% of predictions on the majority class, which lowers cASR without
    improving robustness). These stages reseed the single-seed claims, hardest-hitting
    uncertainty first.
    """
    stages: list[dict] = []
    extra_seeds = SEEDS[1:]  # 2024, 7 -- seed 1914 already ran for all of these

    # R1: does full-data training degenerate systematically, or was that one seed?
    # Decisive diagnostic afterwards: majority_pred_share across all three seeds.
    for seed in extra_seeds:
        stages.append({
            "name": f"R1_full78k_seed{seed}",
            "desc": f"Full 78k reseed, seed {seed} (tests the prediction-collapse confound)",
            "argv": reviews_base() + [
                "--seed", str(seed), "--pilot-root", "results/pilot_full78k",
                "--variant", "full78k", "--clean-n", "78146",
                "--conditions", "B0,B2,B3,B4",
            ],
            "prune": True,
        })

    # R2: the strongest generality effect (-0.227) is single-seed, and the B5 control has
    # never been run on a second architecture -- so the *mechanism* is one-architecture too.
    stages.append({
        "name": "R2_ukrroberta_B5_seed1914",
        "desc": "B5 control on Ukr-RoBERTa, seed 1914 (borrows the existing B0)",
        "argv": ["--dataset", "reviews", "--model", "ukr_roberta",
                 "--pilot-root", "results/pilot_ukrroberta_reviews",
                 "--eval-n", EVAL_N, "--num-epochs", NUM_EPOCHS,
                 "--seed", str(SEEDS[0]), "--conditions", "B5",
                 "--min-baseline-macro-f1", "0.28"],
    })
    for seed in extra_seeds:
        stages.append({
            "name": f"R2_ukrroberta_seed{seed}",
            "desc": f"Ukr-RoBERTa reseed + B5 control, seed {seed}",
            "argv": ["--dataset", "reviews", "--model", "ukr_roberta",
                     "--pilot-root", "results/pilot_ukrroberta_reviews",
                     "--eval-n", EVAL_N, "--num-epochs", NUM_EPOCHS,
                     "--seed", str(seed), "--conditions", "B0,B2,B3,B4,B5",
                     "--min-baseline-macro-f1", "0.28"],
            "prune": True,
        })

    # R3: UNLP is currently *inconclusive* (every paired p non-significant at one seed),
    # not the negative case the earlier write-up claimed.
    for seed in extra_seeds:
        stages.append({
            "name": f"R3_unlp_seed{seed}",
            "desc": f"UNLP reseed, seed {seed} (inconclusive -> real answer)",
            "argv": ["--dataset", "unlp", "--model", "xlmr_base",
                     "--pilot-root", "results/pilot_unlp",
                     "--eval-n", EVAL_N, "--num-epochs", NUM_EPOCHS,
                     "--seed", str(seed), "--conditions", "B0,B2,B3,B4",
                     "--min-baseline-macro-f1", "0.50"],
            "prune": True,
        })

    # R4: r=1.0 beat r=0.5 for every condition on one seed; if it replicates, the
    # recommended configuration changes.
    for seed in extra_seeds:
        stages.append({
            "name": f"R4_ratio_r1.0_seed{seed}",
            "desc": f"Augmentation ratio r=1.0 reseed, seed {seed}",
            "argv": reviews_base() + [
                "--seed", str(seed), "--pilot-root", seed_root(seed),
                "--variant", "r1.0", "--ratio", "1.0",
                "--conditions", "B2,B3,B4",
            ],
            "prune": True,
        })

    return stages


def build_smoke_stages() -> list[dict]:
    """Tiny end-to-end exercise of every code path this campaign adds, in an isolated
    root. 60 clean rows, 20 eval examples, 1 epoch -- the numbers are meaningless; the
    point is that nothing crashes and the new conditions produce sane augmented text."""
    root = "results/smoke_campaign"
    base = [
        "--dataset", "reviews", "--model", "xlmr_base",
        "--clean-n", "60", "--ratio", "0.5", "--eval-n", "20",
        "--num-epochs", "1", "--eval-every", "1", "--eval-limit", "40",
        "--early-stopping", "99", "--min-baseline-macro-f1", "0.0",
        "--seed", "1914",
        "--pilot-root", f"{root}/pilot", "--results-root", f"{root}/results",
    ]
    return [
        {"name": "smoke_all_conditions",
         "desc": "B0-B7 end-to-end, including the argmin control and both MLM paths",
         "argv": base + ["--conditions", "B0,B1,B2,B3,B4,B5,B6,B7"]},
        {"name": "smoke_variant",
         "desc": "--variant naming + borrowed-B0 inheritance in the aggregator",
         "argv": base + ["--conditions", "B3", "--variant", "pool4x8",
                         "--max-tokens", "4", "--max-candidates", "8"]},
    ]


def prune_checkpoints(argv: list[str]) -> None:
    """Delete the weight files of augmented-condition checkpoints whose attack cells
    are all on disk. B0 is never pruned -- later stages score candidates against it."""
    def flag(name: str, default: str | None = None) -> str | None:
        return argv[argv.index(name) + 1] if name in argv else default

    pilot_root = PROJECT_ROOT / (flag("--pilot-root") or "results/pilot")
    results_root = PROJECT_ROOT / (flag("--results-root") or "results")
    ckpt_root = pilot_root / "checkpoints"
    if not ckpt_root.is_dir():
        return

    for ckpt in sorted(ckpt_root.iterdir()):
        if not ckpt.is_dir() or "__B0__" in ckpt.name:
            continue
        cells = [results_root / "textfooler" / ckpt.name,
                 results_root / "textfooler" / f"{ckpt.name}__wsd035",
                 results_root / "bert_attack" / ckpt.name]
        if not all((c / "summary.json").exists() for c in cells):
            continue
        removed = 0
        for weight in WEIGHT_FILES:
            f = ckpt / weight
            if f.exists():
                removed += f.stat().st_size
                f.unlink()
        if removed:
            (ckpt / "PRUNED").write_text(
                f"weights deleted {datetime.now().isoformat()} after all attack cells "
                f"were written; retrain to restore\n", encoding="utf-8")
            log(f"  pruned {ckpt.name} (freed {removed / 1e9:.1f} GB)")


def load_manifest(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"stages": {}}


def save_manifest(path: Path, manifest: dict) -> None:
    manifest["updated"] = datetime.now().isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="Print the stage queue and exit.")
    p.add_argument("--smoke", action="store_true", help="Run the isolated smoke stages instead.")
    p.add_argument("--only", action="append", default=None, help="Run only these stages. Repeatable.")
    p.add_argument("--from", dest="from_stage", default=None, help="Start at this stage.")
    p.add_argument("--force", action="store_true", help="Rerun stages already marked ok.")
    p.add_argument("--prune-checkpoints", action="store_true",
                   help="Also prune stages not marked prune-by-default (frees ~1.1GB each).")
    p.add_argument("--dry-run", action="store_true", help="Print each stage's command without running.")
    p.add_argument("--manifest", default="results/campaign_manifest.json")
    args = p.parse_args(argv)

    stages = build_smoke_stages() if args.smoke else build_stages()
    manifest_path = PROJECT_ROOT / (
        "results/smoke_campaign/manifest.json" if args.smoke else args.manifest
    )

    if args.only:
        wanted = set(args.only)
        unknown = wanted - {s["name"] for s in stages}
        if unknown:
            sys.exit(f"unknown stage(s): {', '.join(sorted(unknown))}")
        stages = [s for s in stages if s["name"] in wanted]
    if args.from_stage:
        names = [s["name"] for s in stages]
        if args.from_stage not in names:
            sys.exit(f"unknown stage: {args.from_stage}")
        stages = stages[names.index(args.from_stage):]

    if args.list:
        for i, s in enumerate(stages, 1):
            print(f"{i:2d}. {s['name']:26s} {s['desc']}")
            print(f"    run_pilot.py {' '.join(s['argv'])}")
        return 0

    manifest = load_manifest(manifest_path)
    log("=" * 78)
    log(f"CAMPAIGN {'(smoke)' if args.smoke else ''}: {len(stages)} stage(s)")
    log("=" * 78)

    log_dir = PROJECT_ROOT / ("results/smoke_campaign/logs" if args.smoke else "results/campaign_logs")
    campaign_started = time.time()
    failures = []

    for i, stage in enumerate(stages, 1):
        name = stage["name"]
        prior = manifest["stages"].get(name, {})
        if prior.get("status") == "ok" and not args.force:
            log(f"[{i}/{len(stages)}] SKIP {name} (already ok on {prior.get('finished', '?')})")
            continue

        cmd = [PYTHON, "scripts/run_pilot.py", *stage["argv"]]
        if args.dry_run:
            log(f"[{i}/{len(stages)}] DRY-RUN {name}: {' '.join(cmd)}")
            continue

        log_dir.mkdir(parents=True, exist_ok=True)
        stage_log = log_dir / f"{name}.log"
        log(f"[{i}/{len(stages)}] START {name} -- {stage['desc']}")
        log(f"            log: {stage_log}")
        started = time.time()
        with open(stage_log, "w", encoding="utf-8") as f:
            f.write(" ".join(cmd) + "\n\n")
            f.flush()
            proc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=PROJECT_ROOT)
        minutes = (time.time() - started) / 60

        ok = proc.returncode == 0
        manifest["stages"][name] = {
            "status": "ok" if ok else "failed",
            "returncode": proc.returncode,
            "minutes": round(minutes, 1),
            "finished": datetime.now().isoformat(),
            "argv": stage["argv"],
        }
        save_manifest(manifest_path, manifest)

        if ok:
            log(f"[{i}/{len(stages)}] DONE  {name} in {minutes / 60:.1f} h")
            if stage.get("prune") or args.prune_checkpoints:
                prune_checkpoints(stage["argv"])
        else:
            # Keep going: a later stage rarely depends on an earlier one (only S2-S4
            # need their seed's B0 from S1), and a 4-day queue should not be lost to
            # one bad cell. Failures are reported at the end.
            failures.append(name)
            log(f"[{i}/{len(stages)}] FAILED {name} after {minutes / 60:.1f} h "
                f"(exit {proc.returncode}) -- see {stage_log}; continuing")

    log("=" * 78)
    log(f"CAMPAIGN COMPLETE in {(time.time() - campaign_started) / 3600:.1f} h")
    for name, info in manifest["stages"].items():
        log(f"  {name}: {info['status']} ({info.get('minutes', 0) / 60:.1f} h)")
    if failures:
        log(f"FAILED STAGES: {', '.join(failures)}")
    log(f"manifest: {manifest_path}")
    log("=" * 78)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
