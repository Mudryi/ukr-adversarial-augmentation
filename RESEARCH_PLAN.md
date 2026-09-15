# Research Plan — Sense-Aware Adversarial Augmentation (SAAA)

Condensed from `article_plan.md` (in this folder). See `CURRENT_STATE.md` for what's already built/run.

## Central question

Can automatically generated, sense-aware synonym augmentation improve the robustness of
Ukrainian text classifiers without sacrificing clean accuracy?

## Research questions

- **RQ1** — Does synonym-based data augmentation improve adversarial robustness over the
  baseline, while keeping clean accuracy roughly unchanged?
- **RQ2** — Does WSD-filtered augmentation outperform naive (unfiltered) synonym augmentation?
  *(main thesis-specific question — WSD filtering already improves TextFooler replacement
  validity from ~39% to ~47% in prior work, so there's motivation to expect better training
  examples.)*
- **RQ3** — Is adversarial (confidence-drop-maximizing) synonym selection better than random
  synonym selection, for augmentation purposes?
- **RQ4** — Does a defense trained against one attack's synonym distribution generalize to a
  different attack at eval time (train under TextFooler-style augmentation, eval under
  BERT-Attack, and vice versa)? **This is P0, not optional** — otherwise reviewers can claim the
  model just learned the perturbation generator.

## The eight training conditions

| ID | Training data | Selection | WSD filter |
|---|---|---|---|
| B0 | Original only | — | — | *(checkpoints likely already exist — see CURRENT_STATE.md §2)* |
| B1 | Original + random synonym | random | no |
| B2 | Original + WSD synonym | random from WSD-filtered set | yes |
| B3 | Original + adversarial synonym | max confidence-drop | no |
| B4 (**SAAA**) | Original + WSD-adversarial synonym | max confidence-drop | yes |
| B5 (control) | Original + *anti*-adversarial synonym | **min** confidence-drop | no |
| B6 | Original + MLM substitution | random | n/a |
| B7 | Original + MLM substitution | max confidence-drop | n/a |

B5–B7 were added after the Stage-A pilot, to close two holes it exposed:

- **B5 is the RQ3 control.** B3 (argmax confidence drop) beat everything, but the pilot
  had no condition isolating *adversarialness* from "perturb the training data somehow".
  B5 picks the **least** damaging valid substitution from the identical pool, sharing one
  implementation with B3 (`augmentation/adversarial_synonym.py`, `objective="min"`) so the
  two differ in nothing else. If B5 also beats B0, RQ3's interpretation is wrong.
- **B6/B7 are the second direction of RQ4.** The pilot trained on TextFooler-family
  synonyms and evaluated under BERT-Attack. That cannot separate "synonym augmentation
  does not transfer" from "TextFooler-family candidates specifically are too narrow".
  B6/B7 augment from the MLM distribution BERT-Attack samples from — same fill-mask model
  and same four admissibility filters (`augmentation/mlm_synonym.py`) — and are evaluated
  under TextFooler, completing the 2×2.

  *Known caveat:* MLM candidates are not guaranteed meaning-preserving. The filter set is
  BERT-Attack's own, and fastText similarity does not separate antonyms (an observed
  example: `погана → висока`, which inverts the sentiment while the gold label is kept).
  This is faithful to the attack, but it means a poor B6/B7 result is ambiguous between
  "distribution mismatch" and "label noise". Quantify the antonym rate from the cached
  `augmented.jsonl` before interpreting those rows.

All four augmentation strategies share one candidate-generation pipeline (reusing
`ukr-synonym-robustness/src/core/{synonym_dict,morphology,wsd,predictor}.py`) so differences
come only from selection/filtering logic, not implementation drift. Default: **one substituted
word per training example**; augmentation applied only to `D_train`, never val/test.

## Metrics

Per model/dataset/condition, on clean + TextFooler + BERT-Attack + WSD-TextFooler test sets:

- Clean accuracy, macro-F1 (existing: accuracy; macro-F1 needs the small new aggregator).
- Adversarial accuracy, Δ = clean − adversarial accuracy.
- **cASR** = P(adv wrong | clean correct) — primary robustness metric (needs new aggregator,
  derivable from existing per-example data, see CURRENT_STATE.md §4).
