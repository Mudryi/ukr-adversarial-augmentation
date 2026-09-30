# Current State — what already exists

Inventory of reusable assets across sibling projects in `/home/mudryi/phd_projects/`, checked
2026-09-13. Each item is tagged **[reuse as-is]**, **[reuse w/ adaptation]**, or **[verify
first]**.

## 1. Datasets & frozen splits — [reuse as-is]

All three datasets from the article plan exist, with the exact splits `ukr-synonym-robustness`
already treats as canonical:

| Dataset | Path (train/eval/test) | Size | Labels |
|---|---|---|---|
| UA Reviews | `xml-roberta-finetune-reviews/cross_domain_uk_reviews/{train,eval,test}_reviews.csv` | 78,146 / 9,769 / 9,769 | 5-class sentiment (1-5) |
| UA News | `xml-roberta-finetune-reviews/ua-news/{train,eval,test}.csv` | 97,646 / 24,294 / 30,469 | 5-class topic |
| UNLP 2025 | `xml-roberta-finetune-reviews/unlp_sharedtask_dataset/{train,eval,test}.csv` | ~3.8k rows total | binary manipulation detection |

Do not use `xml-roberta-finetune_unlp/train.parquet` / `test.csv` — that's the raw shared-task
release (53k unlabeled test rows, span-identification format), a different split from the one
the attack results below were computed on.

## 2. Baseline (B0) classifiers — [verify first]

Fine-tuned checkpoints already exist for all three target models × three datasets, referenced
directly in `ukr-synonym-robustness/configs/*.yaml`:

| Dataset | ukr-roberta-base | xlm-roberta-base | sbert-mpnet (not primary) |
|---|---|---|---|
| Reviews | `trained_models/7ddc/model_7ddc_7_600` | `trained_models/tmdk/model_tmdk_7_600` | `trained_models/7yuz/model_7yuz_4_1200` |
| News | `trained_models/npz4/model_npz4_9_1000` | `trained_models/3rzr/model_3rzr_9_2500` | `trained_models/1kjq/model_1kjq_9_2500` |
| UNLP | `trained_models/1ozc/model_1ozc_14` | `trained_models/p0g9/model_p0g9_14` | `trained_models/zzl4/model_zzl4_14` |

All paths are under `xml-roberta-finetune-reviews/`. Per `article_plan.md` §3, sbert-mpnet is
**not** a primary model for this project — only XLM-R and Ukr-RoBERTa.

**These are NOT the pilot's baseline.** They were trained on the full 78k split by a different
pipeline with accuracy-based checkpoint selection, so using them as B0 would confound
"augmentation helped" with "training pipeline differs". The Stage-A pilot therefore **retrains
B0** with the same loop and clean data as B1–B4 (`scripts/train_augmented.py --condition B0`).
These published checkpoints remain useful as an external reference point — their attack numbers
are in §5 and re-derived in `results/baseline_metrics.md`.

`xml-roberta-finetune_unlp/trained_models/model_{q4oo,vhuj,r89i}_*` are a **different, unrelated**
model (multi-label span-identification) — not used by any config here.

## 3. Attack + WSD + synonym + morphology library — [reuse as-is]

All in `ukr-synonym-robustness/src/`, importable as a package (`pip install -e`):

- `attacks/textfooler.py`, `attacks/bert_attack.py` — TextFooler-UA (dictionary synonyms,
  SBERT sim filter ≥0.7, top-200 candidates) and BERT-Attack-UA (XLM-R-large MLM substitutes,
  fastText cosine filter ≥0.33, 40% max-change budget). Both share `attacks/base.py`.
- `core/synonym_dict.py` — cleaned Ukrainian synonym dictionary loader (merges WordNet-style +
  ULIF + Wiktionary + hand-parsed corrections, removes antonyms).
- `core/morphology.py` — pymorphy2-based `replace_word`, POS/gender/case-aware inflection.
  **This is the core building block for every augmentation strategy.**
- `core/wsd.py` — `SenseSimilarity`, sense-aware filtering via ConEFU
  (`lang-uk/ukr-paraphrase-multilingual-mpnet-base`), default threshold **0.35** (empirically
  chosen, see `results/wsd_dev/threshold_sweep.md`), CLI-configurable via `--wsd-threshold`.
