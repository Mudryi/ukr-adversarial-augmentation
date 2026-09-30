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

  *Caveat, now quantified* (`results/augmentation_diagnostic.md`, via
  `scripts/diagnose_augmentation.py`): the known-antonym substitution rate is **0.33% (B6) /
  0.35% (B7)** against **0.00% for B1–B5**, with flagged pairs like `поганий → хороший` that
  genuinely invert a sentiment label. The rate is a lower bound (dictionary-known antonyms
  only) but far too small to explain B6/B7's weak within-TextFooler performance, so the
  distribution-mismatch reading of RQ4 stands rather than a label-noise one.
  *Original note:* MLM candidates are not guaranteed meaning-preserving. The filter set is
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
| P0 | RQ3 control: anti-adversarial (argmin) selection, B5 | **done** — 3 seeds x 2 architectures, all p < 0.0001 |
| P1 | 3 seeds (1914 + 2 more) on B0–B5, CIs | **done** — S1 |
| P1 | Augmentation from BERT-Attack-style MLM substitutions, B6/B7 | **done** — S2, RQ4 answered both directions |
| P1 | Pool-size ablation (10×20) | **done** — S3, all 3 seeds |
| P1 | Augmentation-ratio ablation, r ∈ {0.25, 0.5, 1.0} | **done** — S4 + R4, r=1.0 reseeded |
| P1 | Re-run pilot on full 78k train (not the 20k subsample) | **done** — S5 + R1; B3's version retracted (collapse), B4's stands |
| P1 | Scale surviving conditions to Ukr-RoBERTa + News + UNLP | **done for Ukr-RoBERTa + UNLP** (3 seeds each, R2/R3); News remains 1 seed (lowest priority, not reseeded) |
| P2 | Inference-time synonym ensemble | optional, drop if time tight |
| P2 | Third architecture (sbert) | only if everything else done |
| P3 | New human annotation | avoid — reuse existing WSD/validity audits in `ukr-synonym-robustness/results/{wsd_dev,audit,audit_replacements}` |

## Staged execution order

1. ~~**Pilot** — XLM-R + Reviews, 1 seed, B0 + B1–B4.~~ **Done 2026-09-13.** Decision point
   passed: B3 and B4 clearly beat B0 on cASR under the TextFooler family with no clean-accuracy
   cost, so scaling is justified. See "Stage-A results" above.
2. ~~**Cross-attack generalization.**~~ **Done — negative** (no transfer to BERT-Attack).
3. **Campaign complete** (24/24 stages, 124.3 h). See "Round 2 results" below for the
   final claimability matrix. `python scripts/run_campaign.py --list` still shows the
   exact commands for reproducibility.

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

**These implied next steps were all carried out** — see "Round 2 results" for the final
answers: the 3-seed reruns, the retirement of B1 as a negative control, the resolution of
the SAAA-vs-B3 question (architecture-dependent, not universal), and the MLM conditions
(B6/B7) that completed the RQ4 matrix.

## Campaign (complete — `scripts/run_campaign.py`, 2026-09-13 to 2026-09-19)

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

## Campaign results — COMPLETE (15/15 stages, 78.1 h, finished 2026-09-17)

These supersede the Stage-A pilot throughout. Claim strength is stated per finding:
a 3-seed result is claimable, a single-seed one is directional.

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
instead (see S3 below), and its two remaining seeds completed in Round 1's final stages —
that mechanism is now claimable at 2/3 seeds (see "Round 2 results").

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
remains the small pool; (2) this was one seed at the time, and S1 showed B3 specifically to
be the seed-unstable condition. *(Superseded — see "S3 (final)" immediately below: all 3
seeds are now in.)*

### S3 (final) — pool ablation now has all 3 seeds

| | seed7 | seed1914 | seed2024 | mean |
|---|---|---|---|---|
| B3 @ 3x6 | 0.387 | 0.304 | 0.235 | 0.309 |
| B4 @ 3x6 | 0.302 | 0.304 | 0.284 | **0.296** |
| B3 @ 10x20 | 0.336 | 0.408 | 0.258 | 0.334 |
| B4 @ 10x20 | 0.236 | 0.347 | 0.295 | **0.292** |

B3-vs-B4 head-to-head widens with pool size: pooled **-0.017 (1/3 seeds)** at 3x6 versus
**-0.044, p < 0.0001 (2/3 seeds)** at 10x20. That is consistent with the "safeguard on search
width" mechanism, **but 2/3 is not unanimity** — seed 2024 favours B3 at both pool sizes.
State this as *supported*, not established. Note also that B4's prized stability degrades at
the wide pool (range 0.111 vs 0.020 at 3x6), so the small pool remains the operating point.