- Flip rate = P(orig prediction ≠ adv prediction).
- Perturbation rate (average % tokens changed) — already logged (`avg_change_rate`).

## Priority plan

| Priority | Item | Status |
|---|---|---|
| P0 | Reproduce baseline (B0) clean + attack results | **done** — `results/baseline_metrics.md` (published grid, macro-F1/cASR derived) |
| P0 | Build shared augmentation pipeline (B1–B4) | **done** — `augmentation/`, shared capped candidate pool |
| P0 | Train B1–B4 on XLM-R + Reviews (pilot) | **done** — Stage-A, 2026-09-13 |
| P0 | Evaluate all 5 conditions × clean/TF/BERT/WSD-TF | **done** — 15 cells, `results/pilot_metrics.md` |
| P0 | Cross-attack generalization matrix | **done** — negative result (RQ4): no transfer to BERT-Attack |
| P0 | RQ3 control: anti-adversarial (argmin) selection, B5 | **queued** — S1; RQ3's interpretation is untested without it |
| P1 | 3 seeds (1914 + 2 more) on B0–B5, CIs | **queued** — S1; required before any gain can be claimed |
| P1 | Augmentation from BERT-Attack-style MLM substitutions, B6/B7 | **queued** — S2; promoted from P2, it is the missing half of RQ4 |
| P1 | Pool-size ablation (10×20) — does SAAA pay off with room to choose? | **queued** — S3 |
| P1 | Augmentation-ratio ablation, r ∈ {0.25, 0.5, 1.0} | **queued** — S4 |
| P1 | Re-run pilot on full 78k train (not the 20k subsample) | **queued** — S5 |
| P1 | Scale surviving conditions to Ukr-RoBERTa + News + UNLP | **queued** — S6 |
| P2 | Inference-time synonym ensemble | optional, drop if time tight |
| P2 | Third architecture (sbert) | only if everything else done |
| P3 | New human annotation | avoid — reuse existing WSD/validity audits in `ukr-synonym-robustness/results/{wsd_dev,audit,audit_replacements}` |

## Staged execution order

1. ~~**Pilot** — XLM-R + Reviews, 1 seed, B0 + B1–B4.~~ **Done 2026-09-13.** Decision point
   passed: B3 and B4 clearly beat B0 on cASR under the TextFooler family with no clean-accuracy
   cost, so scaling is justified. See "Stage-A results" above.
2. ~~**Cross-attack generalization.**~~ **Done — negative** (no transfer to BERT-Attack).
3. Everything from here is queued in **`scripts/run_campaign.py`** — see "Campaign" below.
   Run `python scripts/run_campaign.py --list` for the exact commands.

## Stage-A pilot as actually run (2026-09-13)

Launched via `scripts/run_pilot.py --num-epochs 4` (RTX 3090). Exact settings:

| Setting | Value | Why |
|---|---|---|
| Dataset × model | UA Reviews × XLM-R-base, seed 1914 | Stage A screening (strongest lexical vulnerability) |
| Clean train | **20,000-row deterministic subsample** of the 78k train split | fits an overnight window; identical for every condition |
| Baseline | **B0 retrained with this same loop/data** | the published checkpoint used all 78k rows, a different pipeline, and accuracy-based selection — comparing against it would confound "augmentation helped" with "pipeline differs" |
| Augmentation ratio | r = 0.5 (10k augmented rows), identical across B1–B4 | article_plan.md §12 — no dataset-size confound |
| Candidate pool caps | max 3 tokens × 6 candidates per example, identical across B1–B4 | conditions differ only in *selection rule*; uncapped B4 generation would take 10–60h |
| M₀ for B3/B4 | the retrained B0 | matches M₀ = Train(D), offline adversarial augmentation |
| Training | lr 2e-5, batch 32, grad-accum 2, ≤4 epochs, early stop 6 eval rounds, fp16 AMP, macro-F1 selection | deviates from B0's original lr 2e-6/20-epoch recipe, but applied **identically to all five conditions**, so relative comparisons stay valid |
| Evaluation | first 400 test examples, same for every condition | TextFooler, WSD-TextFooler (0.35), BERT-Attack |
| Eval ordering | attack-major | partial completion still yields a full cross-condition comparison |