- `core/pos_filter.py`, `core/stopwords.py`, `core/tokenization.py`, `core/importance.py` —
  supporting filters and leave-one-out importance scoring (exactly the confidence-drop signal
  article_plan §8 wants for adversarial candidate selection).
- `core/predictor.py` — unified classifier wrapper (`Predictor`), returns softmax probs — this
  is what adversarial augmentation needs to score candidates against a trained classifier.
- `src/evaluation/stats.py` — Wilson CI, paired bootstrap, McNemar exact test — ready for the
  "3 seeds + CIs" requirement (article_plan §19).

## 4. Evaluation/metrics — [reuse w/ adaptation]

`src/evaluation/metrics.py:aggregate()` already computes, per attack run: `original_accuracy`,
`after_attack_accuracy`, `attack_success_rate`, `avg_queries`, `avg_change_rate`,
`avg_semantic_sim`.

**Gap (now closed).** macro-F1, cASR, and flip-rate are not computed at the classifier-attack
level upstream — those exist only in `llm_eval/metrics.py` for the separate LLM-transfer
harness. But every per-example row (`examples.jsonl`: `true_label`, `orig_label`, `adv_label`,
`status`) contains what's needed to derive them **without rerunning any attack**, which
`scripts/aggregate_results.py` now does:
- `cASR = P(adv_label != true_label | orig_label == true_label)`, with a Wilson CI
- `flip_rate = P(orig_label != adv_label)`
- macro-F1 (clean and adversarial) from the per-row predictions
- paired McNemar tests between any two conditions, restricted to examples both models get right
  when clean — the right test here, since every condition is attacked on the same examples

Note `flip_rate == delta` and `cASR == delta / clean_accuracy` in these artifacts. That is not a
bug: the attack pipeline skips already-wrong examples (`SKIPPED_ORIG_WRONG`, leaving
`adv_text == orig_text`), so flips only ever occur on clean-correct rows.

## 5. Existing results already answering "Step 1: reproduce the baseline" — [reuse as-is]

`ukr-synonym-robustness/results/{textfooler,bert_attack}/<dataset>__<model>/` (plus
`__wsd035` suffix directories for WSD-filtered TextFooler) already cover the full
clean × TextFooler × BERT-Attack × WSD-TextFooler grid for all 3 datasets × 3 models. Headline
numbers (from `results/summary_tables.md`, ASR / orig_acc→adv_acc):

| Dataset | ukr-roberta TF | xlmr TF | ukr-roberta BERT-Atk | xlmr BERT-Atk |
|---|---|---|---|---|
| Reviews | 51.2% · 0.763→0.372 | 34.7% · 0.779→0.509 | 14.0% · 0.763→0.656 | 12.6% · 0.779→0.681 |
| News | 8.1% · 0.987→0.907 | 10.8% · 0.936→0.836 | 14.2% · 0.987→0.847 | 19.9% · 0.936→0.750 |
| UNLP | 39.9% · 0.814→0.490 | 37.9% · 0.801→0.497 | 14.5% · 0.814→0.696 | 14.4% · 0.801→0.686 |

This means **P0 "reproduce baseline classifier + attack results" is essentially already done**
for XLM-R and Ukr-RoBERTa — the work is verifying/re-deriving macro-F1 and cASR from the existing
`examples.jsonl` files (§4), not rerunning attacks.

## 6. What this project has built — [done, 2026-09-13]

Everything below was absent when the project started (`ukr-synonym-robustness/research_plan.md`
listed "adversarial augmentation" only as a future Defense idea):