### S4 — augmentation ratio (seed 1914 only; directional)

| Condition | r=0.25 | r=0.5 | r=1.0 |
|---|---|---|---|
| B2 | 0.350 | 0.384 | **0.323** |
| B3 | 0.266 | 0.304 | **0.223** |
| B4 | 0.279 | 0.304 | **0.251** |

r = 1.0 is best for all three conditions, so **more augmentation helps** and r = 0.5 was not
the optimum. The non-monotonicity (r=0.5 worst of the three) is within the seed noise S1
measured for these conditions, so read only the endpoints. One seed — reseed before claiming.

### S5 — full 78k train set (seed 1914 only; directional, and important)

| Condition | 20k subsample | full 78k | vs its own B0 |
|---|---|---|---|
| B0 | 0.394 | 0.439 | — |
| B2 | 0.384 | 0.355 | -0.084 |
| B3 | 0.304 | **0.188** | **-0.250** |
| B4 | 0.304 | 0.268 | -0.170 |

**DO NOT QUOTE THESE NUMBERS BARE — they are confounded by prediction collapse.**
All three augmented conditions here are flagged `DEGENERACY_SUSPECT` by
`scripts/aggregate_results.py`: their eval-split macro-F1 falls below their own baseline
(B0 0.523; B2 0.503, B4 0.491, **B3 0.466**) and their predictions concentrate on the
majority class (B0 71.1%; B3 **78.7%**, with class 1 falling from 76 predictions to 16).
cASR is conditioned on clean-correct examples, which on this imbalanced dataset are
dominated by the majority class — the hardest class to flip away from. A model that has
stopped using its minority classes therefore scores a better cASR *without being more
robust*, so an unknown fraction of B3's −0.250 is degeneracy rather than defence.

What it might mean if it survives: the 20k subsample understated the method, the baseline
gets more brittle with more clean data while augmented conditions get more robust, and every
S1 number is a conservative floor. What it might equally mean: full-data training with this
recipe degenerates. **One seed cannot tell these apart** — stage R1 reseeds it, and the
decisive diagnostic is whether `majority_pred_share` is high on all three seeds.

The 20k 3-seed grid is *not* affected: macro-F1 there is 0.484–0.503 across all conditions
and B3/B4 are **less** concentrated than B0 (71.7/72.4% vs 75.3%).

### S6 — generality (seed 1914 only; directional). cASR delta vs each column's own B0

| Condition | News x XLM-R | Reviews x Ukr-RoBERTa | Reviews x XLM-R | UNLP x XLM-R |
|---|---|---|---|---|
| (B0 absolute) | 0.118 | 0.615 | 0.394 | 0.334 |
| B2 | -0.004 | -0.018 | -0.010 | -0.013 |
| B3 | -0.033 | **-0.227** | -0.091 | **+0.033** |
| B4 | -0.017 | **-0.214** | -0.090 | -0.003 |

Generality is **real but uneven**, and the pattern is legible: the method pays in proportion
to how lexically fragile the baseline is. Ukr-RoBERTa on Reviews starts at cASR 0.615 and
gains the most (−0.227, p < 0.0001); News starts at 0.118, already robust, and gains little
(−0.033, p < 0.001).

**UNLP is inconclusive, not negative.** The +0.033 in the table is a difference of raw cASR
means; the *paired* test — the valid comparison, since the two models have different
clean-correct sets — gives B3 **−0.003 (p = 1.00)**, B4 −0.020 (p = 0.41), B2 −0.035
(p = 0.12). Nothing is significant in either direction at one seed. An earlier version of
this document said "B3 is actively worse" on UNLP; that was wrong and is retracted. The
hypothesis worth testing (stage R3) is that manipulation detection keys on rhetorical rather
than lexical signal, so single-word synonym substitution is not its threat model — but the
data does not yet support saying so. Do not claim cross-task generality; claim it for
sentiment/topic classification and report UNLP as untested.

*(Superseded — see "Round 2 results" below: R3 reseeded UNLP to 3 seeds and it is now a
confirmed negative result, not merely untested.)*

### What is and is not claimable

