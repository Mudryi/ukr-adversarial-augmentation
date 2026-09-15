# ukr-adversarial-augmentation

Follow-up to the *Precision vs. Perturbation* (UNLP 2025) attack/WSD work. This project asks:

> Can automatically generated, sense-aware synonym augmentation improve the robustness of
> Ukrainian text classifiers without sacrificing clean accuracy?

See [`CURRENT_STATE.md`](CURRENT_STATE.md) for the inventory of what exists (reused assets +
what this project built), and [`RESEARCH_PLAN.md`](RESEARCH_PLAN.md) for the research questions,
training conditions, metrics, staged plan, and **results**. The full narrative version of the
plan this was distilled from is `article_plan.md` (in this folder).

## Status — 7 of 15 campaign stages done (2026-09-15)

XLM-R + UA Reviews, seeds 1914/2024/7, conditions B0–B7, each attacked by TextFooler,
WSD-TextFooler and BERT-Attack. **These supersede the single-seed Stage-A pilot.**

- **The anti-adversarial control settles RQ3.** B5 — same candidate pool, but picking the
  *least* confidence-reducing substitution — is far worse than no augmentation at all
  (+0.169 cASR vs baseline, 3/3 seeds, p < 0.0001). The *direction* of adversarial selection
  is the mechanism, not the act of perturbing training data.
- **SAAA (B4) is the best condition, and the pilot had it backwards.** B4 improves on
  baseline in **every** seed (mean cASR 0.296 vs 0.387) with a seed range of 0.020. Plain
  adversarial selection (B3) wins on only 2/3 seeds with a range of 0.152 — wider than its
  own advantage. Sense filtering buys *reliability*.
- **Why it works** (pool ablation): B3 and B4 are indistinguishable at small candidate pools
  (p = 1.00 at 3×6) but diverge sharply when the adversarial search gets room (−0.068,
  p < 0.0001 at 10×20). The WSD filter is a safeguard on search width — it blocks the
  meaning-destroying substitutions a wider search turns up.
- **RQ4 answered in both directions, and it is a negative.** Each augmentation family helps
  only against its own attack family: B4 is best against TextFooler and *worse* than baseline
  against BERT-Attack, while the MLM-based B7 is the only condition that beats baseline
  against BERT-Attack (3/3 seeds) and does nothing against TextFooler.
- **"Naive augmentation hurts" did not replicate** (B1 vs B0 pooled p = 0.43) — that pilot
  finding was seed noise.
- **No clean-performance cost**: accuracy 0.763–0.778, eval macro-F1 0.484–0.503 throughout.

Full numbers and caveats: `RESEARCH_PLAN.md` → "Campaign results". Tables:
`results/pilot_metrics_by_seed.md`, `results/pilot_metrics_paired.csv`.

## Status — campaign running (launched 2026-09-13)

`scripts/run_campaign.py` queues ~100 h of GPU across 15 resumable stages. Done: S1 (3-seed
main grid), S2 (MLM family, 3 seeds), S3 (pool ablation, seed 1914). Remaining: the
augmentation-ratio ablation, the full-78k re-run, three cross-dataset/architecture runs, and
the two remaining pool-ablation seeds. Live state: `results/campaign_manifest.json`. See `RESEARCH_PLAN.md` → "Campaign" for the queue and its decision points.

## Running it

Use the `ukr-synonym-robustness` venv — the default `python3` lacks pymorphy2/sklearn:

```bash
PY=/home/mudryi/phd_projects/ukr-synonym-robustness/dev_env/bin/python3

$PY scripts/run_campaign.py --list        # the stage queue and its exact commands
$PY scripts/run_campaign.py --smoke       # tiny end-to-end test of every code path
$PY scripts/run_campaign.py               # the whole campaign (~100h, resumable)
$PY scripts/run_pilot.py --dry-run        # one stage's pipeline, without executing
$PY scripts/aggregate_results.py --root results --out results/pilot_metrics
```

### Pausing and resuming

Stop the whole campaign by killing its process group:

```bash
kill -TERM -$(ps -o pgid= -p $(pgrep -f run_campaign.py | head -1) | tr -d ' ')
```

Resume with the identical launch command — completed stages are read from
`results/campaign_manifest.json` and skipped, and within the interrupted stage every
finished step is skipped too. Resumption is step-level, keyed on each step's output:
`summary.json` for an attack cell, `TRAINING_COMPLETE` for a checkpoint (weights alone are
not enough — they are rewritten at every improving eval round, so a killed training leaves a
loadable but undertrained model, which is retrained with a logged warning), and
`augmented.csv` + `meta.json` for generated data.

Only the step in flight is lost: under ~40 min in almost every case, the exception being
B4 generation at the 10x20 pool in stage S3 (~4.6 h).

Both orchestrators skip work whose output already exists, so interrupting and rerunning
resumes rather than restarting. For an unattended run, detach it:
`setsid nohup $PY scripts/run_campaign.py > results/campaign.log 2>&1 < /dev/null &`.
Progress: `results/campaign_manifest.json` and `results/campaign_logs/<stage>.log`.

## Reuse strategy — do not copy, reference

This repo is deliberately thin. Nearly everything it needs already exists in sibling projects:

- **Attacks, WSD filter, synonym dictionary, morphological inflection, attack-level metrics** —
  live in `../ukr-synonym-robustness/src/`. Treat it as a local dependency:
  ```bash
  pip install -e ../ukr-synonym-robustness
  # or: export PYTHONPATH="../ukr-synonym-robustness:$PYTHONPATH"
  ```
- **Datasets and frozen train/val/test splits** — referenced by absolute path in
  `configs/*.yaml` here, mirroring `../ukr-synonym-robustness/configs/*.yaml`. CSVs are not
  copied into this repo.
- **Published classifier checkpoints** — referenced by path from
  `../xml-roberta-finetune-reviews/trained_models/` (see `CURRENT_STATE.md` §2 for the exact
  IDs). Used as an external reference only: the pilot's B0 baseline is **retrained here** so
  that it differs from B1–B4 in training *data* alone, not in pipeline.
- **WSD encoder** — `lang-uk/ukr-paraphrase-multilingual-mpnet-base` (ConEFU, from
  `../U-WSD`), pulled from the Hugging Face Hub, not vendored.
- **fastText vectors for BERT-Attack** — `../bert_attack_uk/fasttext_uk_cbow/cbow.uk.300.bin`
  (8.8GB), referenced by absolute path.

Consequence: **this project is not self-contained.** It reads those sibling folders in place and
breaks if they are moved or renamed. Nothing is copied, so there is no divergence risk either.
It writes only inside this directory (plus `__pycache__` in the imported library).

Only genuinely new code lives here: the augmentation strategies and the
train-on-augmented-data / cross-attack-evaluation orchestration (`augmentation/`, `scripts/`).

## Layout

```
configs/          dataset configs (paths to data + baseline checkpoints), mirrors ukr-synonym-robustness/configs
augmentation/      the augmentation strategies: random, WSD, adversarial (+ anti-adversarial
                   control), WSD-adversarial, and MLM-distribution (B1-B7)
scripts/           generate augmented data, train, evaluate robustness, aggregate results,
                   run one pilot cell (run_pilot.py) or the whole queue (run_campaign.py)
results/           experiment outputs (gitignored large artifacts; commit only summary tables)
                   pilot_seed<S>/ per-seed subsample+B0+augmented data+checkpoints
                   {textfooler,bert_attack}/ attack cells    archive/ superseded runs
```