| Component | Path | State |
|---|---|---|
| Random synonym augmentation (B1) | `augmentation/random_synonym.py` | done |
| WSD-aware augmentation (B2) | `augmentation/wsd_synonym.py` | done |
| Adversarial selection (B3) + anti-adversarial control (B5) | `augmentation/adversarial_synonym.py` | done — one function, `objective="max"` vs `"min"`, so the control differs in nothing else |
| WSD-adversarial / SAAA (B4) | `augmentation/wsd_adversarial_synonym.py` | done |
| MLM-distribution augmentation (B6/B7) | `augmentation/mlm_synonym.py` | done — fill-mask candidates + BERT-Attack's own four filters, for the second direction of RQ4 |
| Shared capped candidate pool | `augmentation/_common.py:sample_candidate_pool` | done — all four strategies select from the *same* space, so conditions differ only in selection rule |
| Cached augmented-data generator | `scripts/generate_augmented_dataset.py` | done |
| Train on clean + augmented | `scripts/train_augmented.py` | done — fp16 AMP, macro-F1 selection, no hardcoded wandb key |
| Robustness evaluation | `scripts/evaluate_robustness.py` | done — wraps `run_attack.py` for TF / WSD-TF / BERT-Attack |
| macro-F1 / cASR / flip-rate + Wilson CIs + paired McNemar | `scripts/aggregate_results.py` | done — closes the §4 gap |
| Resumable pilot orchestrator | `scripts/run_pilot.py` | done — per-step subprocess, skip-existing, baseline underfit guard, `--variant` for ablations |
| Multi-stage campaign queue | `scripts/run_campaign.py` | done — 24 stages across 2 rounds, resumable, optional checkpoint pruning |
| Cross-seed aggregation | `scripts/aggregate_results.py` | done — per-seed cASR with range, pooled McNemar (scipy exact test above n=1000), degeneracy flag, single-seed cells flagged |
| Label-noise diagnostic | `scripts/diagnose_augmentation.py` | done — known-antonym substitution rate per condition |

**Nothing is missing at the priority levels this project set out to reach.** Every P0/P1 item
is done and reseeded to 3 seeds (except News generality and the r=0.25 ratio point, both P1
but explicitly deprioritized — see `RESEARCH_PLAN.md` → "Round 2 results"). What remains is
P2 (MLM-based augmentation is already done as B6/B7; inference-time ensembling and a third
architecture are not) and P3 (new annotation — still avoided per the original plan).

## 7. Stage-A pilot artifacts — [produced 2026-09-13]

Run in ~2h50m on the RTX 3090 (`results/pilot_seed1914/overnight.log`).

**Layout note (changed when the campaign launched):** `results/pilot/` was renamed
`results/pilot_seed1914/` (one pilot root per seed; the campaign reuses its subsample, B0 and
augmented data rather than regenerating them), and the pilot's 400-example attack cells were
moved to `results/archive/stageA_pilot_n400/` so that `results/{textfooler,bert_attack}/`
holds one homogeneous 1500-example grid. Paths below are given post-move.

- `results/archive/stageA_pilot_n400/pilot_metrics.{md,csv}` — five-condition × three-attack table with cASR Wilson CIs.
- `results/archive/stageA_pilot_n400/pilot_metrics_paired.csv` — all pairwise McNemar comparisons between conditions.
- `results/pilot_seed1914/clean_train_subsample.csv` — the 20k clean rows every condition trained on.
- `results/pilot_seed1914/augmented/<tag>__B{1..4}__r0.5/` — cached augmented data + per-example
  diagnostics (`augmented.jsonl`: original/replacement word, WSD similarity, confidence drop)
  + `meta.json` (coverage: 97.3% random/adversarial, 93.5% WSD variants).
- `results/pilot_seed1914/checkpoints/reviews__xlmr_base__B{0..4}__seed1914/` — five checkpoints,
  ~1.1GB each (**~5.5GB**; these are the only large artifacts this project writes).
- `results/archive/stageA_pilot_n400/{textfooler,bert_attack}/` — the 15 attack cells (n=400).
- `results/baseline_metrics.{md,csv}` — macro-F1/cASR/flip-rate re-derived for the *published*
  30-cell attack grid (independent of the pilot).

Headline outcome is in `RESEARCH_PLAN.md` → "Stage-A results": sense filtering clearly beats
naive augmentation (RQ2), adversarial selection is the strongest condition (RQ3), SAAA is not
better than plain adversarial selection, and nothing transfers to BERT-Attack (RQ4, negative).

## 7b. Campaign artifacts — [COMPLETE, 2026-09-19 — no further stages queued]

All 24 stages `ok` across two rounds (Round 1: 15 stages / 78.1 h; Round 2 follow-up: 9
stages / 46.2 h), **124.3 h GPU total**, finished 2026-09-19 23:18.
State in `results/campaign_manifest.json`; per-stage logs in `results/campaign_logs/`.
`results/` is now ~33 GB; 107 GB free on the volume.