| Finding | Evidence | Verdict |
|---|---|---|
| Direction of adversarial selection is the mechanism (B5 control) | 3 seeds, +0.169, all p < 0.0001 | **Claimable** |
| SAAA (B4) beats baseline | 3/3 seeds, range 0.020 | **Claimable** |
| B4 is more *stable* than B3 | range 0.020 vs 0.152 | **Claimable** |
| B4 has a lower *mean* than B3 | 1/3 seeds @3x6, 2/3 @10x20 | **Not claimable** |
| WSD filter as a safeguard on search width | 2/3 seeds | Supported, not established |
| RQ2: WSD-filtered beats unfiltered | 3/3 seeds, -0.033 | Claimable, modest |
| RQ4: no cross-family transfer, both directions | 3 seeds each side | **Claimable** |
| Naive augmentation harms robustness | did not replicate (p = 0.43) | **Retracted** |
| Ratio, generality (Ukr-RoBERTa, News) | 1 seed each | Directional only |
| Full-78k gains | 1 seed **and** flagged for prediction collapse | **Do not report** until R1 |
| UNLP is a negative case | paired p = 1.00 at 1 seed | **Not supported** — untested, not negative |
| B6/B7 results reflect distribution, not label noise | antonym rate 0.3% vs 0.0% | Claimable |

## Round 2 results — COMPLETE (9/9 follow-up stages, 46.2 h, finished 2026-09-19)

24/24 stages across both rounds, 124.3 h total GPU. These stages reseeded every
single-seed claim from Round 1 and resolve every open question from that round.

### R1 — full-78k reseeded (3/3 seeds): the collapse is real, and it explains the "win"

| | seed1914 | seed2024 | seed7 |
|---|---|---|---|
| B0 cASR / macro-F1 / majority-share | 0.439 / 0.523 / 71.1% | 0.393 / 0.500 / 74.7% | 0.397 / 0.496 / 75.6% |
| B3 cASR / macro-F1 / majority-share | 0.188 / **0.466** / **78.7%** | 0.401 / 0.504 / 76.7% | 0.224 / **0.466** / 75.7% |
| B3 vs B0 (paired) | −0.284, p<0.0001 | **+0.000, p=1.00** | −0.176, p<0.0001 |
| B4 cASR / macro-F1 | 0.268 / 0.491 | 0.346 / 0.491 | 0.299 / 0.506 |
| B4 vs B0 (paired) | −0.192, p<0.0001 | −0.043, p=0.002 | −0.105, p<0.0001 |

**The apparent full-data win for B3 does not survive reseeding, and the one seed that
resolves the ambiguity resolves it against B3.** On seed2024 — the only one of the three
where B3's eval macro-F1 (0.504) does *not* drop below B0's (0.500), i.e. the only seed
without collapse — B3 gives **exactly zero** robustness gain (p = 1.00). On the two seeds
where it does collapse (macro-F1 −0.057 and −0.030, majority-share up 5–8 points), it
also "wins" by a large margin. That correlation is the whole explanation: **B3's full-78k
robustness number was mostly the collapse, not a defence.**

**B4 (SAAA) is the one that survives.** It beats B0 on 3/3 seeds, every p < 0.005, with far
smaller macro-F1 movement (0.491/0.491/0.506 vs B0's 0.523/0.500/0.496 — a genuine but
modest cost, not a collapse). **Conclusion for the write-up: report B4's full-78k numbers
as a real, if modest, gain (mean cASR delta ≈ −0.11); do not report B3's.**

### R2 — Ukr-RoBERTa reseeded + B5 control (3/3 seeds): the mechanism generalises, the ranking does not

| | seed7 | seed1914 | seed2024 | mean |
|---|---|---|---|---|
| B0 | 0.617 | 0.615 | 0.563 | 0.598 |
| B3 | 0.379 | 0.387 | 0.394 | **0.387** (range 0.015) |
| B4 | 0.437 | 0.400 | 0.406 | 0.414 (range 0.037) |
| B5 | 0.787 | 0.784 | 0.756 | 0.776 |

No cell here is `DEGENERACY_SUSPECT` — this result is clean.

- **The B5 mechanism control replicates on a second architecture.** Anti-adversarial
  selection is far worse than baseline on 3/3 seeds (+0.177/+0.184/+0.203, all p < 0.0001) —
  the same decisive margin as on XLM-R. RQ3's mechanism is not an XLM-R artifact.
- **Generality is confirmed and large**: B3/B4 both beat B0 on 3/3 seeds here, with a much
  bigger margin (−0.16 to −0.26) than on XLM-R/Reviews (−0.09).
