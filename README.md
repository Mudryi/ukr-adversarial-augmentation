# ukr-adversarial-augmentation

Follow-up to the *Precision vs. Perturbation* (UNLP 2025) attack/WSD work. This project asks:

> Can automatically generated, sense-aware synonym augmentation improve the robustness of
> Ukrainian text classifiers without sacrificing clean accuracy?

We train XLM-R and Ukr-RoBERTa classifiers on UA Reviews (plus single-seed checks on News and
UNLP-2025 manipulation detection) under six synonym-substitution augmentation strategies —
random, WSD-filtered, adversarial, WSD-filtered adversarial (SAAA), an anti-adversarial control,
and an MLM-based variant — and evaluate robustness against TextFooler and BERT-Attack across
3 seeds.

**Key findings:**

- The *direction* of adversarial candidate selection, not architecture, drives robustness:
  picking the least confidence-reducing substitution is reliably worse than no augmentation
  at all, on both XLM-R and Ukr-RoBERTa.
- WSD-filtered adversarial augmentation (SAAA) beats the unaugmented baseline in every setting
  tested — main grid, full-data training, and both architectures — with no clean-accuracy cost.
- SAAA's advantage over plain adversarial augmentation is architecture-dependent: it is the
  more stable condition on XLM-R (much smaller seed-to-seed variance), but not the lower-mean
  one on Ukr-RoBERTa.
- Each augmentation family improves robustness only against the attack family it targets
  (e.g. adversarial augmentation helps against TextFooler but not BERT-Attack, and vice versa
  for the MLM-based variant); this is not explained by label noise.
- UNLP-2025 manipulation detection shows no reliable effect, consistent with that task being a
  rhetorical rather than lexical signal.
- More augmented data helps, but not uniformly across conditions.

Full per-seed numbers, significance tests, and the complete results grid: `results/pilot_metrics_by_seed.md`,
`results/pilot_metrics_paired.csv`, `results/augmentation_diagnostic.md` (antonym-rate check).

## Running it

Use the `ukr-synonym-robustness` venv — the default `python3` lacks pymorphy2/sklearn:

```bash
PY=../ukr-synonym-robustness/dev_env/bin/python3

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
- **Datasets and frozen train/val/test splits** — referenced by relative path (sibling
  checkout) in `configs/*.yaml` here, mirroring `../ukr-synonym-robustness/configs/*.yaml`.
  CSVs are not copied into this repo.
- **Published classifier checkpoints** — referenced by path from
  `../xml-roberta-finetune-reviews/trained_models/`. Used as an external reference only:
  the pilot's B0 baseline is **retrained here** so that it differs from B1–B4 in training
  *data* alone, not in pipeline.
- **WSD encoder** — `lang-uk/ukr-paraphrase-multilingual-mpnet-base` (ConEFU, from
  `../U-WSD`), pulled from the Hugging Face Hub, not vendored.
- **fastText vectors for BERT-Attack** — `../bert_attack_uk/fasttext_uk_cbow/cbow.uk.300.bin`
  (8.8GB), referenced by sibling-checkout path.

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