Deliberate limitations of this pilot: single seed, single dataset/model, subsampled clean
train, capped candidate pool, and 400 (not 9,769) eval examples. It answers "does
augmentation help relative to an identically-trained baseline", **not** "does it beat the
published full-data numbers". Stage B scales the surviving conditions up.

A `--min-baseline-macro-f1` guard aborts the run if B0 underfits (majority-class collapse
on Reviews scores ~0.19 macro-F1), so a bad recipe fails loudly instead of producing a
degenerate five-way table hours later.

## Stage-A results (2026-09-13) — SUPERSEDED, kept for the record

> These are single-seed, n=400 numbers. Three of their conclusions did not survive
> reseeding (see "Campaign results" below): B1 does not harm robustness, B3 is not
> the best condition, and B3-vs-B4 is not null. **Do not quote this section.**

Full tables and raw cells archived under `results/archive/stageA_pilot_n400/`
(moved there when the campaign standardised on 1500 eval examples; see that folder's
README). Checkpoints and augmented data remain in `results/pilot_seed1914/`.

**Robustness (cASR on 400 test examples; lower = more robust):**

| Condition | TextFooler | WSD-TextFooler | BERT-Attack |
|---|---|---|---|
| B0 baseline | 0.392 | 0.385 | **0.125** |
| B1 random | 0.458 | 0.431 | 0.208 |
| B2 WSD | 0.380 | 0.339 | 0.142 |
| B3 adversarial | **0.281** | **0.253** | 0.147 |
| B4 SAAA | 0.299 | 0.282 | 0.144 |

Robustness ranking under TextFooler: **B3 > B4 > B2 > B0 > B1**.

**Answers (paired McNemar on examples both models get right when clean):**

- **RQ1 — augmentation ⇒ robustness? Conditionally, no.** *(Superseded — the B1 penalty
  below did not replicate across seeds; see "S1 results".)* Naive random augmentation
  *significantly hurts* robustness (B1 vs B0: +0.077 cASR under TextFooler, p=0.010;
  +0.091 under BERT-Attack, p<0.001). Only *selective* augmentation helps. "Add synonym
  augmentation" is not by itself a defense.
- **RQ2 — WSD-filtered beats naive? Yes, consistently.** B2 vs B1 improves on all three
  attacks: −0.095 TextFooler (p=0.0009), −0.110 WSD-TF (p=0.0002), −0.077 BERT-Attack
  (p=0.0002). This is the clearest positive result in the pilot and it is the
  thesis-specific question.
- **RQ3 — adversarial beats random? Yes.** B3 vs B1 −0.183 (p<0.0001); B3 even beats the
  WSD-filtered random condition, B3 vs B2 −0.093 (p=0.0004).
- **SAAA (B4) vs plain adversarial (B3): no significant difference anywhere** (TF p=0.67,
  WSD-TF p=0.29, BERT-Attack p=1.00), with B3 nominally ahead. So sense filtering adds a
  lot on top of *random* selection but is **redundant on top of adversarial selection** —
  article_plan.md §25's "Outcome B". **The obvious explanation is wrong**: B3 and B4 do *not*
  converge on the same substitutions. On the 9,612 shared source rows they pick the same
  target token 65.4% of the time but the same replacement only **24.1%** of the time, and the
  WSD filter costs a third of the achievable confidence drop (mean 0.091 → 0.061). So two
  substantially different augmentation sets train to indistinguishable robustness — the gain
  appears to come from perturbing along a high-loss direction *at all*, not from which
  particular synonym is used.
  Note also that this pilot is **underpowered for a small difference**: with 48 discordant
  pairs it could only have detected |ΔcASR| ≥ 0.058 under TextFooler, and the observed gap is
  0.015. "No significant difference" here means "no ≥6-point SAAA advantage", not equivalence.
- **RQ4 — cross-attack generalization? No.** Under BERT-Attack no condition beats the
  baseline (B2/B3/B4 differences are not significant, p=0.83/0.56/0.23; B1 is significantly
  worse). The gains are confined to the TextFooler family whose synonym distribution the
  augmentation mimics. This is the attack-overfitting criticism confirmed empirically.