- **The ranking reverses.** On XLM-R, B4 was the more *stable* condition (range 0.020 vs
  B3's 0.152) with no clear mean advantage. On Ukr-RoBERTa, **B3 is both the lower-mean
  AND the more stable condition** (mean 0.387 vs B4's 0.414, range 0.015 vs 0.037; pooled
  B3-vs-B4 favours B3 on 3/3 seeds, p < 0.0001). **"SAAA is more reliable than plain
  adversarial selection" does not generalise across architecture — state the finding as
  architecture-dependent, not universal.**

### R3 — UNLP reseeded (3/3 seeds): confirmed inconclusive, leaning null

| | seed1914 | seed2024 | seed7 |
|---|---|---|---|
| B0->B2 | −0.035, p=0.12 | −0.074, p=0.001 | −0.034, p=0.19 |
| B0->B3 | −0.003, p=1.00 | −0.132, p=0.0005 | +0.017, p=0.52 |
| B0->B4 | −0.020, p=0.41 | +0.027, p=0.26 | −0.030, p=0.22 |

Only 3 of 9 seed x condition comparisons reach significance, with no condition significant
on more than 1/3 seeds and no consistent direction (B4 is nominally *worse* than baseline
on seed2024). Some scattered degeneracy flags (one per condition, different seeds, no
pattern — consistent with the noise expected on a ~3.8k-row dataset, not systematic
collapse). **This is now a real negative result, not a data gap**: the method does not
reliably help UNLP. Consistent with the hypothesis that manipulation detection is a
rhetorical rather than lexical signal — report it as supporting evidence, not proof, since
the mechanism was never tested directly.

### R4 — ratio r=1.0 reseeded (3/3 seeds): direction confirmed, not unanimous

Same-condition paired test, r=0.5 -> r=1.0:

| Condition | seed1914 | seed2024 | seed7 |
|---|---|---|---|
| B2 | −0.044, p=0.0007 | **+0.031, p=0.017** | −0.007, p=0.57 |
| B3 | −0.091, p<0.0001 | **+0.030, p=0.006** | −0.166, p<0.0001 |
| B4 | −0.052, p<0.0001 | +0.005, p=0.73 (null) | −0.100, p<0.0001 |

r=1.0 helps on 2/3 seeds for every condition, and seed2024 reverses significantly for B2
and B3 but is merely *null* (never significantly worse) for B4. **B4 is the only condition
where increasing the ratio never hurts**; for B2/B3 the ratio effect is itself seed-
dependent, which is a finding in its own right (this project's hyperparameters interact
with training-run variance, not just with the method).

### Updated claimability matrix

| Finding | Evidence | Verdict |
|---|---|---|
| Direction of adversarial selection is the mechanism (B5 control) | 3+3 seeds, 2 architectures, all p < 0.0001 | **Claimable, and now architecture-general** |
| SAAA (B4) beats baseline | 3/3 seeds x 2 architectures x full-78k | **Claimable** |
| B4 is more *stable* than B3 | True on XLM-R (0.020 vs 0.152), **false on Ukr-RoBERTa** (0.037 vs 0.015) | **Claimable only as architecture-dependent** |
| B4 has a lower mean than B3 | XLM-R: no. Ukr-RoBERTa: no, B3 is lower. Full-78k: no (B3's low mean is collapse) | **Not claimable anywhere** — reframe around reliability/collapse-resistance, not mean |
| WSD filter as a safeguard on search width | 2/3 seeds | Supported, not established |
| RQ2: WSD-filtered beats unfiltered | 3/3 seeds (main), replicated direction on Ukr-RoBERTa | Claimable, modest |
| RQ4: no cross-family transfer, both directions | 3 seeds each side, antonym rate rules out label noise | **Claimable** |
| Full-78k B3 "gain" | 3 seeds: collapses on 2, null on the one that doesn't | **Retracted as a robustness claim** — it is the collapse |
| Full-78k B4 gain | 3/3 seeds, modest macro-F1 cost | **Claimable**, mean cASR delta ~ -0.11 |
| Generality (Ukr-RoBERTa) | 3/3 seeds, clean (no degeneracy flags), large effect | **Claimable** |
| Generality (News) | 1 seed | Directional only (not reseeded — smallest, lowest-priority effect) |
| UNLP has no reliable effect | 3/3 seeds, 1/9 comparisons significant, no consistent direction | **Claimable as a negative result** |
| Ratio r=1.0 beats r=0.5 | 2/3 seeds for B2/B3, B4 never reverses | **Claimable for B4; directional for B2/B3** |
| Naive augmentation harms robustness | did not replicate (p = 0.43) | **Retracted** |

**Campaign is now closed.** No further stages are queued. The only findings still resting
on a single seed are News generality and the r=0.25 ratio point — both low-priority.

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
