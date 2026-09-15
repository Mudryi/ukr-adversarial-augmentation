I would frame the paper around one central question:

> **Can automatically generated, sense-aware synonym augmentation improve the robustness of Ukrainian text classifiers without sacrificing clean accuracy?**

That gives you a clean extension from *attack/evaluation* into **data augmentation, adversarial training, and robust text classification**. It also directly addresses the lightweight-defense gap identified in your survey. 

The important part is to keep the scope disciplined. I would **not** make this “test every defense.” The core paper should compare different **training-time augmentation strategies**, with inference-time ensembling as one optional secondary experiment.

## 1. Research questions and hypotheses

I would organize the whole paper around four RQs.

**RQ1 — Does synonym-based data augmentation improve adversarial robustness?**

Compare normal training against automatic synonym augmentation.

Expected hypothesis:

$$
H_1:\quad Robustness(\text{SynAug}) > Robustness(\text{Baseline})
$$

while:

$$
Acc_{clean}(\text{SynAug}) \approx Acc_{clean}(\text{Baseline})
$$

You already observed exactly this pattern in the multimodal setting: synonym-augmented fine-tuning improved perturbed performance while leaving clean performance nearly unchanged. 

**RQ2 — Does sense-aware augmentation outperform naive synonym augmentation?**

This is probably the most important thesis-specific question.

Compare:

* random dictionary synonyms;
* WSD-filtered dictionary synonyms.

Your current WSD filtering improves the proportion of good TextFooler replacements from roughly 39% to 47%, so there is already empirical motivation to expect better training examples. 

**RQ3 — Is adversarial augmentation better than random augmentation?**

Compare:

* random acceptable synonym;
* synonym deliberately selected because it reduces classifier confidence;
* same adversarial procedure + WSD filtering.

This distinguishes ordinary **data augmentation** from **adversarial training**.

**RQ4 — Does the defense generalize to attacks not used during training?**

For example:

> Train using TextFooler-like adversarial augmentation → evaluate under BERT-Attack.

This is critical. Otherwise reviewers can reasonably say the model merely learned the perturbation generator.

---

# 2. Priority order

I would execute the project in this order.

| Priority | Experiment                                     | Why                                       |
| -------- | ---------------------------------------------- | ----------------------------------------- |
| **P0**   | Reproduce baseline classifier + attack results | Validate pipeline                         |
| **P0**   | Random synonym augmentation                    | Essential augmentation baseline           |
| **P0**   | WSD-aware augmentation                         | Main thesis-specific contribution         |
| **P0**   | Adversarial synonym augmentation               | Establish adversarial-training comparison |
| **P0**   | WSD-aware adversarial augmentation             | Main candidate method                     |
| **P0**   | Cross-attack evaluation                        | Prevent attack-overfitting criticism      |
| **P1**   | Augmentation-rate ablation                     | Makes paper substantially stronger        |
| **P1**   | 3 random seeds / statistical uncertainty       | Needed for credible training comparison   |
| **P1**   | Analysis by dataset / substitution count       | Explains results                          |
| **P2**   | Inference-time synonym ensemble                | Extra defense comparison                  |
| **P2**   | Third classifier architecture                  | Only if everything else is done           |
| **P3**   | Human annotation of new augmentation data      | Avoid unless absolutely necessary         |

The goal should be to get **all P0 experiments completed first**. If those produce a coherent result, you already have the paper.

---

# 3. Reuse the existing experimental environment

You should avoid changing datasets or attacks unless something is broken.

Use the existing three tasks:

* **UA Reviews** — 5-class sentiment, ~15k;
* **UA News** — 5-class topic classification, ~150k;
* **UNLP 2025** — binary manipulation detection, ~3.8k.

They deliberately span different text lengths and task types. Your previous work also shows that their robustness behavior differs substantially, which is useful rather than problematic. 

For models, start with:

**Primary**

* XLM-RoBERTa-base
* Ukr-RoBERTa

Do **not** immediately include SBERT.

Two architectures already answer an interesting secondary question:

> Does synonym-based adversarial training behave similarly for a multilingual model and a Ukrainian-specific model?

Add SBERT only if training is cheap and results are already stable.

---

# 4. Step 0 — Freeze the experimental protocol

Before generating anything, create a fixed config.

Use exactly the same:

* train/validation/test splits as previous papers;
* preprocessing;
* label definitions;
* tokenizer/model checkpoints;
* attack test sets;
* evaluation code.

