# ukr-adversarial-augmentation

Follow-up to the *Precision vs. Perturbation* (UNLP 2025) attack/WSD work. This project asks:

> Can automatically generated, sense-aware synonym augmentation improve the robustness of
> Ukrainian text classifiers without sacrificing clean accuracy?

See [`CURRENT_STATE.md`](CURRENT_STATE.md) for the inventory of what exists (reused assets +
what this project built), and [`RESEARCH_PLAN.md`](RESEARCH_PLAN.md) for the research questions,
training conditions, metrics, staged plan, and **results**. The full narrative version of the
plan this was distilled from is `article_plan.md` (in this folder).

## Status — campaign COMPLETE (24/24 stages, 124.3 h, finished 2026-09-19)

XLM-R + UA Reviews across 3 seeds for the main grid, plus MLM, pool-size, ratio, full-data
and cross-dataset/architecture conditions — every one of them reseeded to 3 seeds except
News (excluded, lowest priority). **This supersedes the single-seed Stage-A pilot outright.**

**Claimable, and now checked on 2 architectures + full training data:**

- **The mechanism is settled and generalises.** B5 — same candidate pool, but picking the
  *least* confidence-reducing substitution — is far worse than no augmentation at all on
  **both** XLM-R and Ukr-RoBERTa (+0.17 to +0.20 cASR, 6/6 seed×architecture cells,
  p < 0.0001 throughout). The *direction* of adversarial selection is what buys robustness,
  not architecture-specific luck.
- **SAAA (B4) beats baseline everywhere it was tested**: main grid (3/3 seeds), full-78k
  training (3/3 seeds), Ukr-RoBERTa (3/3 seeds). No condition beats it on clean accuracy cost.
- **But "SAAA is more reliable than plain adversarial selection" is architecture-dependent,
  not universal — this is the one place the pilot's framing needed real correction.** On
  XLM-R, B4 has a 7× smaller seed-to-seed range than B3 (0.020 vs 0.152) with no clear mean
  edge. On **Ukr-RoBERTa, B3 is both the lower-mean AND the more stable condition**
  (mean 0.387 vs B4's 0.414, range 0.015 vs 0.037, p < 0.0001 on 3/3 seeds). Neither
  condition has a lower mean than the other everywhere — report reliability/collapse-
  resistance as the contribution, never "B4 has a lower mean than B3."
- **The full-78k "win" for B3 does not survive reseeding, and it is now explained.** All
  three augmented conditions there are flagged `DEGENERACY_SUSPECT` on at least one seed
  (predictions concentrating on the majority class). Reseeding showed *why*: on the one
  seed where B3 does **not** collapse (its macro-F1 matches B0's), it gives **zero**
  robustness gain (p = 1.00). On the two seeds where it does collapse, it also "wins" by a
  large margin. **That correlation is the whole effect — B3's full-78k number is retracted
  as a robustness claim.** B4's full-78k gain is real, smaller, and does not correlate with
  collapse (3/3 seeds, modest macro-F1 cost) — it is the number to report.
- **RQ4 is negative in both directions**, and label noise is ruled out as an explanation:
  each augmentation family helps only against its own attack family (B4 best against
  TextFooler, worse than baseline against BERT-Attack; MLM-based B7 the mirror image), and
  the antonym rate in the MLM conditions is only 0.3% — far too low to be the cause.
- **UNLP has no reliable effect, now confirmed over 3 seeds** (was "inconclusive" at 1 seed;
  now only 1/9 seed×condition comparisons reach significance, no consistent direction).
  Report as a genuine negative case, consistent with manipulation detection being a
  rhetorical rather than lexical signal.
- **More augmentation helps, but not unanimously**: r = 1.0 beats r = 0.5 on 2/3 seeds for
  every condition; **B4 is the only condition where it never reverses** (the third seed is
  null, not worse) — the safest ratio recommendation is for B4 specifically.
- **No clean-performance cost** anywhere: accuracy 0.763–0.778, eval macro-F1 0.484–0.503.
- **Retracted from the pilot:** "naive augmentation hurts" did not replicate (p = 0.43).

**Still single-seed (low priority, not reseeded):** News generality (−0.033) and the r=0.25
ratio point.

Full tables, per-seed numbers and the final claimability matrix: `RESEARCH_PLAN.md` →
"Round 2 results". Raw: `results/pilot_metrics_by_seed.md`, `results/pilot_metrics_paired.csv`,
`results/augmentation_diagnostic.md` (antonym-rate check).

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