**Clean performance — essentially unchanged.** Eval-split macro-F1 (n=9,769, the reliable
measurement): B0 0.484, B1 0.499, B2 0.499, B3 0.503, B4 0.494. Clean accuracy on the 400
attacked examples spans 0.720–0.740, a range of 8 examples — noise. *Note: the
`clean_macro_f1` column in `pilot_metrics.md` is computed on only those 400 examples and is
therefore much noisier than the eval-split figure; do not quote it as the clean-performance
result.*

**Augmentation diagnostics:** coverage 97.3% (random/adversarial) vs 93.5% (both WSD
variants) — sense filtering costs ~4 points of coverage. Cost per condition: B1 0.4 min,
B2 6.2, B3 5.3, B4 25.0 (B4 is the bottleneck: it must sense-score every candidate).

**What this does NOT establish.** Single seed, single dataset, single architecture, 20k-row
train subsample, capped candidate pool, 400 eval examples. The McNemar tests account for
*evaluation* sampling noise only — **not training-run variance**, so the B3/B4 gains need
the 3-seed repeat (P1) before being claimed. B3-vs-B4 being null here is also exactly the
kind of small difference that multiple seeds could reorder.

**Implied next steps:** (1) 3 seeds on B0/B2/B3/B4 to convert these into defensible claims;
(2) drop or de-emphasize B1 — its role is now "informative negative control"; (3) the SAAA
framing needs rethinking, since B3 matches B4 — either find a regime where sense filtering
pays off on top of adversarial selection, or reframe the contribution around RQ2 (sense
filtering rescues *random* augmentation) and the RQ4 negative result; (4) RQ4 suggests
testing augmentation built from BERT-Attack-style MLM substitutions for cross-family
coverage.

## Campaign (queued in `scripts/run_campaign.py`, launched 2026-09-13)

Each stage is one resumable `run_pilot.py` invocation; the queue survives interruption and
restarts at the first unfinished stage. **Evaluation is 1500 test examples throughout**, up
from the pilot's 400 — which could only detect |ΔcASR| ≥ 0.058, wider than most gaps of
interest; 1500 brings that to ≈0.030.

| Stage | What | Conditions | Why it comes here |
|---|---|---|---|
| S1 ×3 seeds | Main grid, 20k clean, r=0.5, caps 3×6 | B0–B5 | Nothing existing is claimable without training-run variance |
| S2 ×3 seeds | MLM family | B6, B7 | Completes the RQ4 matrix |
| S3 (seed 1914) | Pool-size ablation, caps 10×20 | B3, B4, B5 | Make-or-break for the SAAA framing |
| S4 ×2 | Ratio ablation r ∈ {0.25, 1.0} | B2, B3, B4 | |
| S5 | Full 78k train | B0, B2, B3, B4 | Confirms the subsample didn't distort the result |
| S6 ×3 | Ukr-RoBERTa × Reviews; XLM-R × News; XLM-R × UNLP | B0, B2, B3, B4 | Generality |
| S3 ×2 seeds | Pool ablation, remaining seeds | B3, B4, B5 | Queued last: variance on a question S4–S6 don't depend on |

Stages for a given seed **share a pilot root**, so that seed's clean subsample and B0 are
trained once and borrowed by every later stage (`run_pilot.py --variant`). A variant that
trains its own baseline (S5) suffixes B0 too, so it cannot overwrite the main grid's cells.

**Decision points to check as results land, not at the end:**

1. If the seed-to-seed cASR range (in `results/pilot_metrics_by_seed.md`) is comparable to
   the B3−B0 gap, the pilot's headline is noise and S3–S6 need re-scoping.
2. If **B5 also beats B0**, "adversarial selection" is not the mechanism and RQ3 must be
   rewritten around whatever B1 lacks that both B3 and B5 have.
3. If **B4 never separates from B3**, even at 10×20 pools, SAAA is not a contribution and
   the paper reframes around RQ2 + the RQ4 negative.

## Analysis already done on the pilot's cached artifacts