| Path | Contents |
|---|---|
| `results/pilot_seed{1914,2024,7}/` | per-seed clean subsample, B0, augmented data for B1–B7, checkpoints |
| `results/pilot_full78k/`, `results/pilot_ukrroberta_reviews/`, `results/pilot_unlp/`, `results/pilot_news/` | Round 2 roots — each holds 3 seeds' worth of checkpoints/augmented data except News (1 seed, not reseeded) |
| `results/{textfooler,bert_attack}/<cell>/` | attack cells at n=1500; `<cell>` = `<dataset>__<model>__B{0..7}__seed<S>[__<variant>][__wsd035]` |
| `results/pilot_metrics.{md,csv}` | all cells: clean/adv accuracy, `eval_macro_f1` (trustworthy, full eval split), cASR + Wilson CI, flip rate, `majority_pred_share`, `degeneracy_flag` |
| `results/pilot_metrics_paired.csv` | every condition pair, per seed and variant, paired McNemar (large-n cells use a scipy exact binomial test — see `scripts/aggregate_results.py:mcnemar`) |
| `results/pilot_metrics_by_seed.md` | **the table that decides claims** — per-seed cASR with range, pooled McNemar, single-seed cells flagged |
| `results/augmentation_diagnostic.md` | known-antonym substitution rate per condition (label-noise lower bound; 0.0% for B1–B5, 0.3% for B6/B7) |
| `results/archive/stageA_pilot_n400/` | the superseded single-seed pilot (n=400) |

`run_campaign.py --prune-checkpoints` drops the weights of any augmented condition whose
three attack cells are already written; most Round 2 stages prune by default. B0 checkpoints
are never pruned — later stages score candidates against them.

**Final results are in `RESEARCH_PLAN.md` → "Round 2 results"**, which supersedes the
earlier "Campaign results" section for anything the two disagree on (full-78k B3, UNLP, and
the B4-vs-B3 stability ranking on Ukr-RoBERTa all changed between rounds). Headline: the B5
mechanism control and SAAA's baseline-beating result both replicate on a second architecture;
the full-78k B3 "win" is retracted as a collapse artifact while B4's survives; UNLP is now a
confirmed negative result rather than a data gap; and "SAAA is more stable than plain
adversarial selection" turned out to be XLM-R-specific, reversing on Ukr-RoBERTa.

## 8. Environment — [resolved 2026-09-13]

The earlier CUDA driver/library mismatch is **fixed**. Working configuration:

- GPU: NVIDIA RTX 3090 (24GB), driver 580.178.04, CUDA 13.0; `torch.cuda.is_available()` → True.
- Interpreter: **`/home/mudryi/phd_projects/ukr-synonym-robustness/dev_env/bin/python3`** — this
  is the venv every script expects (torch 2.9+cu128, transformers, pymorphy2, scikit-learn,
  pandas). The default `python3` on PATH resolves to an unrelated venv that lacks pymorphy2 and
  sklearn.
- BERT-Attack needs Ukrainian fastText vectors at
  `/home/mudryi/phd_projects/bert_attack_uk/fasttext_uk_cbow/cbow.uk.300.bin` (8.8GB, ~10GB RAM
  when loaded). `ukr-synonym-robustness/resources/fasttext_uk/` is **empty**, so
  `evaluate_robustness.py` passes this absolute path explicitly — without it BERT-Attack fails
  at startup.

## 8. Hygiene flags before reusing training code

- `xml-roberta-finetune-reviews/main.py` and `xml-roberta-finetune_unlp/main.py` both have a
  **hardcoded wandb API key** — scrub before adapting either into `scripts/train_augmented.py`.
- Both repos' `requirements.txt` are unpinned (`wandb, transformers, numpy, torch, datasets` with
  no versions) — pin before use, ideally matching
  `ukr-synonym-robustness/requirements.lock.txt` where the same libraries overlap.
- `xml-roberta-finetune-reviews/main.py` looks mid-edit (comments show it was repurposed between
  reviews/news/unlp configs, currently pointed at UNLP) — use it as a **pattern reference**, not
  a script to run as-is.
- Seed convention: `ukr-synonym-robustness` fixes seed **1914** everywhere (dataset sub-sampling,
  attack seeding, bootstrap). Use 1914 as seed #1 for this project's multi-seed runs so results
  stay comparable to the existing attack grid.