Most importantly:

### Never augment validation or test data.

Augmentation is applied only to:

$$
D_{train}
$$

Test sets stay frozen.

Also, do **not** tune augmentation parameters based on adversarial test-set performance.

Use validation performance or one development configuration.

This sounds obvious, but because the attack pipeline already exists it would be easy to accidentally optimize against the previous adversarial evaluation set.

---

# 5. Step 1 — Reproduce the baseline

Before doing anything new, rerun:

$$
D_{train} \rightarrow M_{baseline}
$$

for XLM-R and Ukr-RoBERTa.

Measure:

* clean accuracy;
* macro-F1;
* TextFooler robustness;
* BERT-Attack robustness;
* WSD-TextFooler robustness.

Your previous attack setup already gives a reasonable standardized starting point: TextFooler/BERT-Attack used semantic filtering, morphology-aware substitutions, and bounded perturbation. The later work uses SBERT ≥ 0.8, top-50 candidates, and a 20% token perturbation budget. 

**Deliverable:** one baseline results table that roughly reproduces previous findings.

If this fails, fix it before touching augmentation.

---

# 6. Step 2 — Build one unified augmentation generator

This is probably the most important engineering task.

I would define a general function conceptually like:

```text
augment(
    text,
    strategy,
    classifier=None,
    wsd_filter=False,
    max_replacements=1
)
```

All experimental conditions should go through the **same candidate-generation pipeline** where possible.

That prevents differences from coming from unrelated implementation details.

## Strategy A — Random synonym augmentation

For each training example:

1. identify replaceable content words;
2. retrieve dictionary synonyms;
3. inflect candidate to the source morphology;
4. randomly choose one valid candidate;
5. replace one word;
6. preserve the original label.

Example:

```text
Original:
Цей телефон дуже хороший.

Augmented:
Цей телефон дуже гарний.
```

This answers:

> Is simple lexical diversity sufficient?

No victim-model information is used.

---

# 7. Step 3 — WSD-aware synonym augmentation

Same procedure, except candidate synonyms pass your existing WSD filter.

Conceptually:

$$
S(w)=\{s_1,\ldots,s_k\}
$$

becomes:

$$
S_{\text{WSD}}(w,c)
=
\{s\in S(w): sim(sense(w,c),sense(s,c'))>\tau\}.
$$

You already have the relevant machinery.

For comparability I would initially use the existing threshold rather than conducting another large threshold search. Your current implementation uses a sense-similarity threshold around **0.35** and shows a modest validity improvement. 

Then randomly sample from:

$$
S_{\text{WSD}}
$$

instead of the entire dictionary.

This gives an extremely clean comparison:

$$
\text{RandomSyn}
\quad vs \quad
\text{WSD-Syn}
$$

Everything else stays identical.

That comparison itself is potentially one of the paper's strongest findings.

---

# 8. Step 4 — Adversarial synonym augmentation

Now introduce the classifier.

For each candidate replacement \(s\), calculate something like:

$$
I(s)
=
p_M(y|x)-p_M(y|x_s)
$$

where \(x_s\) is the sentence containing the synonym.

Select:

$$
s^* = \arg\max_s I(s).
$$

So instead of choosing a synonym randomly, choose the valid synonym that **most reduces confidence in the gold class**.

Importantly, you do **not need the replacement to flip the prediction**.

This is better for augmentation because otherwise many training examples won't produce adversarial samples.

Think of it as:

> hardest synonym-preserving example available for this input.

This becomes **adversarial synonym augmentation**.

---

# 9. Step 5 — Main proposed method: WSD-aware adversarial augmentation

Combine Steps 3 and 4:

1. extract dictionary candidates;
2. inflect correctly;
3. apply WSD consistency filter;
4. score surviving candidates against classifier;
5. retain the most damaging candidate;
6. add it to training data with the original label.

Formally:

$$
s^*
=
\arg\max_{s\in S_{\text{WSD}}}
\left[
p(y|x)-p(y|x_s)
\right].
$$

This gives you your cleanest “method.”

I would probably call it something conservative such as:

**Sense-Aware Adversarial Augmentation (SAAA)**

rather than inventing a dramatic method name.

---

# 10. What exactly counts as “adversarial training”?

There is an important terminology point.

If you:

1. train baseline;
2. generate adversarial examples once;
3. retrain on clean + adversarial examples;

that is reasonably described as **offline adversarial training / adversarial data augmentation**.

If you regenerate examples repeatedly against the evolving model during training, that is stronger **online adversarial training**.

For this paper I recommend the offline version.

Pipeline:

$$
M_0 = Train(D)
$$

generate:

$$
D_{adv}=Attack(M_0,D)
$$

then:

$$
M_{robust}=Train(D \cup D_{adv}).
$$

It is drastically simpler, reproducible, and compute-friendly.

Don't turn this paper into an online attack/training system unless the offline method fails.

---

# 11. The five core training conditions

You ultimately want exactly this comparison:

| ID     | Training dataset                              |
| ------ | --------------------------------------------- |
| **B0** | Original                                      |
| **B1** | Original + random synonym augmentation        |
| **B2** | Original + WSD synonym augmentation           |
| **B3** | Original + adversarial synonym augmentation   |
| **B4** | Original + WSD-aware adversarial augmentation |

This is the heart of the paper.

Everything beyond this is supporting evidence.

---

# 12. Control augmentation size carefully

This is very important scientifically.

Suppose B1 generates 50k samples while B4 generates only 20k.

Then differences could simply come from dataset size.

So compare all approaches using approximately the same augmentation ratio.

Define:

$$
r=\frac{|D_{aug}|}{|D_{original}|}.
$$

Start with:

$$
r=0.5
$$

or perhaps:

$$
r=1.0.
$$

Meaning either:

* one augmented example per two originals; or
* one augmented example per original.

I would pilot both, but don't begin with a huge grid.

---

# 13. First pilot: one model × one dataset

Before running 30 models, use:

**XLM-R + UA Reviews**

Why Reviews?

Your previous studies consistently show strong lexical vulnerability on Reviews, so there should be enough signal to observe a defense effect. 

Run:

* B0 baseline;
* B1 random;
* B2 WSD;
* B3 adversarial;
* B4 WSD-adversarial.

Initially use **one seed**.

Your decision point is:

> Does at least one augmentation strategy clearly improve robust accuracy/cASR without destroying clean performance?

If **nothing works here**, investigate before scaling.

---

# 14. Primary evaluation

Every trained classifier should be evaluated against:

### A. Clean data

Report:

* accuracy;
* macro-F1.

Macro-F1 is particularly worth adding because Reviews is heavily imbalanced.

### B. TextFooler

Dictionary-based attack.

### C. BERT-Attack

MLM-based attack.

This is especially important because BERT-Attack uses a fundamentally different candidate generator and has historically produced more semantic drift but fewer grammar issues than TextFooler. 

### D. WSD-filtered TextFooler

This is arguably your highest-quality existing adversarial evaluation.

It tests performance on a more semantically constrained attack.

---

# 15. Metrics

Do not report only adversarial accuracy.

Use:

### Clean accuracy

$$
Acc_{clean}
$$

### Adversarial accuracy

$$
Acc_{adv}
$$

### Accuracy drop

$$
\Delta=Acc_{clean}-Acc_{adv}
$$

### Conditional attack success rate

$$
cASR =
P(\hat y_{adv}\neq y
\mid
\hat y_{clean}=y)
$$

This should probably be the **primary robustness metric**, consistent with your newer robustness work. 

### Prediction flip rate

$$
Flip=P(\hat y_{clean}\neq \hat y_{adv})
$$

### Macro-F1

For both clean and adversarial data.

### Perturbation rate

Average percentage of tokens changed.

This prevents the attack comparison from being misleading.

---

# 16. The single most important extra experiment: cross-attack generalization

This should be **P0**, not optional.

Example:

Train:

$$
M_{TF}=Train(D+D_{TF})
$$

but evaluate under:

$$
Attack_{BERT}(M_{TF})
$$

and vice versa.

You want something like:

| Training           |   TF | BERT | WSD-TF |
| ------------------ | ---: | ---: | -----: |
| None               | poor | poor |   poor |
| Random             |    ↑ |    ↑ |      ↑ |
| TF adversarial     |   ↑↑ |    ↑ |      ↑ |
| WSD-TF adversarial |   ↑↑ |   ↑↑ |     ↑↑ |

The question becomes:

> Does training against one synonym distribution create general lexical robustness?

If yes, this substantially upgrades the paper.

---

# 17. P1 ablation: augmentation amount

Once you identify your best method, do **not** rerun every rate for everything.

Pick:

**XLM-R + Reviews**

and evaluate:

$$
r\in\{0.25,0.5,1.0\}.
$$

Optionally:

$$
2.0
$$

only if generation is cheap.

Plot:

**augmentation ratio → clean accuracy**

and:

**augmentation ratio → cASR**

This gives you the robustness/augmentation trade-off.

A useful result would be:

> Most robustness improvement is obtained by 0.5× augmentation, with little additional gain from doubling the augmented corpus.

That is scientifically meaningful and practically useful.

---

# 18. P1 ablation: one synonym vs multiple substitutions

Your LLM robustness work found an important pattern: examples with many replacements were substantially less reliable as genuine meaning-preserving perturbations; one-word changes gave cleaner evidence. 

Therefore I would make the default training augmentation:

> **one substituted word per training sample.**

Then optionally test:

* one substitution;
* up to two;
* up to 20%.

My expectation is that **one-word augmentation is likely the cleanest choice**.

It also makes the method cheaper.

---

# 19. Statistical design

For screening:

> one seed is fine.

For final reported results:

> **three seeds** for at least B0, B2, B3, B4.

Report:

$$
mean \pm std
$$

for clean performance.

For adversarial comparisons, use paired evaluation because the methods see the same underlying test examples.

Given your previous work, paired bootstrap or McNemar-style comparison would fit nicely.

At minimum report confidence intervals for:

* cASR;
* adversarial accuracy;
* difference relative to baseline.

Don't make a 1–2 percentage point gain into a claim without uncertainty.

---

# 20. Dataset-generation diagnostics — mostly automatic

You specifically want to avoid manual work, so collect automatic diagnostics during augmentation.

For every generated example save:

```text
dataset
sample_id
original_text
augmented_text
original_word
replacement
strategy
wsd_similarity
sentence_similarity
gold_label
baseline_probability_before
baseline_probability_after
confidence_drop
```

Then you can later analyze:

### Candidate coverage

$$
Coverage =
\frac{\# examples\ successfully\ augmented}
{\# examples}
$$

### Mean WSD similarity

### Mean SBERT similarity

### Confidence reduction

$$
p(y|x)-p(y|x')
$$

### Replacement frequency

### POS distribution

### Number of unique source/replacement words

All of that can become useful tables/figures with no annotation.

---

# 21. Very small manual sanity check only if needed

I would **not plan a new 500-example human study**.

You already demonstrated in earlier work that automatic synonym attacks can contain semantic/grammatical errors, and the newer study directly evaluated WSD filtering. 

For this paper, ideally reuse that evidence.

If a reviewer-level sanity check seems necessary, inspect something like:

* 30 random augmentation examples per method;

not hundreds.

The paper is about the **effect of augmentation on robustness**, not another synonym-quality benchmark.

---

# 22. Optional P2: inference-time ensemble

Only after the main experiments work.

Take:

$$
x
$$

and automatically produce perhaps 5 WSD-filtered variants:

$$
x'_1,\ldots,x'_5.
$$

Predict all:

$$
p(y|x),p(y|x'_1),...,p(y|x'_5)
$$

and average:

$$
p_{ensemble}(y)
=
\frac{1}{6}
\sum_i p_i(y).
$$

Compare:

* baseline;
* B4 adversarially trained model;
* baseline + ensemble;
* B4 + ensemble.

This directly contrasts:

**training-time compute**

versus

**inference-time compute**.

Your survey already identifies randomized/inference-time smoothing as a defense family, so this gives the paper a useful connection without forcing you into certified robustness. 

But I would drop this immediately if time gets tight.

---

# 23. Full experiment matrix — don't run everything blindly

The naïve full matrix is:

$$
3\ datasets
\times
2\ models
\times
5\ training\ strategies
=
30
$$

trained classifiers.

With three seeds:

$$
90\ runs.
$$

That is possible, but inefficient.

I recommend staged compute.

### Stage A — screening

**Reviews × XLM-R × 5 strategies × 1 seed**

= 5 runs.

### Stage B — confirm generality

Best ~4 strategies:

$$
3\ datasets\times2\ models\times4
=
24
$$

runs.

### Stage C — uncertainty

Repeat important runs with seeds 2–3.

This way you don't spend GPU time replicating a method that obviously fails.

---

# 24. Minimum successful paper

If time becomes a problem, the minimum paper I'd still be comfortable submitting contains:

1. three Ukrainian classification datasets;
2. two transformer architectures;
3. Baseline;
4. Random Synonym Augmentation;
5. WSD Synonym Augmentation;
6. Adversarial Synonym Augmentation;
7. WSD-Adversarial Augmentation;
8. clean evaluation;
9. TextFooler;
10. BERT-Attack;
11. WSD-TextFooler;
12. cross-attack generalization;
13. one augmentation-rate ablation;
14. uncertainty across final runs.

That's already a coherent paper.

You do **not** need inference ensembling, another language, LLM evaluation, certified robustness, RL, or a new manually labeled dataset.

---

# 25. What outcomes would actually be interesting?

Don't assume B4 has to win.

There are several publishable outcomes.

### Outcome A — ideal

$$
WSDAdv > Adv > WSDRandom > Random > Baseline
$$

Excellent story:

> semantic quality + adversarial difficulty both matter.

### Outcome B

$$
Adv \approx WSDAdv > Random
$$

Still useful:

> adversarial selection matters; WSD filtering offers little additional downstream benefit.

### Outcome C

$$
WSDRandom > Adv
$$

Actually quite interesting:

> high-quality semantic diversity is more useful than attack-targeted but noisy augmentation.

### Outcome D

All augmentation methods increase robustness but decrease clean accuracy.

Then paper becomes about the:

> **clean-robustness trade-off**.

### Outcome E

Methods work on Reviews/UNLP but not News.

Also plausible and useful because your previous work already shows strong dataset-specific attack behavior. 

So don't engineer the experiment around proving that your proposed method wins.

---

# 26. Resources you need

You already have most of them.

**Existing resources to reuse**

* UA Reviews dataset;
* UA News dataset;
* UNLP 2025 dataset;
* existing 80/10/10 splits;
* Ukr-RoBERTa;
* XLM-RoBERTa;
* synonym dictionary;
* morphological inflection code;
* TextFooler implementation;
* BERT-Attack implementation;
* SBERT semantic filtering;
* WSD model/filter;
* existing training/evaluation scripts.

Your original benchmark already packaged dataset loaders, fine-tuning, and attack pipelines, which is why this follow-up should be engineering-light. 

**New code required**

Mostly:

```text
augmentation/
    random_synonym.py
    wsd_synonym.py
    adversarial_synonym.py
    wsd_adversarial_synonym.py

generate_augmented_dataset.py
train_augmented.py
evaluate_robustness.py
aggregate_results.py
```

I would **pre-generate and cache all augmentation datasets** rather than generating synonyms during training.

That makes runs deterministic and debugging much easier.

---

# 27. Paper structure you can effectively fill while experiments run

The final paper could be extremely conventional:

**1. Introduction**
SSA vulnerability → Ukrainian problem → previous work evaluates attacks → defenses underexplored → propose sense-aware adversarial augmentation.

**2. Related Work**
SSA → adversarial training → data augmentation → low-resource robustness → WSD.

**3. Method**
Random augmentation → WSD augmentation → adversarial augmentation → WSD-adversarial augmentation.

**4. Experimental Setup**
3 datasets → 2 models → attacks → metrics.

**5. Results**
Clean performance → robustness → cross-attack generalization.

**6. Analysis**
augmentation ratio → dataset differences → maybe confidence/coverage.

**7. Conclusion**

Your survey already establishes that lightweight adversarial-training and morphology-aware defenses are an open Ukrainian direction. 

---

# 28. Concrete execution order

If I were doing this project, my actual sequence would be:

1. **Freeze existing splits and attack configs.**
2. **Reproduce XLM-R + Reviews baseline.**
3. **Implement cached random synonym augmentation.**
4. **Implement cached WSD-filtered augmentation.**
5. **Implement model-confidence adversarial selection.**
6. **Combine it with WSD filtering.**
7. **Train the five XLM-R/Reviews pilot models.**
8. **Evaluate all five on clean + TF + BERT + WSD-TF.**
9. **Inspect whether the research hypothesis has signal.**
10. **Run cross-attack evaluation immediately.**
11. **Scale the four useful methods to Ukr-RoBERTa and the other two datasets.**
12. **Run augmentation-ratio ablation on XLM-R/Reviews.**
13. **Repeat final important runs using three seeds.**
14. **Compute CIs/paired comparisons.**
15. **Only then decide whether inference-time ensembling adds enough value.**
16. **Write the results around what actually happened, rather than around which method was expected to win.**

The key design principle is that the paper should **not** become another attack-quality study. You already have that part. This one should clearly move the thesis into **automatic data augmentation → adversarial training → robust Ukrainian text classification**, with WSD acting as the bridge between your earlier semantic work and the new defense work.