`results/pilot_seed1914/augmented/*/augmented.jsonl` supports mechanism questions without
any GPU time. What it showed for B3 vs B4 (see the SAAA bullet above) is that they are *not*
the same method in disguise — 24.1% replacement overlap — which is why the pool-size ablation
is worth 10 hours: the null needs a mechanism, and "the pool was too small for the filter to
matter" is the only cheap one left standing.

## Campaign results (live) — SUPERSEDE the Stage-A pilot

### S1 — main grid, 3 seeds, n=1500 (2026-09-14)

Seeds 1914/2024/7, XLM-R x UA Reviews, conditions B0-B5. Where these disagree with the
single-seed pilot above, **these win**: the pilot measured no training-run variance.

**cASR under TextFooler, per seed (lower = more robust):**

| Condition | seed7 | seed1914 | seed2024 | mean | range | beats B0 on |
|---|---|---|---|---|---|---|
| B0 baseline | 0.363 | 0.394 | 0.404 | 0.387 | 0.041 | — |
| B1 random | 0.401 | 0.431 | 0.342 | 0.391 | 0.089 | 1/3 |
| B2 WSD | 0.353 | 0.384 | 0.347 | 0.361 | 0.036 | **3/3** |
| B3 adversarial | 0.387 | 0.304 | 0.235 | 0.309 | **0.152** | 2/3 |
| B4 **SAAA** | 0.302 | 0.304 | 0.284 | **0.296** | **0.020** | **3/3** |
| B5 anti-adversarial | 0.526 | 0.601 | 0.515 | 0.547 | 0.086 | 0/3 |

**1. The RQ3 control passed decisively — and it is the cleanest result in the project.**
B5, which picks the *least* confidence-reducing valid substitution from the identical pool,
is **far worse than no augmentation at all**: +0.169 cASR vs B0, every seed, every p < 0.0001.
So the gain from B3/B4 is not "perturbing the training data somehow" — the *direction* of
selection is doing the work. This was the single largest threat to RQ3 and it is now closed.

**2. SAAA is the best condition — reversing the pilot.** B4 beats B0 on **3/3 seeds**
(-0.067 / -0.091 / -0.134, all p < 0.0001) with a seed range of **0.020**. B3 beats B0 on only
2/3 and is *significantly worse* than B0 on seed 7 (+0.031, p = 0.035), with a range of 0.152 —
**larger than its own mean advantage over B0**. Plain adversarial selection is a lottery
across training runs; adding the sense filter makes it reliable.

*Stated precisely:* head-to-head B3-vs-B4 pools to -0.017 (p = 0.013) in B4's favour, but only
1/3 seeds agrees and the pooled figure is carried by seed 7 — so **do not claim B4 has a lower
mean than B3**. The defensible claim is about consistency: B4 is the only adversarial
condition that improves on baseline in every run, at ~1/7th the seed-to-seed spread.

**3. The pilot's "naive augmentation hurts" does NOT replicate.** B1 vs B0 across seeds:
+0.042, +0.050, **-0.072** — 1/3, pooled p = 0.43. **Null, not harmful.** The pilot's
significant B1 penalty was a seed effect. Any write-up quoting it must be corrected.

**4. RQ2 holds, but smaller than the pilot suggested.** B2 beats B0 on 3/3 seeds, pooled
-0.033 (p < 0.0001), though only seed 2024 is individually significant.

**5. RQ4 remains negative.** Under BERT-Attack every condition is at or above the B0 baseline
(0.140): B2 0.166, B3 0.160, B4 0.155, B5 0.198. No transfer, and the ordering of conditions
does not even survive the change of attack family.

**6. No clean-performance cost.** Clean accuracy 0.763-0.778 and eval-split macro-F1
0.484-0.503 across every condition and seed — no condition trades accuracy for robustness.

**Consequence for the campaign.** S3 (pool-size ablation) was designed to explain a
*null* B3-vs-B4 result, a premise S1 removed — but it ran anyway and delivered the mechanism
instead (see S3 below). Its two remaining seeds, queued at the end, are what make that
mechanism claimable.

### S2 — the MLM family, 3 seeds (2026-09-15): RQ4 answered in both directions

B6/B7 augment from the fill-mask distribution BERT-Attack samples from. Adding them turns
RQ4 from a one-directional negative into a symmetric result.

**cASR means over 3 seeds (lower = more robust):**

| Condition | Augmentation family | vs TextFooler | vs BERT-Attack |
|---|---|---|---|
| B0 baseline | — | 0.387 | 0.140 |
| B4 **SAAA** | synonym dict | **0.296** (best) | 0.155 |
| B6 MLM-random | MLM | 0.419 | 0.152 |
| B7 **MLM-adversarial** | MLM | 0.390 | **0.127** (best) |

**Each augmentation family buys robustness only against its own attack family.** B7 is the
**only** condition in the whole grid that beats the baseline under BERT-Attack (-0.012,
**3/3 seeds**, pooled p = 0.017) — and it gives nothing against TextFooler (0.390 vs 0.387).
Symmetrically, every synonym-dictionary condition (B1-B5) is *worse* than baseline under
BERT-Attack (B2 +0.019, B3 +0.019, B4 +0.014, B5 +0.060, all p < 0.005).

This is a far stronger statement than the pilot's "no transfer": the defence tracks the
perturbation distribution it was trained on, demonstrated in both directions, with a
condition that succeeds in each. Note B7's effect is small (-0.012) though perfectly
consistent, whereas B4's within-family gain is large (-0.091).

### S3 — pool-size ablation, seed 1914 (2026-09-15): the SAAA mechanism

Re-running B3/B4/B5 with candidate pools of 10 tokens x 20 candidates instead of 3 x 6:

| Condition | caps 3x6 | caps 10x20 | change |
|---|---|---|---|
| B3 adversarial | 0.304 | 0.408 | **+0.104** |
| B4 SAAA | 0.304 | 0.347 | +0.043 |
| B5 anti-adversarial | 0.601 | 0.624 | +0.023 |

**B3 vs B4 head-to-head: +0.001 (p = 1.00) at 3x6, but -0.068 (p < 0.0001) at 10x20.**

This supplies the mechanism the project was missing. A *wider* adversarial search finds
substitutions that hurt the trained model more — and the WSD filter is precisely what blocks
the meaning-destroying ones among them. With a pool of at most 18 candidates there is little
for the filter to catch, which is why the pilot saw B3 and B4 as identical; with 200
candidates the unfiltered condition degrades 2.4x as much. Sense filtering is a *safeguard
on search width*, not a general improvement.

Two caveats before this is written up: (1) both conditions are worse at 10x20 than at 3x6, so
this is a diagnostic regime, **not** a better operating point — the recommended configuration
remains the small pool; (2) this is one seed, and S1 showed B3 specifically to be the
seed-unstable condition. The two remaining S3 seeds are queued at the end of the campaign and
are what make this claimable.

## Guardrails (don't skip)

- Augment `D_train` only. Val/test stay frozen and untouched.
- Never tune augmentation hyperparameters (WSD threshold, ratio r) against the adversarial test
  set — use validation performance or a fixed dev config. WSD threshold stays at the existing
  0.35 default unless there's a specific reason to sweep it.
- Offline adversarial augmentation (generate once from `M_0`, retrain) — not online/iterative
  regeneration against an evolving model. Simpler, reproducible, and consistent with
  `article_plan.md` §10's recommendation.
- Control augmentation size: compare B1–B4 at the same augmentation ratio `r = |D_aug|/|D_train|`
  so differences don't come from dataset-size confounds.

## New code required (maps to this repo's skeleton)

```
augmentation/
    random_synonym.py            # RQ1: strategy A
    wsd_synonym.py                # RQ2: strategy B (B2)
    adversarial_synonym.py        # RQ3: strategy C (B3)
    wsd_adversarial_synonym.py    # main method: strategy D (B4 / SAAA)
scripts/
    generate_augmented_dataset.py # pre-generate + cache augmented data per condition/ratio
    train_augmented.py            # fine-tune given (dataset, model, condition, ratio, seed)
    evaluate_robustness.py        # run clean/TF/BERT/WSD-TF eval, reusing ukr-synonym-robustness attacks
    aggregate_results.py          # macro-F1, cASR, flip-rate, CIs across all runs
```

Pre-generate and cache all augmented datasets (don't augment on the fly during training) —
keeps runs deterministic and debuggable, per `article_plan.md` §26.
