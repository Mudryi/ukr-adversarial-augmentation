# Baseline / augmentation metrics (macro-F1, cASR, flip-rate)

Derived from `examples.jsonl` per-row data; not present in `ukr-synonym-robustness/src/evaluation/metrics.py`'s `Summary`.

`eval_macro_f1` is the full eval-split figure from the checkpoint's TRAINING_COMPLETE marker -- judge clean performance on it, NOT on a macro-F1 computed over the attacked subset. `majority_pred_share` and `degeneracy_flag` guard against a cASR 'gain' that is really a model abandoning its minority classes.

> **24 flagged cell(s).** Their cASR must not be quoted as a robustness result without reporting the macro-F1 drop alongside it:
>
> - `reviews/xlmr_base/B2/seed1914/full78k` eval macro-F1 0.503, majority share 73.3% — DEGENERACY_SUSPECT(-0.020)
> - `reviews/xlmr_base/B2/seed2024/full78k` eval macro-F1 0.471, majority share 79.9% — DEGENERACY_SUSPECT(-0.029)
> - `reviews/xlmr_base/B3/seed1914/full78k` eval macro-F1 0.466, majority share 78.7% — DEGENERACY_SUSPECT(-0.057)
> - `reviews/xlmr_base/B3/seed7/full78k` eval macro-F1 0.466, majority share 75.7% — DEGENERACY_SUSPECT(-0.030)
> - `reviews/xlmr_base/B4/seed1914/full78k` eval macro-F1 0.491, majority share 76.7% — DEGENERACY_SUSPECT(-0.032)
> - `unlp/xlmr_base/B2/seed7` eval macro-F1 0.766, majority share 54.2% — DEGENERACY_SUSPECT(-0.021)
> - `unlp/xlmr_base/B3/seed2024` eval macro-F1 0.738, majority share 58.9% — DEGENERACY_SUSPECT(-0.036)
> - `unlp/xlmr_base/B4/seed7` eval macro-F1 0.762, majority share 63.6% — DEGENERACY_SUSPECT(-0.025)

| attack | dataset | model | condition | seed | variant | wsd | n_total | clean_accuracy | eval_macro_f1 | adv_accuracy | delta | cASR | flip_rate | majority_pred_share | degeneracy_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| textfooler | news | xlmr_base | B0 | 1914 |  |  | 1500 | 0.918 | 0.8974 | 0.81 | 0.108 | 0.1176 | 0.108 | 0.3453 |  |
| textfooler | news | xlmr_base | B0 | 1914 |  | wsd035 | 1500 | 0.918 | 0.8974 | 0.8207 | 0.0973 | 0.106 | 0.0973 | 0.3453 |  |
| textfooler | news | xlmr_base | B2 | 1914 |  |  | 1500 | 0.924 | 0.8998 | 0.8187 | 0.1053 | 0.114 | 0.1053 | 0.3367 |  |
| textfooler | news | xlmr_base | B2 | 1914 |  | wsd035 | 1500 | 0.924 | 0.8998 | 0.8273 | 0.0967 | 0.1046 | 0.0967 | 0.3367 |  |
| textfooler | news | xlmr_base | B3 | 1914 |  |  | 1500 | 0.9173 | 0.8992 | 0.8393 | 0.078 | 0.085 | 0.078 | 0.3407 |  |
| textfooler | news | xlmr_base | B3 | 1914 |  | wsd035 | 1500 | 0.9173 | 0.8992 | 0.8427 | 0.0747 | 0.0814 | 0.0747 | 0.3407 |  |
| textfooler | news | xlmr_base | B4 | 1914 |  |  | 1500 | 0.9213 | 0.8994 | 0.8287 | 0.0927 | 0.1006 | 0.0927 | 0.3427 |  |
| textfooler | news | xlmr_base | B4 | 1914 |  | wsd035 | 1500 | 0.9213 | 0.8994 | 0.838 | 0.0833 | 0.0904 | 0.0833 | 0.3427 |  |
| textfooler | reviews | ukr_roberta | B0 | 1914 |  |  | 1500 | 0.7407 | 0.451 | 0.2853 | 0.4553 | 0.6148 | 0.4553 | 0.764 |  |
| textfooler | reviews | ukr_roberta | B0 | 1914 |  | wsd035 | 1500 | 0.7407 | 0.451 | 0.308 | 0.4327 | 0.5842 | 0.4327 | 0.764 |  |
| textfooler | reviews | ukr_roberta | B0 | 2024 |  |  | 1500 | 0.738 | 0.4589 | 0.3227 | 0.4153 | 0.5628 | 0.4153 | 0.7647 |  |
| textfooler | reviews | ukr_roberta | B0 | 2024 |  | wsd035 | 1500 | 0.738 | 0.4589 | 0.3467 | 0.3913 | 0.5303 | 0.3913 | 0.7647 |  |
| textfooler | reviews | ukr_roberta | B0 | 7 |  |  | 1500 | 0.7273 | 0.4526 | 0.2787 | 0.4487 | 0.6169 | 0.4487 | 0.756 |  |
| textfooler | reviews | ukr_roberta | B0 | 7 |  | wsd035 | 1500 | 0.7273 | 0.4526 | 0.302 | 0.4253 | 0.5848 | 0.4253 | 0.756 |  |
| textfooler | reviews | ukr_roberta | B2 | 1914 |  |  | 1500 | 0.7173 | 0.4549 | 0.2893 | 0.428 | 0.5967 | 0.428 | 0.7353 |  |
| textfooler | reviews | ukr_roberta | B2 | 1914 |  | wsd035 | 1500 | 0.7173 | 0.4549 | 0.31 | 0.4073 | 0.5678 | 0.4073 | 0.7353 |  |
| textfooler | reviews | ukr_roberta | B2 | 2024 |  |  | 1500 | 0.7373 | 0.4439 | 0.3873 | 0.35 | 0.4747 | 0.35 | 0.7847 |  |
| textfooler | reviews | ukr_roberta | B2 | 2024 |  | wsd035 | 1500 | 0.7373 | 0.4439 | 0.4053 | 0.332 | 0.4503 | 0.332 | 0.7847 |  |
| textfooler | reviews | ukr_roberta | B2 | 7 |  |  | 1500 | 0.7153 | 0.4516 | 0.27 | 0.4453 | 0.6226 | 0.4453 | 0.7227 |  |
| textfooler | reviews | ukr_roberta | B2 | 7 |  | wsd035 | 1500 | 0.7153 | 0.4516 | 0.2873 | 0.428 | 0.5983 | 0.428 | 0.7227 |  |
| textfooler | reviews | ukr_roberta | B3 | 1914 |  |  | 1500 | 0.7247 | 0.452 | 0.444 | 0.2807 | 0.3873 | 0.2807 | 0.7487 |  |
| textfooler | reviews | ukr_roberta | B3 | 1914 |  | wsd035 | 1500 | 0.7247 | 0.452 | 0.45 | 0.2747 | 0.379 | 0.2747 | 0.7487 |  |
| textfooler | reviews | ukr_roberta | B3 | 2024 |  |  | 1500 | 0.712 | 0.4522 | 0.4313 | 0.2807 | 0.3942 | 0.2807 | 0.7327 |  |
| textfooler | reviews | ukr_roberta | B3 | 2024 |  | wsd035 | 1500 | 0.712 | 0.4522 | 0.4487 | 0.2633 | 0.3699 | 0.2633 | 0.7327 |  |
| textfooler | reviews | ukr_roberta | B3 | 7 |  |  | 1500 | 0.7367 | 0.4577 | 0.4573 | 0.2793 | 0.3792 | 0.2793 | 0.752 |  |
| textfooler | reviews | ukr_roberta | B3 | 7 |  | wsd035 | 1500 | 0.7367 | 0.4577 | 0.4733 | 0.2633 | 0.3575 | 0.2633 | 0.752 |  |
| textfooler | reviews | ukr_roberta | B4 | 1914 |  |  | 1500 | 0.726 | 0.4503 | 0.4353 | 0.2907 | 0.4004 | 0.2907 | 0.7453 |  |
| textfooler | reviews | ukr_roberta | B4 | 1914 |  | wsd035 | 1500 | 0.726 | 0.4503 | 0.45 | 0.276 | 0.3802 | 0.276 | 0.7453 |  |
| textfooler | reviews | ukr_roberta | B4 | 2024 |  |  | 1500 | 0.7267 | 0.4513 | 0.432 | 0.2947 | 0.4055 | 0.2947 | 0.744 |  |
| textfooler | reviews | ukr_roberta | B4 | 2024 |  | wsd035 | 1500 | 0.7267 | 0.4513 | 0.4507 | 0.276 | 0.3798 | 0.276 | 0.744 |  |
| textfooler | reviews | ukr_roberta | B4 | 7 |  |  | 1500 | 0.7193 | 0.455 | 0.4053 | 0.314 | 0.4365 | 0.314 | 0.7593 |  |
| textfooler | reviews | ukr_roberta | B4 | 7 |  | wsd035 | 1500 | 0.7193 | 0.455 | 0.4253 | 0.294 | 0.4087 | 0.294 | 0.7593 |  |
| textfooler | reviews | ukr_roberta | B5 | 1914 |  |  | 1500 | 0.7267 | 0.4499 | 0.1567 | 0.57 | 0.7844 | 0.57 | 0.7453 |  |
| textfooler | reviews | ukr_roberta | B5 | 1914 |  | wsd035 | 1500 | 0.7267 | 0.4499 | 0.1713 | 0.5553 | 0.7642 | 0.5553 | 0.7453 |  |
| textfooler | reviews | ukr_roberta | B5 | 2024 |  |  | 1500 | 0.726 | 0.4421 | 0.1773 | 0.5487 | 0.7557 | 0.5487 | 0.7547 |  |
| textfooler | reviews | ukr_roberta | B5 | 2024 |  | wsd035 | 1500 | 0.726 | 0.4421 | 0.194 | 0.532 | 0.7328 | 0.532 | 0.7547 |  |
| textfooler | reviews | ukr_roberta | B5 | 7 |  |  | 1500 | 0.736 | 0.4443 | 0.1567 | 0.5793 | 0.7871 | 0.5793 | 0.7593 |  |
| textfooler | reviews | ukr_roberta | B5 | 7 |  | wsd035 | 1500 | 0.736 | 0.4443 | 0.1793 | 0.5567 | 0.7563 | 0.5567 | 0.7593 |  |
| textfooler | reviews | xlmr_base | B0 | 1914 |  |  | 1500 | 0.768 | 0.484 | 0.4653 | 0.3027 | 0.3941 | 0.3027 | 0.7533 |  |
| textfooler | reviews | xlmr_base | B0 | 1914 | full78k |  | 1500 | 0.7507 | 0.5228 | 0.4213 | 0.3293 | 0.4387 | 0.3293 | 0.7113 |  |
| textfooler | reviews | xlmr_base | B0 | 1914 | full78k | wsd035 | 1500 | 0.7507 | 0.5228 | 0.4367 | 0.314 | 0.4183 | 0.314 | 0.7113 |  |
| textfooler | reviews | xlmr_base | B0 | 1914 |  | wsd035 | 1500 | 0.768 | 0.484 | 0.484 | 0.284 | 0.3698 | 0.284 | 0.7533 |  |
| textfooler | reviews | xlmr_base | B0 | 2024 |  |  | 1500 | 0.7627 | 0.4921 | 0.4547 | 0.308 | 0.4038 | 0.308 | 0.746 |  |
| textfooler | reviews | xlmr_base | B0 | 2024 | full78k |  | 1500 | 0.7653 | 0.5 | 0.4647 | 0.3007 | 0.3929 | 0.3007 | 0.7467 |  |
| textfooler | reviews | xlmr_base | B0 | 2024 | full78k | wsd035 | 1500 | 0.7653 | 0.5 | 0.4833 | 0.282 | 0.3685 | 0.282 | 0.7467 |  |
| textfooler | reviews | xlmr_base | B0 | 2024 |  | wsd035 | 1500 | 0.7627 | 0.4921 | 0.4687 | 0.294 | 0.3855 | 0.294 | 0.746 |  |
| textfooler | reviews | xlmr_base | B0 | 7 |  |  | 1500 | 0.77 | 0.4929 | 0.4907 | 0.2793 | 0.3628 | 0.2793 | 0.7687 |  |
| textfooler | reviews | xlmr_base | B0 | 7 | full78k |  | 1500 | 0.7693 | 0.4964 | 0.464 | 0.3053 | 0.3969 | 0.3053 | 0.756 |  |
| textfooler | reviews | xlmr_base | B0 | 7 | full78k | wsd035 | 1500 | 0.7693 | 0.4964 | 0.5007 | 0.2687 | 0.3492 | 0.2687 | 0.756 |  |
| textfooler | reviews | xlmr_base | B0 | 7 |  | wsd035 | 1500 | 0.77 | 0.4929 | 0.5147 | 0.2553 | 0.3316 | 0.2553 | 0.7687 |  |
| textfooler | reviews | xlmr_base | B1 | 1914 |  |  | 1500 | 0.748 | 0.499 | 0.4253 | 0.3227 | 0.4314 | 0.3227 | 0.706 |  |
| textfooler | reviews | xlmr_base | B1 | 1914 |  | wsd035 | 1500 | 0.748 | 0.499 | 0.4487 | 0.2993 | 0.4002 | 0.2993 | 0.706 |  |
| textfooler | reviews | xlmr_base | B1 | 2024 |  |  | 1500 | 0.77 | 0.5011 | 0.5067 | 0.2633 | 0.342 | 0.2633 | 0.7533 |  |
| textfooler | reviews | xlmr_base | B1 | 2024 |  | wsd035 | 1500 | 0.77 | 0.5011 | 0.524 | 0.246 | 0.3195 | 0.246 | 0.7533 |  |
| textfooler | reviews | xlmr_base | B1 | 7 |  |  | 1500 | 0.7653 | 0.497 | 0.4587 | 0.3067 | 0.4007 | 0.3067 | 0.748 |  |
| textfooler | reviews | xlmr_base | B1 | 7 |  | wsd035 | 1500 | 0.7653 | 0.497 | 0.4807 | 0.2847 | 0.372 | 0.2847 | 0.748 |  |
| textfooler | reviews | xlmr_base | B2 | 1914 |  |  | 1500 | 0.7607 | 0.499 | 0.4687 | 0.292 | 0.3839 | 0.292 | 0.7387 |  |
| textfooler | reviews | xlmr_base | B2 | 1914 | full78k |  | 1500 | 0.768 | 0.5027 | 0.4953 | 0.2727 | 0.355 | 0.2727 | 0.7327 | DEGENERACY_SUSPECT(-0.020) |
| textfooler | reviews | xlmr_base | B2 | 1914 | full78k | wsd035 | 1500 | 0.768 | 0.5027 | 0.514 | 0.254 | 0.3307 | 0.254 | 0.7327 | DEGENERACY_SUSPECT(-0.020) |
| textfooler | reviews | xlmr_base | B2 | 1914 | r0.25 |  | 1500 | 0.7647 | 0.4783 | 0.4973 | 0.2673 | 0.3496 | 0.2673 | 0.7487 |  |
| textfooler | reviews | xlmr_base | B2 | 1914 | r0.25 | wsd035 | 1500 | 0.7647 | 0.4783 | 0.512 | 0.2527 | 0.3304 | 0.2527 | 0.7487 |  |
| textfooler | reviews | xlmr_base | B2 | 1914 | r1.0 |  | 1500 | 0.744 | 0.5045 | 0.504 | 0.24 | 0.3226 | 0.24 | 0.7313 |  |
| textfooler | reviews | xlmr_base | B2 | 1914 | r1.0 | wsd035 | 1500 | 0.744 | 0.5045 | 0.5173 | 0.2267 | 0.3047 | 0.2267 | 0.7313 |  |
| textfooler | reviews | xlmr_base | B2 | 1914 |  | wsd035 | 1500 | 0.7607 | 0.499 | 0.4893 | 0.2713 | 0.3567 | 0.2713 | 0.7387 |  |
| textfooler | reviews | xlmr_base | B2 | 2024 |  |  | 1500 | 0.7753 | 0.4966 | 0.506 | 0.2693 | 0.3474 | 0.2693 | 0.754 |  |
| textfooler | reviews | xlmr_base | B2 | 2024 | full78k |  | 1500 | 0.7653 | 0.4706 | 0.5867 | 0.1787 | 0.2334 | 0.1787 | 0.7993 | DEGENERACY_SUSPECT(-0.029) |
| textfooler | reviews | xlmr_base | B2 | 2024 | full78k | wsd035 | 1500 | 0.7653 | 0.4706 | 0.6013 | 0.164 | 0.2143 | 0.164 | 0.7993 | DEGENERACY_SUSPECT(-0.029) |
| textfooler | reviews | xlmr_base | B2 | 2024 | r1.0 |  | 1500 | 0.7727 | 0.5104 | 0.4813 | 0.2913 | 0.377 | 0.2913 | 0.752 |  |
| textfooler | reviews | xlmr_base | B2 | 2024 | r1.0 | wsd035 | 1500 | 0.7727 | 0.5104 | 0.5073 | 0.2653 | 0.3434 | 0.2653 | 0.752 |  |
| textfooler | reviews | xlmr_base | B2 | 2024 |  | wsd035 | 1500 | 0.7753 | 0.4966 | 0.5293 | 0.246 | 0.3173 | 0.246 | 0.754 |  |
| textfooler | reviews | xlmr_base | B2 | 7 |  |  | 1500 | 0.772 | 0.5026 | 0.4993 | 0.2727 | 0.3532 | 0.2727 | 0.7413 |  |
| textfooler | reviews | xlmr_base | B2 | 7 | full78k |  | 1500 | 0.7627 | 0.5135 | 0.4707 | 0.292 | 0.3829 | 0.292 | 0.7333 |  |
| textfooler | reviews | xlmr_base | B2 | 7 | full78k | wsd035 | 1500 | 0.7627 | 0.5135 | 0.4987 | 0.264 | 0.3462 | 0.264 | 0.7333 |  |
| textfooler | reviews | xlmr_base | B2 | 7 | r1.0 |  | 1500 | 0.7613 | 0.4955 | 0.5047 | 0.2567 | 0.3371 | 0.2567 | 0.752 |  |
| textfooler | reviews | xlmr_base | B2 | 7 | r1.0 | wsd035 | 1500 | 0.7613 | 0.4955 | 0.5287 | 0.2327 | 0.3056 | 0.2327 | 0.752 |  |
| textfooler | reviews | xlmr_base | B2 | 7 |  | wsd035 | 1500 | 0.772 | 0.5026 | 0.5213 | 0.2507 | 0.3247 | 0.2507 | 0.7413 |  |
| textfooler | reviews | xlmr_base | B3 | 1914 |  |  | 1500 | 0.762 | 0.503 | 0.5307 | 0.2313 | 0.3036 | 0.2313 | 0.7167 |  |
| textfooler | reviews | xlmr_base | B3 | 1914 | full78k |  | 1500 | 0.7747 | 0.4656 | 0.6287 | 0.146 | 0.1885 | 0.146 | 0.7873 | DEGENERACY_SUSPECT(-0.057) |
| textfooler | reviews | xlmr_base | B3 | 1914 | full78k | wsd035 | 1500 | 0.7747 | 0.4656 | 0.6367 | 0.138 | 0.1781 | 0.138 | 0.7873 | DEGENERACY_SUSPECT(-0.057) |
| textfooler | reviews | xlmr_base | B3 | 1914 | pool10x20 |  | 1500 | 0.748 | 0.4989 | 0.4427 | 0.3053 | 0.4082 | 0.3053 | 0.7167 |  |
| textfooler | reviews | xlmr_base | B3 | 1914 | pool10x20 | wsd035 | 1500 | 0.748 | 0.4989 | 0.4427 | 0.3053 | 0.4082 | 0.3053 | 0.7167 |  |
| textfooler | reviews | xlmr_base | B3 | 1914 | r0.25 |  | 1500 | 0.7653 | 0.4833 | 0.562 | 0.2033 | 0.2657 | 0.2033 | 0.7547 |  |
| textfooler | reviews | xlmr_base | B3 | 1914 | r0.25 | wsd035 | 1500 | 0.7653 | 0.4833 | 0.57 | 0.1953 | 0.2552 | 0.1953 | 0.7547 |  |
| textfooler | reviews | xlmr_base | B3 | 1914 | r1.0 |  | 1500 | 0.7727 | 0.4864 | 0.6007 | 0.172 | 0.2226 | 0.172 | 0.772 |  |
| textfooler | reviews | xlmr_base | B3 | 1914 | r1.0 | wsd035 | 1500 | 0.7727 | 0.4864 | 0.6093 | 0.1633 | 0.2114 | 0.1633 | 0.772 |  |
| textfooler | reviews | xlmr_base | B3 | 1914 |  | wsd035 | 1500 | 0.762 | 0.503 | 0.538 | 0.224 | 0.294 | 0.224 | 0.7167 |  |
| textfooler | reviews | xlmr_base | B3 | 2024 |  |  | 1500 | 0.772 | 0.4935 | 0.5907 | 0.1813 | 0.2349 | 0.1813 | 0.752 |  |
| textfooler | reviews | xlmr_base | B3 | 2024 | full78k |  | 1500 | 0.776 | 0.5039 | 0.4647 | 0.3113 | 0.4012 | 0.3113 | 0.7673 |  |
| textfooler | reviews | xlmr_base | B3 | 2024 | full78k | wsd035 | 1500 | 0.776 | 0.5039 | 0.47 | 0.306 | 0.3943 | 0.306 | 0.7673 |  |
| textfooler | reviews | xlmr_base | B3 | 2024 | pool10x20 |  | 1500 | 0.7647 | 0.4883 | 0.5673 | 0.1973 | 0.2581 | 0.1973 | 0.7627 |  |
| textfooler | reviews | xlmr_base | B3 | 2024 | pool10x20 | wsd035 | 1500 | 0.7647 | 0.4883 | 0.5773 | 0.1873 | 0.245 | 0.1873 | 0.7627 |  |
| textfooler | reviews | xlmr_base | B3 | 2024 | r1.0 |  | 1500 | 0.7733 | 0.5004 | 0.5613 | 0.212 | 0.2741 | 0.212 | 0.7647 |  |
| textfooler | reviews | xlmr_base | B3 | 2024 | r1.0 | wsd035 | 1500 | 0.7733 | 0.5004 | 0.582 | 0.1913 | 0.2474 | 0.1913 | 0.7647 |  |
| textfooler | reviews | xlmr_base | B3 | 2024 |  | wsd035 | 1500 | 0.772 | 0.4935 | 0.5993 | 0.1727 | 0.2237 | 0.1727 | 0.752 |  |
| textfooler | reviews | xlmr_base | B3 | 7 |  |  | 1500 | 0.7627 | 0.5017 | 0.4673 | 0.2953 | 0.3872 | 0.2953 | 0.7507 |  |
| textfooler | reviews | xlmr_base | B3 | 7 | full78k |  | 1500 | 0.768 | 0.4663 | 0.596 | 0.172 | 0.224 | 0.172 | 0.7567 | DEGENERACY_SUSPECT(-0.030) |
| textfooler | reviews | xlmr_base | B3 | 7 | full78k | wsd035 | 1500 | 0.768 | 0.4663 | 0.61 | 0.158 | 0.2057 | 0.158 | 0.7567 | DEGENERACY_SUSPECT(-0.030) |
| textfooler | reviews | xlmr_base | B3 | 7 | pool10x20 |  | 1500 | 0.7627 | 0.4862 | 0.5067 | 0.256 | 0.3357 | 0.256 | 0.7547 |  |
| textfooler | reviews | xlmr_base | B3 | 7 | pool10x20 | wsd035 | 1500 | 0.7627 | 0.4862 | 0.5127 | 0.25 | 0.3278 | 0.25 | 0.7547 |  |
| textfooler | reviews | xlmr_base | B3 | 7 | r1.0 |  | 1500 | 0.7607 | 0.5018 | 0.5833 | 0.1773 | 0.2331 | 0.1773 | 0.748 |  |
| textfooler | reviews | xlmr_base | B3 | 7 | r1.0 | wsd035 | 1500 | 0.7607 | 0.5018 | 0.5933 | 0.1673 | 0.22 | 0.1673 | 0.748 |  |
| textfooler | reviews | xlmr_base | B3 | 7 |  | wsd035 | 1500 | 0.7627 | 0.5017 | 0.48 | 0.2827 | 0.3706 | 0.2827 | 0.7507 |  |
| textfooler | reviews | xlmr_base | B4 | 1914 |  |  | 1500 | 0.7613 | 0.494 | 0.53 | 0.2313 | 0.3039 | 0.2313 | 0.724 |  |
| textfooler | reviews | xlmr_base | B4 | 1914 | full78k |  | 1500 | 0.7673 | 0.4909 | 0.5613 | 0.206 | 0.2685 | 0.206 | 0.7673 | DEGENERACY_SUSPECT(-0.032) |
| textfooler | reviews | xlmr_base | B4 | 1914 | full78k | wsd035 | 1500 | 0.7673 | 0.4909 | 0.5773 | 0.19 | 0.2476 | 0.19 | 0.7673 | DEGENERACY_SUSPECT(-0.032) |
| textfooler | reviews | xlmr_base | B4 | 1914 | pool10x20 |  | 1500 | 0.7493 | 0.4908 | 0.4893 | 0.26 | 0.347 | 0.26 | 0.7333 |  |
| textfooler | reviews | xlmr_base | B4 | 1914 | pool10x20 | wsd035 | 1500 | 0.7493 | 0.4908 | 0.496 | 0.2533 | 0.3381 | 0.2533 | 0.7333 |  |
| textfooler | reviews | xlmr_base | B4 | 1914 | r0.25 |  | 1500 | 0.7613 | 0.4868 | 0.5487 | 0.2127 | 0.2793 | 0.2127 | 0.7533 |  |
| textfooler | reviews | xlmr_base | B4 | 1914 | r0.25 | wsd035 | 1500 | 0.7613 | 0.4868 | 0.5607 | 0.2007 | 0.2636 | 0.2007 | 0.7533 |  |
| textfooler | reviews | xlmr_base | B4 | 1914 | r1.0 |  | 1500 | 0.75 | 0.5043 | 0.562 | 0.188 | 0.2507 | 0.188 | 0.7287 |  |
| textfooler | reviews | xlmr_base | B4 | 1914 | r1.0 | wsd035 | 1500 | 0.75 | 0.5043 | 0.572 | 0.178 | 0.2373 | 0.178 | 0.7287 |  |
| textfooler | reviews | xlmr_base | B4 | 1914 |  | wsd035 | 1500 | 0.7613 | 0.494 | 0.5487 | 0.2127 | 0.2793 | 0.2127 | 0.724 |  |
| textfooler | reviews | xlmr_base | B4 | 2024 |  |  | 1500 | 0.778 | 0.4943 | 0.5573 | 0.2207 | 0.2836 | 0.2207 | 0.7667 |  |
| textfooler | reviews | xlmr_base | B4 | 2024 | full78k |  | 1500 | 0.76 | 0.4914 | 0.4967 | 0.2633 | 0.3465 | 0.2633 | 0.738 |  |
| textfooler | reviews | xlmr_base | B4 | 2024 | full78k | wsd035 | 1500 | 0.76 | 0.4914 | 0.514 | 0.246 | 0.3237 | 0.246 | 0.738 |  |
| textfooler | reviews | xlmr_base | B4 | 2024 | pool10x20 |  | 1500 | 0.7627 | 0.4936 | 0.538 | 0.2247 | 0.2946 | 0.2247 | 0.7367 |  |
| textfooler | reviews | xlmr_base | B4 | 2024 | pool10x20 | wsd035 | 1500 | 0.7627 | 0.4936 | 0.552 | 0.2107 | 0.2762 | 0.2107 | 0.7367 |  |
| textfooler | reviews | xlmr_base | B4 | 2024 | r1.0 |  | 1500 | 0.7653 | 0.4953 | 0.55 | 0.2153 | 0.2814 | 0.2153 | 0.7447 |  |
| textfooler | reviews | xlmr_base | B4 | 2024 | r1.0 | wsd035 | 1500 | 0.7653 | 0.4953 | 0.5607 | 0.2047 | 0.2674 | 0.2047 | 0.7447 |  |
| textfooler | reviews | xlmr_base | B4 | 2024 |  | wsd035 | 1500 | 0.778 | 0.4943 | 0.58 | 0.198 | 0.2545 | 0.198 | 0.7667 |  |
| textfooler | reviews | xlmr_base | B4 | 7 |  |  | 1500 | 0.766 | 0.497 | 0.5347 | 0.2313 | 0.302 | 0.2313 | 0.7593 |  |
| textfooler | reviews | xlmr_base | B4 | 7 | full78k |  | 1500 | 0.7733 | 0.5058 | 0.542 | 0.2313 | 0.2991 | 0.2313 | 0.766 |  |
| textfooler | reviews | xlmr_base | B4 | 7 | full78k | wsd035 | 1500 | 0.7733 | 0.5058 | 0.5487 | 0.2247 | 0.2905 | 0.2247 | 0.766 |  |
| textfooler | reviews | xlmr_base | B4 | 7 | pool10x20 |  | 1500 | 0.7687 | 0.4909 | 0.5873 | 0.1813 | 0.2359 | 0.1813 | 0.768 |  |
| textfooler | reviews | xlmr_base | B4 | 7 | pool10x20 | wsd035 | 1500 | 0.7687 | 0.4909 | 0.604 | 0.1647 | 0.2142 | 0.1647 | 0.768 |  |
| textfooler | reviews | xlmr_base | B4 | 7 | r1.0 |  | 1500 | 0.7647 | 0.4903 | 0.61 | 0.1547 | 0.2023 | 0.1547 | 0.7787 |  |
| textfooler | reviews | xlmr_base | B4 | 7 | r1.0 | wsd035 | 1500 | 0.7647 | 0.4903 | 0.618 | 0.1467 | 0.1918 | 0.1467 | 0.7787 |  |
| textfooler | reviews | xlmr_base | B4 | 7 |  | wsd035 | 1500 | 0.766 | 0.497 | 0.546 | 0.22 | 0.2872 | 0.22 | 0.7593 |  |
| textfooler | reviews | xlmr_base | B5 | 1914 |  |  | 1500 | 0.7487 | 0.5 | 0.2987 | 0.45 | 0.6011 | 0.45 | 0.7027 |  |
| textfooler | reviews | xlmr_base | B5 | 1914 | pool10x20 |  | 1500 | 0.7547 | 0.5119 | 0.284 | 0.4707 | 0.6237 | 0.4707 | 0.706 |  |
| textfooler | reviews | xlmr_base | B5 | 1914 | pool10x20 | wsd035 | 1500 | 0.7547 | 0.5119 | 0.2953 | 0.4593 | 0.6087 | 0.4593 | 0.706 |  |
| textfooler | reviews | xlmr_base | B5 | 1914 |  | wsd035 | 1500 | 0.7487 | 0.5 | 0.3307 | 0.418 | 0.5583 | 0.418 | 0.7027 |  |
| textfooler | reviews | xlmr_base | B5 | 2024 |  |  | 1500 | 0.7747 | 0.4956 | 0.376 | 0.3987 | 0.5146 | 0.3987 | 0.7507 |  |
| textfooler | reviews | xlmr_base | B5 | 2024 | pool10x20 |  | 1500 | 0.756 | 0.5021 | 0.286 | 0.47 | 0.6217 | 0.47 | 0.7313 |  |
| textfooler | reviews | xlmr_base | B5 | 2024 | pool10x20 | wsd035 | 1500 | 0.756 | 0.5021 | 0.3113 | 0.4447 | 0.5882 | 0.4447 | 0.7313 |  |
| textfooler | reviews | xlmr_base | B5 | 2024 |  | wsd035 | 1500 | 0.7747 | 0.4956 | 0.4033 | 0.3713 | 0.4793 | 0.3713 | 0.7507 |  |
| textfooler | reviews | xlmr_base | B5 | 7 |  |  | 1500 | 0.7627 | 0.4993 | 0.3613 | 0.4013 | 0.5262 | 0.4013 | 0.7373 |  |
| textfooler | reviews | xlmr_base | B5 | 7 | pool10x20 |  | 1500 | 0.7627 | 0.5034 | 0.32 | 0.4427 | 0.5804 | 0.4427 | 0.7313 |  |
| textfooler | reviews | xlmr_base | B5 | 7 | pool10x20 | wsd035 | 1500 | 0.7627 | 0.5034 | 0.3347 | 0.428 | 0.5612 | 0.428 | 0.7313 |  |
| textfooler | reviews | xlmr_base | B5 | 7 |  | wsd035 | 1500 | 0.7627 | 0.4993 | 0.374 | 0.3887 | 0.5096 | 0.3887 | 0.7373 |  |
| textfooler | reviews | xlmr_base | B6 | 1914 |  |  | 1500 | 0.7653 | 0.5006 | 0.452 | 0.3133 | 0.4094 | 0.3133 | 0.7353 |  |
| textfooler | reviews | xlmr_base | B6 | 1914 |  | wsd035 | 1500 | 0.7653 | 0.5006 | 0.476 | 0.2893 | 0.378 | 0.2893 | 0.7353 |  |
| textfooler | reviews | xlmr_base | B6 | 2024 |  |  | 1500 | 0.7687 | 0.5015 | 0.446 | 0.3227 | 0.4198 | 0.3227 | 0.7633 |  |
| textfooler | reviews | xlmr_base | B6 | 2024 |  | wsd035 | 1500 | 0.7687 | 0.5015 | 0.462 | 0.3067 | 0.399 | 0.3067 | 0.7633 |  |
| textfooler | reviews | xlmr_base | B6 | 7 |  |  | 1500 | 0.7653 | 0.4902 | 0.4387 | 0.3267 | 0.4268 | 0.3267 | 0.7393 |  |
| textfooler | reviews | xlmr_base | B6 | 7 |  | wsd035 | 1500 | 0.7653 | 0.4902 | 0.4613 | 0.304 | 0.3972 | 0.304 | 0.7393 |  |
| textfooler | reviews | xlmr_base | B7 | 1914 |  |  | 1500 | 0.7613 | 0.4863 | 0.456 | 0.3053 | 0.4011 | 0.3053 | 0.752 |  |
| textfooler | reviews | xlmr_base | B7 | 1914 |  | wsd035 | 1500 | 0.7613 | 0.4863 | 0.488 | 0.2733 | 0.359 | 0.2733 | 0.752 |  |
| textfooler | reviews | xlmr_base | B7 | 2024 |  |  | 1500 | 0.762 | 0.5029 | 0.4413 | 0.3207 | 0.4208 | 0.3207 | 0.7527 |  |
| textfooler | reviews | xlmr_base | B7 | 2024 |  | wsd035 | 1500 | 0.762 | 0.5029 | 0.47 | 0.292 | 0.3832 | 0.292 | 0.7527 |  |
| textfooler | reviews | xlmr_base | B7 | 7 |  |  | 1500 | 0.762 | 0.4916 | 0.496 | 0.266 | 0.3491 | 0.266 | 0.7747 |  |
| textfooler | reviews | xlmr_base | B7 | 7 |  | wsd035 | 1500 | 0.762 | 0.4916 | 0.516 | 0.246 | 0.3228 | 0.246 | 0.7747 |  |
| textfooler | unlp | xlmr_base | B0 | 1914 |  |  | 382 | 0.7906 | 0.7737 | 0.5262 | 0.2644 | 0.3344 | 0.2644 | 0.5812 |  |
| textfooler | unlp | xlmr_base | B0 | 1914 |  | wsd035 | 382 | 0.7906 | 0.7737 | 0.5419 | 0.2487 | 0.3146 | 0.2487 | 0.5812 |  |
| textfooler | unlp | xlmr_base | B0 | 2024 |  |  | 382 | 0.8534 | 0.7734 | 0.5681 | 0.2853 | 0.3344 | 0.2853 | 0.6126 |  |
| textfooler | unlp | xlmr_base | B0 | 2024 |  | wsd035 | 382 | 0.8534 | 0.7734 | 0.5681 | 0.2853 | 0.3344 | 0.2853 | 0.6126 |  |
| textfooler | unlp | xlmr_base | B0 | 7 |  |  | 382 | 0.8298 | 0.7871 | 0.555 | 0.2749 | 0.3312 | 0.2749 | 0.6152 |  |
| textfooler | unlp | xlmr_base | B0 | 7 |  | wsd035 | 382 | 0.8298 | 0.7871 | 0.5733 | 0.2565 | 0.3091 | 0.2565 | 0.6152 |  |
| textfooler | unlp | xlmr_base | B2 | 1914 |  |  | 382 | 0.7906 | 0.7934 | 0.5366 | 0.2539 | 0.3212 | 0.2539 | 0.5393 |  |
| textfooler | unlp | xlmr_base | B2 | 1914 |  | wsd035 | 382 | 0.7906 | 0.7934 | 0.5524 | 0.2382 | 0.3013 | 0.2382 | 0.5393 |  |
| textfooler | unlp | xlmr_base | B2 | 2024 |  |  | 382 | 0.8246 | 0.7775 | 0.6178 | 0.2068 | 0.2508 | 0.2068 | 0.6204 |  |
| textfooler | unlp | xlmr_base | B2 | 2024 |  | wsd035 | 382 | 0.8246 | 0.7775 | 0.6283 | 0.1963 | 0.2381 | 0.1963 | 0.6204 |  |
| textfooler | unlp | xlmr_base | B2 | 7 |  |  | 382 | 0.8037 | 0.766 | 0.5602 | 0.2435 | 0.3029 | 0.2435 | 0.5419 | DEGENERACY_SUSPECT(-0.021) |
| textfooler | unlp | xlmr_base | B2 | 7 |  | wsd035 | 382 | 0.8037 | 0.766 | 0.5838 | 0.2199 | 0.2736 | 0.2199 | 0.5419 | DEGENERACY_SUSPECT(-0.021) |
| textfooler | unlp | xlmr_base | B3 | 1914 |  |  | 382 | 0.8403 | 0.8082 | 0.5314 | 0.3089 | 0.3676 | 0.3089 | 0.5942 |  |
| textfooler | unlp | xlmr_base | B3 | 1914 |  | wsd035 | 382 | 0.8403 | 0.8082 | 0.5497 | 0.2906 | 0.3458 | 0.2906 | 0.5942 |  |
| textfooler | unlp | xlmr_base | B3 | 2024 |  |  | 382 | 0.7356 | 0.7376 | 0.5419 | 0.1937 | 0.2633 | 0.1937 | 0.589 | DEGENERACY_SUSPECT(-0.036) |
| textfooler | unlp | xlmr_base | B3 | 2024 |  | wsd035 | 382 | 0.7356 | 0.7376 | 0.5497 | 0.1859 | 0.2527 | 0.1859 | 0.589 | DEGENERACY_SUSPECT(-0.036) |
| textfooler | unlp | xlmr_base | B3 | 7 |  |  | 382 | 0.8403 | 0.7913 | 0.5419 | 0.2984 | 0.3551 | 0.2984 | 0.6047 |  |
| textfooler | unlp | xlmr_base | B3 | 7 |  | wsd035 | 382 | 0.8403 | 0.7913 | 0.5576 | 0.2827 | 0.3364 | 0.2827 | 0.6047 |  |
| textfooler | unlp | xlmr_base | B4 | 1914 |  |  | 382 | 0.822 | 0.7956 | 0.5497 | 0.2723 | 0.3312 | 0.2723 | 0.5916 |  |
| textfooler | unlp | xlmr_base | B4 | 1914 |  | wsd035 | 382 | 0.822 | 0.7956 | 0.5733 | 0.2487 | 0.3025 | 0.2487 | 0.5916 |  |
| textfooler | unlp | xlmr_base | B4 | 2024 |  |  | 382 | 0.8089 | 0.7741 | 0.5 | 0.3089 | 0.3819 | 0.3089 | 0.5157 |  |
| textfooler | unlp | xlmr_base | B4 | 2024 |  | wsd035 | 382 | 0.8089 | 0.7741 | 0.5131 | 0.2958 | 0.3657 | 0.2958 | 0.5157 |  |
| textfooler | unlp | xlmr_base | B4 | 7 |  |  | 382 | 0.8194 | 0.7623 | 0.5812 | 0.2382 | 0.2907 | 0.2382 | 0.6361 | DEGENERACY_SUSPECT(-0.025) |
| textfooler | unlp | xlmr_base | B4 | 7 |  | wsd035 | 382 | 0.8194 | 0.7623 | 0.5864 | 0.233 | 0.2843 | 0.233 | 0.6361 | DEGENERACY_SUSPECT(-0.025) |
| bert_attack | news | xlmr_base | B0 | 1914 |  |  | 1500 | 0.918 | 0.8974 | 0.718 | 0.2 | 0.2179 | 0.2 | 0.3453 |  |
| bert_attack | news | xlmr_base | B2 | 1914 |  |  | 1500 | 0.924 | 0.8998 | 0.722 | 0.202 | 0.2186 | 0.202 | 0.3367 |  |
| bert_attack | news | xlmr_base | B3 | 1914 |  |  | 1500 | 0.9173 | 0.8992 | 0.732 | 0.1853 | 0.202 | 0.1853 | 0.3407 |  |
| bert_attack | news | xlmr_base | B4 | 1914 |  |  | 1500 | 0.9213 | 0.8994 | 0.7327 | 0.1887 | 0.2048 | 0.1887 | 0.3427 |  |
| bert_attack | reviews | ukr_roberta | B0 | 1914 |  |  | 1500 | 0.7407 | 0.451 | 0.6007 | 0.14 | 0.189 | 0.14 | 0.764 |  |
| bert_attack | reviews | ukr_roberta | B0 | 2024 |  |  | 1500 | 0.738 | 0.4589 | 0.5947 | 0.1433 | 0.1942 | 0.1433 | 0.7647 |  |
| bert_attack | reviews | ukr_roberta | B0 | 7 |  |  | 1500 | 0.7273 | 0.4526 | 0.578 | 0.1493 | 0.2053 | 0.1493 | 0.756 |  |
| bert_attack | reviews | ukr_roberta | B2 | 1914 |  |  | 1500 | 0.7173 | 0.4549 | 0.5447 | 0.1727 | 0.2407 | 0.1727 | 0.7353 |  |
| bert_attack | reviews | ukr_roberta | B2 | 2024 |  |  | 1500 | 0.7373 | 0.4439 | 0.624 | 0.1133 | 0.1537 | 0.1133 | 0.7847 |  |
| bert_attack | reviews | ukr_roberta | B2 | 7 |  |  | 1500 | 0.7153 | 0.4516 | 0.5047 | 0.2107 | 0.2945 | 0.2107 | 0.7227 |  |
| bert_attack | reviews | ukr_roberta | B3 | 1914 |  |  | 1500 | 0.7247 | 0.452 | 0.5787 | 0.146 | 0.2015 | 0.146 | 0.7487 |  |
| bert_attack | reviews | ukr_roberta | B3 | 2024 |  |  | 1500 | 0.712 | 0.4522 | 0.5693 | 0.1427 | 0.2004 | 0.1427 | 0.7327 |  |
| bert_attack | reviews | ukr_roberta | B3 | 7 |  |  | 1500 | 0.7367 | 0.4577 | 0.5953 | 0.1413 | 0.1919 | 0.1413 | 0.752 |  |
| bert_attack | reviews | ukr_roberta | B4 | 1914 |  |  | 1500 | 0.726 | 0.4503 | 0.576 | 0.15 | 0.2066 | 0.15 | 0.7453 |  |
| bert_attack | reviews | ukr_roberta | B4 | 2024 |  |  | 1500 | 0.7267 | 0.4513 | 0.574 | 0.1527 | 0.2101 | 0.1527 | 0.744 |  |
| bert_attack | reviews | ukr_roberta | B4 | 7 |  |  | 1500 | 0.7193 | 0.455 | 0.5533 | 0.166 | 0.2308 | 0.166 | 0.7593 |  |
| bert_attack | reviews | ukr_roberta | B5 | 1914 |  |  | 1500 | 0.7267 | 0.4499 | 0.5353 | 0.1913 | 0.2633 | 0.1913 | 0.7453 |  |
| bert_attack | reviews | ukr_roberta | B5 | 2024 |  |  | 1500 | 0.726 | 0.4421 | 0.5673 | 0.1587 | 0.2185 | 0.1587 | 0.7547 |  |
| bert_attack | reviews | ukr_roberta | B5 | 7 |  |  | 1500 | 0.736 | 0.4443 | 0.5533 | 0.1827 | 0.2482 | 0.1827 | 0.7593 |  |
| bert_attack | reviews | xlmr_base | B0 | 1914 |  |  | 1500 | 0.768 | 0.484 | 0.6587 | 0.1093 | 0.1424 | 0.1093 | 0.7533 |  |
| bert_attack | reviews | xlmr_base | B0 | 1914 | full78k |  | 1500 | 0.7507 | 0.5228 | 0.6287 | 0.122 | 0.1625 | 0.122 | 0.7113 |  |
| bert_attack | reviews | xlmr_base | B0 | 2024 |  |  | 1500 | 0.7627 | 0.4921 | 0.6473 | 0.1153 | 0.1512 | 0.1153 | 0.746 |  |
| bert_attack | reviews | xlmr_base | B0 | 2024 | full78k |  | 1500 | 0.7653 | 0.5 | 0.6553 | 0.11 | 0.1437 | 0.11 | 0.7467 |  |
| bert_attack | reviews | xlmr_base | B0 | 7 |  |  | 1500 | 0.77 | 0.4929 | 0.6727 | 0.0973 | 0.1264 | 0.0973 | 0.7687 |  |
| bert_attack | reviews | xlmr_base | B0 | 7 | full78k |  | 1500 | 0.7693 | 0.4964 | 0.6547 | 0.1147 | 0.149 | 0.1147 | 0.756 |  |
| bert_attack | reviews | xlmr_base | B1 | 1914 |  |  | 1500 | 0.748 | 0.499 | 0.5987 | 0.1493 | 0.1996 | 0.1493 | 0.706 |  |
| bert_attack | reviews | xlmr_base | B1 | 2024 |  |  | 1500 | 0.77 | 0.5011 | 0.6467 | 0.1233 | 0.1602 | 0.1233 | 0.7533 |  |
| bert_attack | reviews | xlmr_base | B1 | 7 |  |  | 1500 | 0.7653 | 0.497 | 0.6473 | 0.118 | 0.1542 | 0.118 | 0.748 |  |
| bert_attack | reviews | xlmr_base | B2 | 1914 |  |  | 1500 | 0.7607 | 0.499 | 0.6307 | 0.13 | 0.1709 | 0.13 | 0.7387 |  |
| bert_attack | reviews | xlmr_base | B2 | 1914 | full78k |  | 1500 | 0.768 | 0.5027 | 0.6587 | 0.1093 | 0.1424 | 0.1093 | 0.7327 | DEGENERACY_SUSPECT(-0.020) |
| bert_attack | reviews | xlmr_base | B2 | 1914 | r0.25 |  | 1500 | 0.7647 | 0.4783 | 0.638 | 0.1267 | 0.1656 | 0.1267 | 0.7487 |  |
| bert_attack | reviews | xlmr_base | B2 | 1914 | r1.0 |  | 1500 | 0.744 | 0.5045 | 0.6173 | 0.1267 | 0.1703 | 0.1267 | 0.7313 |  |
| bert_attack | reviews | xlmr_base | B2 | 2024 |  |  | 1500 | 0.7753 | 0.4966 | 0.6513 | 0.124 | 0.1599 | 0.124 | 0.754 |  |
| bert_attack | reviews | xlmr_base | B2 | 2024 | full78k |  | 1500 | 0.7653 | 0.4706 | 0.69 | 0.0753 | 0.0984 | 0.0753 | 0.7993 | DEGENERACY_SUSPECT(-0.029) |
| bert_attack | reviews | xlmr_base | B2 | 2024 | r1.0 |  | 1500 | 0.7727 | 0.5104 | 0.6447 | 0.128 | 0.1657 | 0.128 | 0.752 |  |
| bert_attack | reviews | xlmr_base | B2 | 7 |  |  | 1500 | 0.772 | 0.5026 | 0.6427 | 0.1293 | 0.1675 | 0.1293 | 0.7413 |  |
| bert_attack | reviews | xlmr_base | B2 | 7 | full78k |  | 1500 | 0.7627 | 0.5135 | 0.6413 | 0.1213 | 0.1591 | 0.1213 | 0.7333 |  |
| bert_attack | reviews | xlmr_base | B2 | 7 | r1.0 |  | 1500 | 0.7613 | 0.4955 | 0.646 | 0.1153 | 0.1515 | 0.1153 | 0.752 |  |
| bert_attack | reviews | xlmr_base | B3 | 1914 |  |  | 1500 | 0.762 | 0.503 | 0.6307 | 0.1313 | 0.1724 | 0.1313 | 0.7167 |  |
| bert_attack | reviews | xlmr_base | B3 | 1914 | full78k |  | 1500 | 0.7747 | 0.4656 | 0.6993 | 0.0753 | 0.0972 | 0.0753 | 0.7873 | DEGENERACY_SUSPECT(-0.057) |
| bert_attack | reviews | xlmr_base | B3 | 1914 | pool10x20 |  | 1500 | 0.748 | 0.4989 | 0.6293 | 0.1187 | 0.1586 | 0.1187 | 0.7167 |  |
| bert_attack | reviews | xlmr_base | B3 | 1914 | r0.25 |  | 1500 | 0.7653 | 0.4833 | 0.67 | 0.0953 | 0.1246 | 0.0953 | 0.7547 |  |
| bert_attack | reviews | xlmr_base | B3 | 1914 | r1.0 |  | 1500 | 0.7727 | 0.4864 | 0.676 | 0.0967 | 0.1251 | 0.0967 | 0.772 |  |
| bert_attack | reviews | xlmr_base | B3 | 2024 |  |  | 1500 | 0.772 | 0.4935 | 0.6507 | 0.1213 | 0.1572 | 0.1213 | 0.752 |  |
| bert_attack | reviews | xlmr_base | B3 | 2024 | full78k |  | 1500 | 0.776 | 0.5039 | 0.6727 | 0.1033 | 0.1332 | 0.1033 | 0.7673 |  |
| bert_attack | reviews | xlmr_base | B3 | 2024 | pool10x20 |  | 1500 | 0.7647 | 0.4883 | 0.6407 | 0.124 | 0.1622 | 0.124 | 0.7627 |  |
| bert_attack | reviews | xlmr_base | B3 | 2024 | r1.0 |  | 1500 | 0.7733 | 0.5004 | 0.6513 | 0.122 | 0.1578 | 0.122 | 0.7647 |  |
| bert_attack | reviews | xlmr_base | B3 | 7 |  |  | 1500 | 0.7627 | 0.5017 | 0.6487 | 0.114 | 0.1495 | 0.114 | 0.7507 |  |
| bert_attack | reviews | xlmr_base | B3 | 7 | full78k |  | 1500 | 0.768 | 0.4663 | 0.678 | 0.09 | 0.1172 | 0.09 | 0.7567 | DEGENERACY_SUSPECT(-0.030) |
| bert_attack | reviews | xlmr_base | B3 | 7 | pool10x20 |  | 1500 | 0.7627 | 0.4862 | 0.6613 | 0.1013 | 0.1329 | 0.1013 | 0.7547 |  |
| bert_attack | reviews | xlmr_base | B3 | 7 | r1.0 |  | 1500 | 0.7607 | 0.5018 | 0.646 | 0.1147 | 0.1507 | 0.1147 | 0.748 |  |
| bert_attack | reviews | xlmr_base | B4 | 1914 |  |  | 1500 | 0.7613 | 0.494 | 0.6373 | 0.124 | 0.1629 | 0.124 | 0.724 |  |
| bert_attack | reviews | xlmr_base | B4 | 1914 | full78k |  | 1500 | 0.7673 | 0.4909 | 0.6747 | 0.0927 | 0.1208 | 0.0927 | 0.7673 | DEGENERACY_SUSPECT(-0.032) |
| bert_attack | reviews | xlmr_base | B4 | 1914 | pool10x20 |  | 1500 | 0.7493 | 0.4908 | 0.6407 | 0.1087 | 0.145 | 0.1087 | 0.7333 |  |
| bert_attack | reviews | xlmr_base | B4 | 1914 | r0.25 |  | 1500 | 0.7613 | 0.4868 | 0.638 | 0.1233 | 0.162 | 0.1233 | 0.7533 |  |
| bert_attack | reviews | xlmr_base | B4 | 1914 | r1.0 |  | 1500 | 0.75 | 0.5043 | 0.644 | 0.106 | 0.1413 | 0.106 | 0.7287 |  |
| bert_attack | reviews | xlmr_base | B4 | 2024 |  |  | 1500 | 0.778 | 0.4943 | 0.662 | 0.116 | 0.1491 | 0.116 | 0.7667 |  |
| bert_attack | reviews | xlmr_base | B4 | 2024 | full78k |  | 1500 | 0.76 | 0.4914 | 0.6647 | 0.0953 | 0.1254 | 0.0953 | 0.738 |  |
| bert_attack | reviews | xlmr_base | B4 | 2024 | pool10x20 |  | 1500 | 0.7627 | 0.4936 | 0.64 | 0.1227 | 0.1608 | 0.1227 | 0.7367 |  |
| bert_attack | reviews | xlmr_base | B4 | 2024 | r1.0 |  | 1500 | 0.7653 | 0.4953 | 0.6313 | 0.134 | 0.1751 | 0.134 | 0.7447 |  |
| bert_attack | reviews | xlmr_base | B4 | 7 |  |  | 1500 | 0.766 | 0.497 | 0.6487 | 0.1173 | 0.1532 | 0.1173 | 0.7593 |  |
| bert_attack | reviews | xlmr_base | B4 | 7 | full78k |  | 1500 | 0.7733 | 0.5058 | 0.67 | 0.1033 | 0.1336 | 0.1033 | 0.766 |  |
| bert_attack | reviews | xlmr_base | B4 | 7 | pool10x20 |  | 1500 | 0.7687 | 0.4909 | 0.6733 | 0.0953 | 0.124 | 0.0953 | 0.768 |  |
| bert_attack | reviews | xlmr_base | B4 | 7 | r1.0 |  | 1500 | 0.7647 | 0.4903 | 0.6693 | 0.0953 | 0.1247 | 0.0953 | 0.7787 |  |
| bert_attack | reviews | xlmr_base | B5 | 1914 |  |  | 1500 | 0.7487 | 0.5 | 0.5827 | 0.166 | 0.2217 | 0.166 | 0.7027 |  |
| bert_attack | reviews | xlmr_base | B5 | 1914 | pool10x20 |  | 1500 | 0.7547 | 0.5119 | 0.5793 | 0.1753 | 0.2323 | 0.1753 | 0.706 |  |
| bert_attack | reviews | xlmr_base | B5 | 2024 |  |  | 1500 | 0.7747 | 0.4956 | 0.6373 | 0.1373 | 0.1773 | 0.1373 | 0.7507 |  |
| bert_attack | reviews | xlmr_base | B5 | 2024 | pool10x20 |  | 1500 | 0.756 | 0.5021 | 0.622 | 0.134 | 0.1772 | 0.134 | 0.7313 |  |
| bert_attack | reviews | xlmr_base | B5 | 7 |  |  | 1500 | 0.7627 | 0.4993 | 0.6133 | 0.1493 | 0.1958 | 0.1493 | 0.7373 |  |
| bert_attack | reviews | xlmr_base | B5 | 7 | pool10x20 |  | 1500 | 0.7627 | 0.5034 | 0.6107 | 0.152 | 0.1993 | 0.152 | 0.7313 |  |
| bert_attack | reviews | xlmr_base | B6 | 1914 |  |  | 1500 | 0.7653 | 0.5006 | 0.64 | 0.1253 | 0.1638 | 0.1253 | 0.7353 |  |
| bert_attack | reviews | xlmr_base | B6 | 2024 |  |  | 1500 | 0.7687 | 0.5015 | 0.664 | 0.1047 | 0.1362 | 0.1047 | 0.7633 |  |
| bert_attack | reviews | xlmr_base | B6 | 7 |  |  | 1500 | 0.7653 | 0.4902 | 0.6453 | 0.12 | 0.1568 | 0.12 | 0.7393 |  |
| bert_attack | reviews | xlmr_base | B7 | 1914 |  |  | 1500 | 0.7613 | 0.4863 | 0.6593 | 0.102 | 0.134 | 0.102 | 0.752 |  |
| bert_attack | reviews | xlmr_base | B7 | 2024 |  |  | 1500 | 0.762 | 0.5029 | 0.6587 | 0.1033 | 0.1356 | 0.1033 | 0.7527 |  |
| bert_attack | reviews | xlmr_base | B7 | 7 |  |  | 1500 | 0.762 | 0.4916 | 0.6773 | 0.0847 | 0.1111 | 0.0847 | 0.7747 |  |
| bert_attack | unlp | xlmr_base | B0 | 1914 |  |  | 382 | 0.7906 | 0.7737 | 0.6885 | 0.1021 | 0.1291 | 0.1021 | 0.5812 |  |
| bert_attack | unlp | xlmr_base | B0 | 2024 |  |  | 382 | 0.8534 | 0.7734 | 0.712 | 0.1414 | 0.1656 | 0.1414 | 0.6126 |  |
| bert_attack | unlp | xlmr_base | B0 | 7 |  |  | 382 | 0.8298 | 0.7871 | 0.7068 | 0.123 | 0.1483 | 0.123 | 0.6152 |  |
| bert_attack | unlp | xlmr_base | B2 | 1914 |  |  | 382 | 0.7906 | 0.7934 | 0.7042 | 0.0864 | 0.1093 | 0.0864 | 0.5393 |  |
| bert_attack | unlp | xlmr_base | B2 | 2024 |  |  | 382 | 0.8246 | 0.7775 | 0.7277 | 0.0969 | 0.1175 | 0.0969 | 0.6204 |  |
| bert_attack | unlp | xlmr_base | B2 | 7 |  |  | 382 | 0.8037 | 0.766 | 0.7042 | 0.0995 | 0.1238 | 0.0995 | 0.5419 | DEGENERACY_SUSPECT(-0.021) |
| bert_attack | unlp | xlmr_base | B3 | 1914 |  |  | 382 | 0.8403 | 0.8082 | 0.7251 | 0.1152 | 0.1371 | 0.1152 | 0.5942 |  |
| bert_attack | unlp | xlmr_base | B3 | 2024 |  |  | 382 | 0.7356 | 0.7376 | 0.6492 | 0.0864 | 0.1174 | 0.0864 | 0.589 | DEGENERACY_SUSPECT(-0.036) |
| bert_attack | unlp | xlmr_base | B3 | 7 |  |  | 382 | 0.8403 | 0.7913 | 0.7042 | 0.1361 | 0.162 | 0.1361 | 0.6047 |  |
| bert_attack | unlp | xlmr_base | B4 | 1914 |  |  | 382 | 0.822 | 0.7956 | 0.7173 | 0.1047 | 0.1274 | 0.1047 | 0.5916 |  |
| bert_attack | unlp | xlmr_base | B4 | 2024 |  |  | 382 | 0.8089 | 0.7741 | 0.7199 | 0.089 | 0.11 | 0.089 | 0.5157 |  |
| bert_attack | unlp | xlmr_base | B4 | 7 |  |  | 382 | 0.8194 | 0.7623 | 0.7277 | 0.0916 | 0.1118 | 0.0916 | 0.6361 | DEGENERACY_SUSPECT(-0.025) |

## Paired condition comparisons (McNemar exact), per seed

Restricted to examples BOTH models classify correctly when clean. `casr_delta` < 0 means `condition` is MORE robust than `reference`; `p_value` is a two-sided exact test on the discordant pairs. These capture EVALUATION sampling noise only -- not training-run variance, which is what the across-seed table below is for.

| attack | dataset | model | wsd | seed | variant | reference | condition | n_paired | reference_casr_paired | condition_casr_paired | casr_delta | b_worse | c_better | p_value |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bert_attack | news | xlmr_base |  | 1914 |  | B0 | B2 | 1352 | 0.2078 | 0.2034 | -0.0044 | 48 | 54 | 0.6208 |
| bert_attack | news | xlmr_base |  | 1914 |  | B0 | B3 | 1344 | 0.2016 | 0.1875 | -0.0141 | 54 | 73 | 0.1098 |
| bert_attack | news | xlmr_base |  | 1914 |  | B0 | B4 | 1351 | 0.2065 | 0.1917 | -0.0148 | 43 | 63 | 0.0645 |
| bert_attack | news | xlmr_base |  | 1914 |  | B2 | B3 | 1345 | 0.1985 | 0.1851 | -0.0134 | 38 | 56 | 0.079 |
| bert_attack | news | xlmr_base |  | 1914 |  | B2 | B4 | 1356 | 0.2058 | 0.1932 | -0.0125 | 40 | 57 | 0.1038 |
| bert_attack | news | xlmr_base |  | 1914 |  | B3 | B4 | 1349 | 0.1875 | 0.1875 | 0.0 | 47 | 47 | 1.0 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B0 | B2 | 1031 | 0.1465 | 0.2173 | 0.0708 | 90 | 17 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B0 | B3 | 1037 | 0.1485 | 0.1774 | 0.0289 | 68 | 38 | 0.0046 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B0 | B4 | 1040 | 0.1519 | 0.1837 | 0.0317 | 66 | 33 | 0.0012 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B0 | B5 | 1045 | 0.1589 | 0.2421 | 0.0833 | 109 | 22 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B2 | B3 | 1039 | 0.2214 | 0.1761 | -0.0452 | 30 | 77 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B2 | B4 | 1045 | 0.2249 | 0.1799 | -0.045 | 18 | 65 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B2 | B5 | 1029 | 0.2216 | 0.2332 | 0.0117 | 54 | 42 | 0.2615 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B3 | B4 | 1057 | 0.1845 | 0.1902 | 0.0057 | 44 | 38 | 0.5811 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B3 | B5 | 1019 | 0.1688 | 0.2267 | 0.0579 | 95 | 36 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 1914 |  | B4 | B5 | 1024 | 0.1787 | 0.2305 | 0.0518 | 83 | 30 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B0 | B2 | 1062 | 0.1695 | 0.1375 | -0.032 | 36 | 70 | 0.0012 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B0 | B3 | 1030 | 0.1612 | 0.1835 | 0.0223 | 62 | 39 | 0.0281 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B0 | B4 | 1051 | 0.1694 | 0.1912 | 0.0219 | 61 | 38 | 0.0265 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B0 | B5 | 1053 | 0.1747 | 0.1975 | 0.0228 | 56 | 32 | 0.0138 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B2 | B3 | 1028 | 0.1235 | 0.1848 | 0.0613 | 89 | 26 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B2 | B4 | 1037 | 0.1234 | 0.1861 | 0.0627 | 93 | 28 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B2 | B5 | 1048 | 0.1384 | 0.1966 | 0.0582 | 85 | 24 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B3 | B4 | 1037 | 0.1842 | 0.1823 | -0.0019 | 49 | 51 | 0.9204 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B3 | B5 | 1022 | 0.184 | 0.183 | -0.001 | 51 | 52 | 1.0 |
| bert_attack | reviews | ukr_roberta |  | 2024 |  | B4 | B5 | 1038 | 0.1898 | 0.1879 | -0.0019 | 46 | 48 | 0.9179 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B0 | B2 | 1034 | 0.1828 | 0.2776 | 0.0948 | 117 | 19 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B0 | B3 | 1042 | 0.1795 | 0.1622 | -0.0173 | 39 | 57 | 0.0822 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B0 | B4 | 1031 | 0.1765 | 0.2066 | 0.0301 | 63 | 32 | 0.0019 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B0 | B5 | 1048 | 0.1823 | 0.2156 | 0.0334 | 65 | 30 | 0.0004 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B2 | B3 | 1024 | 0.2705 | 0.1611 | -0.1094 | 21 | 133 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B2 | B4 | 1030 | 0.2786 | 0.2107 | -0.068 | 20 | 90 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B2 | B5 | 1042 | 0.2802 | 0.2159 | -0.0643 | 29 | 96 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B3 | B4 | 1040 | 0.1596 | 0.2048 | 0.0452 | 71 | 24 | 0.0 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B3 | B5 | 1039 | 0.1655 | 0.2089 | 0.0433 | 84 | 39 | 0.0001 |
| bert_attack | reviews | ukr_roberta |  | 7 |  | B4 | B5 | 1043 | 0.2157 | 0.2148 | -0.001 | 57 | 58 | 1.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B0 | B1 | 1077 | 0.1086 | 0.1792 | 0.0706 | 101 | 25 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B0 | B2 | 1087 | 0.1132 | 0.1371 | 0.0239 | 57 | 31 | 0.0073 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B0 | B3 | 1088 | 0.1158 | 0.1452 | 0.0294 | 70 | 38 | 0.0027 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B0 | B4 | 1096 | 0.1141 | 0.1414 | 0.0274 | 62 | 32 | 0.0026 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B0 | B5 | 1079 | 0.1075 | 0.2039 | 0.0964 | 120 | 16 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B0 | B6 | 1103 | 0.1188 | 0.1369 | 0.0181 | 54 | 34 | 0.0422 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B0 | B7 | 1097 | 0.1167 | 0.1085 | -0.0082 | 46 | 55 | 0.4262 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B1 | B2 | 1066 | 0.1811 | 0.1341 | -0.0469 | 33 | 83 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B1 | B3 | 1077 | 0.1829 | 0.1402 | -0.0427 | 29 | 75 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B1 | B4 | 1081 | 0.1804 | 0.1369 | -0.0435 | 29 | 76 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B1 | B5 | 1078 | 0.1763 | 0.1985 | 0.0223 | 65 | 41 | 0.025 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B1 | B6 | 1081 | 0.185 | 0.1323 | -0.0527 | 28 | 85 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B1 | B7 | 1063 | 0.175 | 0.1025 | -0.0724 | 27 | 104 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B2 | B3 | 1086 | 0.1473 | 0.1492 | 0.0018 | 52 | 50 | 0.9212 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B2 | B4 | 1083 | 0.1404 | 0.1376 | -0.0028 | 52 | 55 | 0.8468 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B2 | B5 | 1070 | 0.1383 | 0.2019 | 0.0636 | 97 | 29 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B2 | B6 | 1089 | 0.1423 | 0.135 | -0.0073 | 45 | 53 | 0.4797 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B2 | B7 | 1086 | 0.1418 | 0.1077 | -0.0341 | 29 | 66 | 0.0002 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B3 | B4 | 1093 | 0.1446 | 0.1391 | -0.0055 | 40 | 46 | 0.59 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B3 | B5 | 1079 | 0.1427 | 0.203 | 0.0602 | 88 | 23 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B3 | B6 | 1093 | 0.1519 | 0.1372 | -0.0146 | 37 | 53 | 0.1133 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B3 | B7 | 1087 | 0.149 | 0.1113 | -0.0377 | 37 | 78 | 0.0002 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B4 | B5 | 1076 | 0.1329 | 0.2017 | 0.0688 | 96 | 22 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B4 | B6 | 1099 | 0.151 | 0.1374 | -0.0136 | 39 | 54 | 0.1462 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B4 | B7 | 1082 | 0.1331 | 0.1072 | -0.0259 | 35 | 63 | 0.0061 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B5 | B6 | 1082 | 0.2079 | 0.1312 | -0.0767 | 22 | 105 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B5 | B7 | 1073 | 0.2088 | 0.1072 | -0.1016 | 18 | 127 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 |  | B6 | B7 | 1090 | 0.1321 | 0.1101 | -0.022 | 32 | 56 | 0.0138 |
| bert_attack | reviews | xlmr_base |  | 1914 | full78k | B0 | B2 | 1084 | 0.1476 | 0.1116 | -0.036 | 29 | 68 | 0.0001 |
| bert_attack | reviews | xlmr_base |  | 1914 | full78k | B0 | B3 | 1069 | 0.1413 | 0.0636 | -0.0776 | 17 | 100 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | full78k | B0 | B4 | 1070 | 0.143 | 0.0888 | -0.0542 | 26 | 84 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | full78k | B2 | B3 | 1099 | 0.1174 | 0.0764 | -0.0409 | 23 | 68 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | full78k | B2 | B4 | 1092 | 0.1163 | 0.098 | -0.0183 | 28 | 48 | 0.0286 |
| bert_attack | reviews | xlmr_base |  | 1914 | full78k | B3 | B4 | 1105 | 0.0706 | 0.0968 | 0.0262 | 46 | 17 | 0.0003 |
| bert_attack | reviews | xlmr_base |  | 1914 | pool10x20 | B0 | B3 | 1080 | 0.1148 | 0.1407 | 0.0259 | 62 | 34 | 0.0056 |
| bert_attack | reviews | xlmr_base |  | 1914 | pool10x20 | B0 | B4 | 1087 | 0.115 | 0.1306 | 0.0156 | 53 | 36 | 0.0893 |
| bert_attack | reviews | xlmr_base |  | 1914 | pool10x20 | B0 | B5 | 1086 | 0.1142 | 0.2118 | 0.0976 | 126 | 20 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | pool10x20 | B3 | B4 | 1083 | 0.1413 | 0.1265 | -0.0148 | 33 | 49 | 0.097 |
| bert_attack | reviews | xlmr_base |  | 1914 | pool10x20 | B3 | B5 | 1072 | 0.139 | 0.2052 | 0.0662 | 96 | 25 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | pool10x20 | B4 | B5 | 1073 | 0.1202 | 0.206 | 0.0857 | 110 | 18 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | r0.25 | B0 | B2 | 1110 | 0.1198 | 0.1468 | 0.027 | 58 | 28 | 0.0016 |
| bert_attack | reviews | xlmr_base |  | 1914 | r0.25 | B0 | B3 | 1104 | 0.1205 | 0.0996 | -0.0208 | 34 | 57 | 0.0206 |
| bert_attack | reviews | xlmr_base |  | 1914 | r0.25 | B0 | B4 | 1101 | 0.119 | 0.1371 | 0.0182 | 50 | 30 | 0.033 |
| bert_attack | reviews | xlmr_base |  | 1914 | r0.25 | B2 | B3 | 1105 | 0.1457 | 0.1023 | -0.0434 | 21 | 69 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | r0.25 | B2 | B4 | 1101 | 0.1453 | 0.1408 | -0.0045 | 35 | 40 | 0.6445 |
| bert_attack | reviews | xlmr_base |  | 1914 | r0.25 | B3 | B4 | 1105 | 0.1059 | 0.1439 | 0.038 | 67 | 25 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | r1.0 | B0 | B2 | 1084 | 0.1144 | 0.1531 | 0.0387 | 70 | 28 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | r1.0 | B0 | B3 | 1099 | 0.1174 | 0.0937 | -0.0237 | 24 | 50 | 0.0034 |
| bert_attack | reviews | xlmr_base |  | 1914 | r1.0 | B0 | B4 | 1082 | 0.1128 | 0.1201 | 0.0074 | 41 | 33 | 0.416 |
| bert_attack | reviews | xlmr_base |  | 1914 | r1.0 | B2 | B3 | 1069 | 0.1497 | 0.0926 | -0.0571 | 18 | 79 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 1914 | r1.0 | B2 | B4 | 1070 | 0.1486 | 0.1159 | -0.0327 | 27 | 62 | 0.0003 |
| bert_attack | reviews | xlmr_base |  | 1914 | r1.0 | B3 | B4 | 1076 | 0.0883 | 0.118 | 0.0297 | 58 | 26 | 0.0006 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B0 | B1 | 1098 | 0.1257 | 0.1284 | 0.0027 | 40 | 37 | 0.8199 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B0 | B2 | 1104 | 0.1286 | 0.1268 | -0.0018 | 35 | 37 | 0.9063 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B0 | B3 | 1103 | 0.1278 | 0.1306 | 0.0027 | 39 | 36 | 0.8176 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B0 | B4 | 1111 | 0.1332 | 0.1188 | -0.0144 | 26 | 42 | 0.0681 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B0 | B5 | 1103 | 0.1269 | 0.1442 | 0.0172 | 49 | 30 | 0.0422 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B0 | B6 | 1095 | 0.1196 | 0.1041 | -0.0155 | 27 | 44 | 0.0568 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B0 | B7 | 1088 | 0.1222 | 0.1112 | -0.011 | 23 | 35 | 0.148 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B1 | B2 | 1125 | 0.1431 | 0.1404 | -0.0027 | 32 | 35 | 0.8072 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B1 | B3 | 1111 | 0.1359 | 0.135 | -0.0009 | 32 | 33 | 1.0 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B1 | B4 | 1118 | 0.1395 | 0.1208 | -0.0188 | 26 | 47 | 0.0186 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B1 | B5 | 1119 | 0.1412 | 0.1519 | 0.0107 | 41 | 29 | 0.1882 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B1 | B6 | 1102 | 0.1289 | 0.1116 | -0.0172 | 28 | 47 | 0.037 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B1 | B7 | 1101 | 0.1326 | 0.1181 | -0.0145 | 28 | 44 | 0.0764 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B2 | B3 | 1116 | 0.1407 | 0.138 | -0.0027 | 33 | 36 | 0.8099 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B2 | B4 | 1127 | 0.1411 | 0.1295 | -0.0115 | 27 | 40 | 0.1421 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B2 | B5 | 1120 | 0.1384 | 0.1527 | 0.0143 | 45 | 29 | 0.0805 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B2 | B6 | 1110 | 0.1306 | 0.1117 | -0.0189 | 28 | 49 | 0.022 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B2 | B7 | 1115 | 0.139 | 0.1256 | -0.0135 | 26 | 41 | 0.0864 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B3 | B4 | 1117 | 0.1388 | 0.1262 | -0.0125 | 27 | 41 | 0.1143 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B3 | B5 | 1114 | 0.1382 | 0.1526 | 0.0144 | 45 | 29 | 0.0805 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B3 | B6 | 1104 | 0.1295 | 0.1141 | -0.0154 | 29 | 46 | 0.0639 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B3 | B7 | 1104 | 0.1322 | 0.1205 | -0.0118 | 30 | 43 | 0.1597 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B4 | B5 | 1122 | 0.1257 | 0.1595 | 0.0339 | 63 | 25 | 0.0001 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B4 | B6 | 1116 | 0.121 | 0.1192 | -0.0018 | 40 | 42 | 0.9122 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B4 | B7 | 1106 | 0.1184 | 0.1221 | 0.0036 | 34 | 30 | 0.708 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B5 | B6 | 1105 | 0.1448 | 0.1158 | -0.029 | 24 | 56 | 0.0005 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B5 | B7 | 1103 | 0.1451 | 0.1197 | -0.0254 | 22 | 50 | 0.0013 |
| bert_attack | reviews | xlmr_base |  | 2024 |  | B6 | B7 | 1094 | 0.1088 | 0.1124 | 0.0037 | 36 | 32 | 0.7163 |
| bert_attack | reviews | xlmr_base |  | 2024 | full78k | B0 | B2 | 1087 | 0.1095 | 0.0754 | -0.034 | 19 | 56 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 2024 | full78k | B0 | B3 | 1095 | 0.1187 | 0.0959 | -0.0228 | 28 | 53 | 0.0073 |
| bert_attack | reviews | xlmr_base |  | 2024 | full78k | B0 | B4 | 1099 | 0.1192 | 0.1065 | -0.0127 | 29 | 43 | 0.1249 |
| bert_attack | reviews | xlmr_base |  | 2024 | full78k | B2 | B3 | 1098 | 0.0774 | 0.0974 | 0.02 | 45 | 23 | 0.0103 |
| bert_attack | reviews | xlmr_base |  | 2024 | full78k | B2 | B4 | 1079 | 0.0686 | 0.0973 | 0.0287 | 55 | 24 | 0.0006 |
| bert_attack | reviews | xlmr_base |  | 2024 | full78k | B3 | B4 | 1101 | 0.0972 | 0.1072 | 0.01 | 43 | 32 | 0.248 |
| bert_attack | reviews | xlmr_base |  | 2024 | pool10x20 | B0 | B3 | 1094 | 0.1298 | 0.1344 | 0.0046 | 44 | 39 | 0.6609 |
| bert_attack | reviews | xlmr_base |  | 2024 | pool10x20 | B0 | B4 | 1088 | 0.1222 | 0.1333 | 0.011 | 47 | 35 | 0.2242 |
| bert_attack | reviews | xlmr_base |  | 2024 | pool10x20 | B0 | B5 | 1081 | 0.1147 | 0.1471 | 0.0324 | 60 | 25 | 0.0002 |
| bert_attack | reviews | xlmr_base |  | 2024 | pool10x20 | B3 | B4 | 1097 | 0.1358 | 0.1386 | 0.0027 | 41 | 38 | 0.8221 |
| bert_attack | reviews | xlmr_base |  | 2024 | pool10x20 | B3 | B5 | 1074 | 0.1285 | 0.1508 | 0.0223 | 65 | 41 | 0.025 |
| bert_attack | reviews | xlmr_base |  | 2024 | pool10x20 | B4 | B5 | 1073 | 0.1277 | 0.1473 | 0.0196 | 61 | 40 | 0.046 |
| bert_attack | reviews | xlmr_base |  | 2024 | r1.0 | B0 | B2 | 1102 | 0.1289 | 0.1343 | 0.0054 | 43 | 37 | 0.5764 |
| bert_attack | reviews | xlmr_base |  | 2024 | r1.0 | B0 | B3 | 1087 | 0.1224 | 0.1168 | -0.0055 | 43 | 49 | 0.6024 |
| bert_attack | reviews | xlmr_base |  | 2024 | r1.0 | B0 | B4 | 1086 | 0.1243 | 0.1427 | 0.0184 | 56 | 36 | 0.047 |
| bert_attack | reviews | xlmr_base |  | 2024 | r1.0 | B2 | B3 | 1096 | 0.1332 | 0.1214 | -0.0119 | 33 | 46 | 0.1766 |
| bert_attack | reviews | xlmr_base |  | 2024 | r1.0 | B2 | B4 | 1101 | 0.1353 | 0.149 | 0.0136 | 56 | 41 | 0.1548 |
| bert_attack | reviews | xlmr_base |  | 2024 | r1.0 | B3 | B4 | 1099 | 0.1247 | 0.1501 | 0.0255 | 57 | 29 | 0.0034 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B0 | B1 | 1098 | 0.0993 | 0.1257 | 0.0264 | 56 | 27 | 0.0019 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B0 | B2 | 1097 | 0.0994 | 0.1349 | 0.0356 | 62 | 23 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B0 | B3 | 1093 | 0.097 | 0.1217 | 0.0247 | 54 | 27 | 0.0036 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B0 | B4 | 1097 | 0.0985 | 0.1285 | 0.0301 | 62 | 29 | 0.0007 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B0 | B5 | 1091 | 0.099 | 0.165 | 0.066 | 91 | 19 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B0 | B6 | 1096 | 0.0995 | 0.1286 | 0.0292 | 58 | 26 | 0.0006 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B0 | B7 | 1101 | 0.1026 | 0.0872 | -0.0154 | 33 | 50 | 0.0784 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B1 | B2 | 1112 | 0.1331 | 0.1484 | 0.0153 | 43 | 26 | 0.0533 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B1 | B3 | 1105 | 0.1321 | 0.1312 | -0.0009 | 33 | 34 | 1.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B1 | B4 | 1105 | 0.1303 | 0.1357 | 0.0054 | 41 | 35 | 0.5666 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B1 | B5 | 1101 | 0.1326 | 0.1708 | 0.0381 | 72 | 30 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B1 | B6 | 1105 | 0.1276 | 0.1357 | 0.0081 | 41 | 32 | 0.3492 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B1 | B7 | 1097 | 0.1276 | 0.0912 | -0.0365 | 25 | 65 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B2 | B3 | 1104 | 0.144 | 0.1286 | -0.0154 | 35 | 52 | 0.0857 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B2 | B4 | 1112 | 0.1457 | 0.134 | -0.0117 | 33 | 46 | 0.1766 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B2 | B5 | 1101 | 0.1444 | 0.1708 | 0.0263 | 58 | 29 | 0.0025 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B2 | B6 | 1101 | 0.1399 | 0.129 | -0.0109 | 35 | 47 | 0.2242 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B2 | B7 | 1096 | 0.1396 | 0.0894 | -0.0502 | 21 | 76 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B3 | B4 | 1104 | 0.1259 | 0.1322 | 0.0063 | 38 | 31 | 0.4704 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B3 | B5 | 1096 | 0.1277 | 0.1688 | 0.0411 | 69 | 24 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B3 | B6 | 1099 | 0.1265 | 0.131 | 0.0045 | 42 | 37 | 0.653 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B3 | B7 | 1089 | 0.1221 | 0.0882 | -0.034 | 23 | 60 | 0.0001 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B4 | B5 | 1099 | 0.1319 | 0.1692 | 0.0373 | 71 | 30 | 0.0001 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B4 | B6 | 1101 | 0.1308 | 0.1317 | 0.0009 | 39 | 38 | 1.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B4 | B7 | 1100 | 0.1291 | 0.0891 | -0.04 | 22 | 66 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B5 | B6 | 1097 | 0.1668 | 0.1349 | -0.0319 | 32 | 67 | 0.0006 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B5 | B7 | 1092 | 0.1731 | 0.0934 | -0.0797 | 15 | 102 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 |  | B6 | B7 | 1090 | 0.1321 | 0.089 | -0.0431 | 19 | 66 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 | full78k | B0 | B2 | 1090 | 0.1165 | 0.1367 | 0.0202 | 52 | 30 | 0.0198 |
| bert_attack | reviews | xlmr_base |  | 7 | full78k | B0 | B3 | 1084 | 0.1089 | 0.0923 | -0.0166 | 33 | 51 | 0.063 |
| bert_attack | reviews | xlmr_base |  | 7 | full78k | B0 | B4 | 1103 | 0.1206 | 0.107 | -0.0136 | 32 | 47 | 0.1147 |
| bert_attack | reviews | xlmr_base |  | 7 | full78k | B2 | B3 | 1092 | 0.1346 | 0.0971 | -0.0375 | 31 | 72 | 0.0001 |
| bert_attack | reviews | xlmr_base |  | 7 | full78k | B2 | B4 | 1103 | 0.1423 | 0.107 | -0.0354 | 25 | 64 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 | full78k | B3 | B4 | 1093 | 0.0933 | 0.0952 | 0.0018 | 42 | 40 | 0.9122 |
| bert_attack | reviews | xlmr_base |  | 7 | pool10x20 | B0 | B3 | 1094 | 0.1033 | 0.1115 | 0.0082 | 48 | 39 | 0.3912 |
| bert_attack | reviews | xlmr_base |  | 7 | pool10x20 | B0 | B4 | 1102 | 0.0971 | 0.0989 | 0.0018 | 36 | 34 | 0.905 |
| bert_attack | reviews | xlmr_base |  | 7 | pool10x20 | B0 | B5 | 1088 | 0.0965 | 0.1691 | 0.0726 | 93 | 14 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 | pool10x20 | B3 | B4 | 1092 | 0.1044 | 0.1016 | -0.0027 | 38 | 41 | 0.8221 |
| bert_attack | reviews | xlmr_base |  | 7 | pool10x20 | B3 | B5 | 1074 | 0.1052 | 0.1713 | 0.0661 | 91 | 20 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 | pool10x20 | B4 | B5 | 1081 | 0.0944 | 0.1674 | 0.0731 | 93 | 14 | 0.0 |
| bert_attack | reviews | xlmr_base |  | 7 | r1.0 | B0 | B2 | 1095 | 0.0959 | 0.126 | 0.0301 | 59 | 26 | 0.0004 |
| bert_attack | reviews | xlmr_base |  | 7 | r1.0 | B0 | B3 | 1080 | 0.0954 | 0.1194 | 0.0241 | 54 | 28 | 0.0054 |
| bert_attack | reviews | xlmr_base |  | 7 | r1.0 | B0 | B4 | 1098 | 0.1011 | 0.0974 | -0.0036 | 33 | 37 | 0.7202 |
| bert_attack | reviews | xlmr_base |  | 7 | r1.0 | B2 | B3 | 1082 | 0.1266 | 0.1192 | -0.0074 | 33 | 41 | 0.416 |
| bert_attack | reviews | xlmr_base |  | 7 | r1.0 | B2 | B4 | 1088 | 0.1268 | 0.0983 | -0.0285 | 32 | 63 | 0.0019 |
| bert_attack | reviews | xlmr_base |  | 7 | r1.0 | B3 | B4 | 1087 | 0.1242 | 0.0994 | -0.0248 | 25 | 52 | 0.0028 |
| bert_attack | unlp | xlmr_base |  | 1914 |  | B0 | B2 | 287 | 0.1045 | 0.0836 | -0.0209 | 8 | 14 | 0.2863 |
| bert_attack | unlp | xlmr_base |  | 1914 |  | B0 | B3 | 288 | 0.1181 | 0.0972 | -0.0208 | 7 | 13 | 0.2632 |
| bert_attack | unlp | xlmr_base |  | 1914 |  | B0 | B4 | 296 | 0.1182 | 0.098 | -0.0203 | 8 | 14 | 0.2863 |
| bert_attack | unlp | xlmr_base |  | 1914 |  | B2 | B3 | 291 | 0.1031 | 0.1031 | 0.0 | 12 | 12 | 1.0 |
| bert_attack | unlp | xlmr_base |  | 1914 |  | B2 | B4 | 296 | 0.1014 | 0.098 | -0.0034 | 7 | 8 | 1.0 |
| bert_attack | unlp | xlmr_base |  | 1914 |  | B3 | B4 | 300 | 0.1133 | 0.12 | 0.0067 | 12 | 10 | 0.8318 |
| bert_attack | unlp | xlmr_base |  | 2024 |  | B0 | B2 | 309 | 0.1456 | 0.11 | -0.0356 | 10 | 21 | 0.0708 |
| bert_attack | unlp | xlmr_base |  | 2024 |  | B0 | B3 | 265 | 0.1132 | 0.1057 | -0.0075 | 22 | 24 | 0.883 |
| bert_attack | unlp | xlmr_base |  | 2024 |  | B0 | B4 | 295 | 0.1254 | 0.0949 | -0.0305 | 9 | 18 | 0.1221 |
| bert_attack | unlp | xlmr_base |  | 2024 |  | B2 | B3 | 258 | 0.0543 | 0.1047 | 0.0504 | 23 | 10 | 0.0351 |
| bert_attack | unlp | xlmr_base |  | 2024 |  | B2 | B4 | 285 | 0.0807 | 0.0772 | -0.0035 | 12 | 13 | 1.0 |
| bert_attack | unlp | xlmr_base |  | 2024 |  | B3 | B4 | 270 | 0.1 | 0.0889 | -0.0111 | 14 | 17 | 0.7201 |
| bert_attack | unlp | xlmr_base |  | 7 |  | B0 | B2 | 292 | 0.1164 | 0.1027 | -0.0137 | 8 | 12 | 0.5034 |
| bert_attack | unlp | xlmr_base |  | 7 |  | B0 | B3 | 303 | 0.1254 | 0.1353 | 0.0099 | 12 | 9 | 0.6636 |
| bert_attack | unlp | xlmr_base |  | 7 |  | B0 | B4 | 301 | 0.1229 | 0.0963 | -0.0266 | 8 | 16 | 0.1516 |
| bert_attack | unlp | xlmr_base |  | 7 |  | B2 | B3 | 299 | 0.1137 | 0.1338 | 0.0201 | 17 | 11 | 0.3449 |
| bert_attack | unlp | xlmr_base |  | 7 |  | B2 | B4 | 289 | 0.1038 | 0.09 | -0.0138 | 13 | 17 | 0.5847 |
| bert_attack | unlp | xlmr_base |  | 7 |  | B3 | B4 | 302 | 0.1325 | 0.096 | -0.0364 | 7 | 18 | 0.0433 |
| textfooler | news | xlmr_base | wsd035 | 1914 |  | B0 | B2 | 1352 | 0.0969 | 0.0902 | -0.0067 | 36 | 45 | 0.3742 |
| textfooler | news | xlmr_base | wsd035 | 1914 |  | B0 | B3 | 1344 | 0.0938 | 0.0699 | -0.0238 | 32 | 64 | 0.0014 |
| textfooler | news | xlmr_base | wsd035 | 1914 |  | B0 | B4 | 1351 | 0.094 | 0.0785 | -0.0155 | 30 | 51 | 0.0257 |
| textfooler | news | xlmr_base | wsd035 | 1914 |  | B2 | B3 | 1345 | 0.0862 | 0.0691 | -0.0171 | 27 | 50 | 0.0117 |
| textfooler | news | xlmr_base | wsd035 | 1914 |  | B2 | B4 | 1356 | 0.0922 | 0.0811 | -0.0111 | 23 | 38 | 0.0722 |
| textfooler | news | xlmr_base | wsd035 | 1914 |  | B3 | B4 | 1349 | 0.0704 | 0.0778 | 0.0074 | 43 | 33 | 0.3019 |
| textfooler | news | xlmr_base |  | 1914 |  | B0 | B2 | 1352 | 0.1087 | 0.0999 | -0.0089 | 34 | 46 | 0.2185 |
| textfooler | news | xlmr_base |  | 1914 |  | B0 | B3 | 1344 | 0.1057 | 0.0729 | -0.0327 | 27 | 71 | 0.0 |
| textfooler | news | xlmr_base |  | 1914 |  | B0 | B4 | 1351 | 0.1058 | 0.0888 | -0.017 | 31 | 54 | 0.0165 |
| textfooler | news | xlmr_base |  | 1914 |  | B2 | B3 | 1345 | 0.0959 | 0.0714 | -0.0245 | 23 | 56 | 0.0003 |
| textfooler | news | xlmr_base |  | 1914 |  | B2 | B4 | 1356 | 0.1018 | 0.0914 | -0.0103 | 25 | 39 | 0.1034 |
| textfooler | news | xlmr_base |  | 1914 |  | B3 | B4 | 1349 | 0.0734 | 0.0882 | 0.0148 | 49 | 29 | 0.0308 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B0 | B2 | 1031 | 0.5606 | 0.5538 | -0.0068 | 96 | 103 | 0.6707 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B0 | B3 | 1037 | 0.5632 | 0.3539 | -0.2093 | 40 | 257 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B0 | B4 | 1040 | 0.5635 | 0.3548 | -0.2087 | 35 | 252 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B0 | B5 | 1045 | 0.5636 | 0.7589 | 0.1952 | 223 | 19 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B2 | B3 | 1039 | 0.5553 | 0.3561 | -0.1992 | 19 | 226 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B2 | B4 | 1045 | 0.5579 | 0.3598 | -0.1981 | 15 | 222 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B2 | B5 | 1029 | 0.552 | 0.7541 | 0.2021 | 226 | 18 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B3 | B4 | 1057 | 0.3623 | 0.3652 | 0.0028 | 69 | 66 | 0.8634 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B3 | B5 | 1019 | 0.3474 | 0.7547 | 0.4073 | 425 | 10 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 1914 |  | B4 | B5 | 1024 | 0.3516 | 0.7539 | 0.4023 | 424 | 12 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B0 | B2 | 1062 | 0.516 | 0.436 | -0.08 | 52 | 137 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B0 | B3 | 1030 | 0.5068 | 0.3544 | -0.1524 | 41 | 198 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B0 | B4 | 1051 | 0.5147 | 0.3597 | -0.1551 | 38 | 201 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B0 | B5 | 1053 | 0.5157 | 0.7284 | 0.2127 | 233 | 9 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B2 | B3 | 1028 | 0.4251 | 0.3512 | -0.0739 | 52 | 128 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B2 | B4 | 1037 | 0.4291 | 0.352 | -0.0771 | 58 | 138 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B2 | B5 | 1048 | 0.4313 | 0.7242 | 0.2929 | 324 | 17 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B3 | B4 | 1037 | 0.3549 | 0.352 | -0.0029 | 69 | 72 | 0.8663 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B3 | B5 | 1022 | 0.3523 | 0.7202 | 0.3679 | 387 | 11 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 2024 |  | B4 | B5 | 1038 | 0.3565 | 0.7245 | 0.368 | 392 | 10 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B0 | B2 | 1034 | 0.5696 | 0.587 | 0.0174 | 92 | 74 | 0.1869 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B0 | B3 | 1042 | 0.571 | 0.3253 | -0.2457 | 26 | 282 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B0 | B4 | 1031 | 0.5674 | 0.386 | -0.1814 | 43 | 230 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B0 | B5 | 1048 | 0.5706 | 0.7471 | 0.1765 | 202 | 17 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B2 | B3 | 1024 | 0.5859 | 0.3213 | -0.2646 | 17 | 288 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B2 | B4 | 1030 | 0.5845 | 0.3864 | -0.1981 | 19 | 223 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B2 | B5 | 1042 | 0.5883 | 0.7466 | 0.1583 | 188 | 23 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B3 | B4 | 1040 | 0.325 | 0.3894 | 0.0644 | 116 | 49 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B3 | B5 | 1039 | 0.3272 | 0.7449 | 0.4177 | 444 | 10 | 0.0 |
| textfooler | reviews | ukr_roberta | wsd035 | 7 |  | B4 | B5 | 1043 | 0.3912 | 0.7469 | 0.3557 | 382 | 11 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B0 | B2 | 1031 | 0.5936 | 0.5839 | -0.0097 | 87 | 97 | 0.5071 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B0 | B3 | 1037 | 0.5959 | 0.3626 | -0.2334 | 31 | 273 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B0 | B4 | 1040 | 0.5962 | 0.376 | -0.2202 | 31 | 260 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B0 | B5 | 1045 | 0.5952 | 0.7789 | 0.1837 | 208 | 16 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B2 | B3 | 1039 | 0.5852 | 0.3648 | -0.2204 | 18 | 247 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B2 | B4 | 1045 | 0.5876 | 0.3799 | -0.2077 | 15 | 232 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B2 | B5 | 1029 | 0.5821 | 0.7755 | 0.1934 | 215 | 16 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B3 | B4 | 1057 | 0.3709 | 0.386 | 0.0151 | 80 | 64 | 0.2112 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B3 | B5 | 1019 | 0.3562 | 0.7763 | 0.42 | 436 | 8 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 1914 |  | B4 | B5 | 1024 | 0.3711 | 0.7754 | 0.4043 | 426 | 12 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B0 | B2 | 1062 | 0.5499 | 0.4623 | -0.0876 | 50 | 143 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B0 | B3 | 1030 | 0.5408 | 0.3796 | -0.1612 | 46 | 212 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B0 | B4 | 1051 | 0.5471 | 0.3863 | -0.1608 | 42 | 211 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B0 | B5 | 1053 | 0.548 | 0.7512 | 0.2032 | 224 | 10 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B2 | B3 | 1028 | 0.4514 | 0.3765 | -0.0749 | 53 | 130 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B2 | B4 | 1037 | 0.4552 | 0.3809 | -0.0743 | 68 | 145 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B2 | B5 | 1048 | 0.458 | 0.7481 | 0.2901 | 320 | 16 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B3 | B4 | 1037 | 0.3799 | 0.3799 | 0.0 | 79 | 79 | 1.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B3 | B5 | 1022 | 0.3757 | 0.7436 | 0.3679 | 387 | 11 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 2024 |  | B4 | B5 | 1038 | 0.3825 | 0.7476 | 0.3651 | 389 | 10 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B0 | B2 | 1034 | 0.6035 | 0.6122 | 0.0087 | 84 | 75 | 0.5259 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B0 | B3 | 1042 | 0.6036 | 0.3474 | -0.2562 | 23 | 290 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B0 | B4 | 1031 | 0.6004 | 0.4132 | -0.1872 | 37 | 230 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B0 | B5 | 1048 | 0.6021 | 0.7796 | 0.1775 | 203 | 17 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B2 | B3 | 1024 | 0.6104 | 0.3438 | -0.2666 | 20 | 293 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B2 | B4 | 1030 | 0.6097 | 0.4136 | -0.1961 | 24 | 226 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B2 | B5 | 1042 | 0.6123 | 0.7783 | 0.166 | 192 | 19 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B3 | B4 | 1040 | 0.3481 | 0.4183 | 0.0702 | 121 | 48 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B3 | B5 | 1039 | 0.3494 | 0.7767 | 0.4273 | 453 | 9 | 0.0 |
| textfooler | reviews | ukr_roberta |  | 7 |  | B4 | B5 | 1043 | 0.4199 | 0.7785 | 0.3586 | 385 | 11 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B0 | B1 | 1077 | 0.3417 | 0.3825 | 0.0409 | 130 | 86 | 0.0033 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B0 | B2 | 1087 | 0.3487 | 0.3284 | -0.0202 | 82 | 104 | 0.1234 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B0 | B3 | 1088 | 0.3483 | 0.2675 | -0.0809 | 53 | 141 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B0 | B4 | 1096 | 0.3485 | 0.2573 | -0.0912 | 59 | 159 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B0 | B5 | 1079 | 0.3448 | 0.5449 | 0.2002 | 246 | 30 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B0 | B6 | 1103 | 0.3518 | 0.3554 | 0.0036 | 98 | 94 | 0.8287 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B0 | B7 | 1097 | 0.3519 | 0.3355 | -0.0164 | 85 | 103 | 0.2149 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B1 | B2 | 1066 | 0.3827 | 0.3199 | -0.0629 | 78 | 145 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B1 | B3 | 1077 | 0.3816 | 0.26 | -0.1216 | 47 | 178 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B1 | B4 | 1081 | 0.383 | 0.2488 | -0.1341 | 42 | 187 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B1 | B5 | 1078 | 0.3822 | 0.5445 | 0.1623 | 217 | 42 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B1 | B6 | 1081 | 0.3867 | 0.3478 | -0.0389 | 80 | 122 | 0.0038 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B1 | B7 | 1063 | 0.381 | 0.3246 | -0.0564 | 75 | 135 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B2 | B3 | 1086 | 0.3297 | 0.268 | -0.0617 | 55 | 122 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B2 | B4 | 1083 | 0.3287 | 0.253 | -0.0757 | 49 | 131 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B2 | B5 | 1070 | 0.3196 | 0.5458 | 0.2262 | 273 | 31 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B2 | B6 | 1089 | 0.3324 | 0.3517 | 0.0193 | 95 | 74 | 0.1237 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B2 | B7 | 1086 | 0.3297 | 0.3379 | 0.0083 | 98 | 89 | 0.5587 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B3 | B4 | 1093 | 0.2662 | 0.2525 | -0.0137 | 67 | 82 | 0.2513 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B3 | B5 | 1079 | 0.2576 | 0.544 | 0.2864 | 326 | 17 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B3 | B6 | 1093 | 0.2699 | 0.3532 | 0.0833 | 132 | 41 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B3 | B7 | 1087 | 0.2677 | 0.333 | 0.0653 | 129 | 58 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B4 | B5 | 1076 | 0.2454 | 0.5465 | 0.3011 | 341 | 17 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B4 | B6 | 1099 | 0.2611 | 0.3549 | 0.0937 | 146 | 43 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B4 | B7 | 1082 | 0.2542 | 0.3299 | 0.0758 | 138 | 56 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B5 | B6 | 1082 | 0.5481 | 0.3466 | -0.2015 | 34 | 252 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B5 | B7 | 1073 | 0.5461 | 0.3271 | -0.219 | 28 | 263 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 |  | B6 | B7 | 1090 | 0.3505 | 0.3339 | -0.0165 | 86 | 104 | 0.2174 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | full78k | B0 | B2 | 1084 | 0.4041 | 0.2998 | -0.1042 | 59 | 172 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | full78k | B0 | B3 | 1069 | 0.4041 | 0.1319 | -0.2722 | 16 | 307 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | full78k | B0 | B4 | 1070 | 0.4047 | 0.2103 | -0.1944 | 24 | 232 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | full78k | B2 | B3 | 1099 | 0.3066 | 0.1483 | -0.1583 | 29 | 203 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | full78k | B2 | B4 | 1092 | 0.3049 | 0.2207 | -0.0842 | 51 | 143 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | full78k | B3 | B4 | 1105 | 0.1493 | 0.2271 | 0.0778 | 117 | 31 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | pool10x20 | B0 | B3 | 1080 | 0.3454 | 0.3954 | 0.05 | 166 | 112 | 0.0014 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | pool10x20 | B0 | B4 | 1087 | 0.3487 | 0.3238 | -0.0248 | 113 | 140 | 0.1019 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | pool10x20 | B0 | B5 | 1086 | 0.3453 | 0.5967 | 0.2514 | 290 | 17 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | pool10x20 | B3 | B4 | 1083 | 0.3952 | 0.3176 | -0.0776 | 51 | 135 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | pool10x20 | B3 | B5 | 1072 | 0.3927 | 0.5924 | 0.1996 | 255 | 41 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | pool10x20 | B4 | B5 | 1073 | 0.3159 | 0.5946 | 0.2787 | 323 | 24 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r0.25 | B0 | B2 | 1110 | 0.355 | 0.3108 | -0.0441 | 70 | 119 | 0.0004 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r0.25 | B0 | B3 | 1104 | 0.3478 | 0.2283 | -0.1196 | 37 | 169 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r0.25 | B0 | B4 | 1101 | 0.3506 | 0.2407 | -0.1099 | 36 | 157 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r0.25 | B2 | B3 | 1105 | 0.3113 | 0.2335 | -0.0778 | 46 | 132 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r0.25 | B2 | B4 | 1101 | 0.3134 | 0.2443 | -0.069 | 47 | 123 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r0.25 | B3 | B4 | 1105 | 0.2335 | 0.2452 | 0.0118 | 67 | 54 | 0.2753 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r1.0 | B0 | B2 | 1084 | 0.3469 | 0.2869 | -0.06 | 73 | 138 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r1.0 | B0 | B3 | 1099 | 0.3494 | 0.1811 | -0.1683 | 30 | 215 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r1.0 | B0 | B4 | 1082 | 0.3438 | 0.2135 | -0.1303 | 31 | 172 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r1.0 | B2 | B3 | 1069 | 0.2862 | 0.1684 | -0.1179 | 27 | 153 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r1.0 | B2 | B4 | 1070 | 0.2822 | 0.2112 | -0.071 | 42 | 118 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 1914 | r1.0 | B3 | B4 | 1076 | 0.1654 | 0.2128 | 0.0474 | 92 | 41 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B0 | B1 | 1098 | 0.3643 | 0.2887 | -0.0756 | 59 | 142 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B0 | B2 | 1104 | 0.3678 | 0.2899 | -0.0779 | 55 | 141 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B0 | B3 | 1103 | 0.3645 | 0.1976 | -0.1668 | 35 | 219 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B0 | B4 | 1111 | 0.3735 | 0.2295 | -0.144 | 35 | 195 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B0 | B5 | 1103 | 0.3663 | 0.4578 | 0.0916 | 160 | 59 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B0 | B6 | 1095 | 0.3662 | 0.3726 | 0.0064 | 107 | 100 | 0.6768 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B0 | B7 | 1088 | 0.3621 | 0.3603 | -0.0018 | 100 | 102 | 0.9439 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B1 | B2 | 1125 | 0.3031 | 0.2969 | -0.0062 | 73 | 80 | 0.6278 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B1 | B3 | 1111 | 0.2952 | 0.198 | -0.0972 | 33 | 141 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B1 | B4 | 1118 | 0.3014 | 0.2281 | -0.0733 | 44 | 126 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B1 | B5 | 1119 | 0.2994 | 0.462 | 0.1626 | 221 | 39 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B1 | B6 | 1102 | 0.2931 | 0.3739 | 0.0808 | 154 | 65 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B1 | B7 | 1101 | 0.2916 | 0.3633 | 0.0718 | 146 | 67 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B2 | B3 | 1116 | 0.2912 | 0.2025 | -0.0887 | 40 | 139 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B2 | B4 | 1127 | 0.3008 | 0.2316 | -0.0692 | 40 | 118 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B2 | B5 | 1120 | 0.2929 | 0.4625 | 0.1696 | 227 | 37 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B2 | B6 | 1110 | 0.2955 | 0.3793 | 0.0838 | 157 | 64 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B2 | B7 | 1115 | 0.2951 | 0.3713 | 0.0762 | 140 | 55 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B3 | B4 | 1117 | 0.2041 | 0.2238 | 0.0197 | 74 | 52 | 0.0609 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B3 | B5 | 1114 | 0.2029 | 0.4605 | 0.2576 | 306 | 19 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B3 | B6 | 1104 | 0.1984 | 0.3759 | 0.1775 | 229 | 33 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B3 | B7 | 1104 | 0.1947 | 0.3641 | 0.1694 | 216 | 29 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B4 | B5 | 1122 | 0.2317 | 0.4652 | 0.2335 | 287 | 25 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B4 | B6 | 1116 | 0.2312 | 0.3826 | 0.1514 | 201 | 32 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B4 | B7 | 1106 | 0.2215 | 0.3689 | 0.1474 | 196 | 33 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B5 | B6 | 1105 | 0.4624 | 0.3774 | -0.0851 | 63 | 157 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B5 | B7 | 1103 | 0.4569 | 0.3645 | -0.0925 | 68 | 170 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 |  | B6 | B7 | 1094 | 0.3739 | 0.3665 | -0.0073 | 88 | 96 | 0.6059 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | full78k | B0 | B2 | 1087 | 0.3441 | 0.1868 | -0.1573 | 36 | 207 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | full78k | B0 | B3 | 1095 | 0.347 | 0.368 | 0.021 | 160 | 137 | 0.2017 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | full78k | B0 | B4 | 1099 | 0.3485 | 0.3085 | -0.04 | 87 | 131 | 0.0035 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | full78k | B2 | B3 | 1098 | 0.194 | 0.3707 | 0.1767 | 256 | 62 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | full78k | B2 | B4 | 1079 | 0.1854 | 0.3021 | 0.1168 | 184 | 58 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | full78k | B3 | B4 | 1101 | 0.3724 | 0.3061 | -0.0663 | 74 | 147 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | pool10x20 | B0 | B3 | 1094 | 0.3684 | 0.2176 | -0.1508 | 35 | 200 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | pool10x20 | B0 | B4 | 1088 | 0.3621 | 0.2509 | -0.1112 | 46 | 167 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | pool10x20 | B0 | B5 | 1081 | 0.358 | 0.5745 | 0.2165 | 264 | 30 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | pool10x20 | B3 | B4 | 1097 | 0.2151 | 0.2516 | 0.0365 | 87 | 47 | 0.0007 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | pool10x20 | B3 | B5 | 1074 | 0.2104 | 0.5754 | 0.365 | 409 | 17 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | pool10x20 | B4 | B5 | 1073 | 0.2423 | 0.5713 | 0.329 | 371 | 18 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | r1.0 | B0 | B2 | 1102 | 0.3684 | 0.3167 | -0.0517 | 84 | 141 | 0.0002 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | r1.0 | B0 | B3 | 1087 | 0.3671 | 0.2042 | -0.1628 | 36 | 213 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | r1.0 | B0 | B4 | 1086 | 0.3628 | 0.2385 | -0.1243 | 48 | 183 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | r1.0 | B2 | B3 | 1096 | 0.3148 | 0.208 | -0.1068 | 41 | 158 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | r1.0 | B2 | B4 | 1101 | 0.3161 | 0.2452 | -0.0708 | 48 | 126 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 2024 | r1.0 | B3 | B4 | 1099 | 0.212 | 0.2411 | 0.0291 | 94 | 62 | 0.0128 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B0 | B1 | 1098 | 0.3033 | 0.3479 | 0.0446 | 124 | 75 | 0.0006 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B0 | B2 | 1097 | 0.3045 | 0.2972 | -0.0073 | 92 | 100 | 0.6135 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B0 | B3 | 1093 | 0.3047 | 0.3486 | 0.0439 | 138 | 90 | 0.0018 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B0 | B4 | 1097 | 0.3099 | 0.2589 | -0.051 | 69 | 125 | 0.0001 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B0 | B5 | 1091 | 0.3034 | 0.4922 | 0.1888 | 244 | 38 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B0 | B6 | 1096 | 0.3038 | 0.3714 | 0.0675 | 140 | 66 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B0 | B7 | 1101 | 0.3097 | 0.3052 | -0.0045 | 87 | 92 | 0.7651 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B1 | B2 | 1112 | 0.3561 | 0.3004 | -0.0558 | 65 | 127 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B1 | B3 | 1105 | 0.3511 | 0.3529 | 0.0018 | 98 | 96 | 0.9428 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B1 | B4 | 1105 | 0.3548 | 0.2643 | -0.0905 | 54 | 154 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B1 | B5 | 1101 | 0.3542 | 0.4959 | 0.1417 | 196 | 40 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B1 | B6 | 1105 | 0.3511 | 0.3765 | 0.0253 | 109 | 81 | 0.0499 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B1 | B7 | 1097 | 0.3491 | 0.3026 | -0.0465 | 68 | 119 | 0.0002 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B2 | B3 | 1104 | 0.2971 | 0.3524 | 0.0553 | 140 | 79 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B2 | B4 | 1112 | 0.3022 | 0.2689 | -0.0333 | 70 | 107 | 0.0066 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B2 | B5 | 1101 | 0.2961 | 0.4968 | 0.2007 | 255 | 34 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B2 | B6 | 1101 | 0.297 | 0.3742 | 0.0772 | 148 | 63 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B2 | B7 | 1096 | 0.2965 | 0.3057 | 0.0091 | 103 | 93 | 0.5204 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B3 | B4 | 1104 | 0.3551 | 0.2663 | -0.0888 | 52 | 150 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B3 | B5 | 1096 | 0.3485 | 0.4964 | 0.1478 | 214 | 52 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B3 | B6 | 1099 | 0.3503 | 0.3776 | 0.0273 | 123 | 93 | 0.0482 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B3 | B7 | 1089 | 0.3489 | 0.3012 | -0.0478 | 88 | 140 | 0.0007 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B4 | B5 | 1099 | 0.2611 | 0.4968 | 0.2357 | 289 | 30 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B4 | B6 | 1101 | 0.2625 | 0.3797 | 0.1172 | 169 | 40 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B4 | B7 | 1100 | 0.26 | 0.3027 | 0.0427 | 121 | 74 | 0.0009 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B5 | B6 | 1097 | 0.4941 | 0.3756 | -0.1185 | 53 | 183 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B5 | B7 | 1092 | 0.4973 | 0.3022 | -0.1951 | 30 | 243 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 |  | B6 | B7 | 1090 | 0.3761 | 0.2982 | -0.078 | 63 | 148 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | full78k | B0 | B2 | 1090 | 0.322 | 0.3239 | 0.0018 | 109 | 107 | 0.9458 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | full78k | B0 | B3 | 1084 | 0.322 | 0.1753 | -0.1467 | 39 | 198 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | full78k | B0 | B4 | 1103 | 0.3291 | 0.2638 | -0.0653 | 77 | 149 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | full78k | B2 | B3 | 1092 | 0.3242 | 0.1804 | -0.1438 | 36 | 193 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | full78k | B2 | B4 | 1103 | 0.3255 | 0.2611 | -0.0644 | 75 | 146 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | full78k | B3 | B4 | 1093 | 0.1812 | 0.2553 | 0.0741 | 152 | 71 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | pool10x20 | B0 | B3 | 1094 | 0.3026 | 0.3062 | 0.0037 | 117 | 113 | 0.8432 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | pool10x20 | B0 | B4 | 1102 | 0.3085 | 0.1887 | -0.1198 | 36 | 168 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | pool10x20 | B0 | B5 | 1088 | 0.3006 | 0.5423 | 0.2417 | 283 | 20 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | pool10x20 | B3 | B4 | 1092 | 0.304 | 0.1859 | -0.1181 | 59 | 188 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | pool10x20 | B3 | B5 | 1074 | 0.2998 | 0.54 | 0.2402 | 287 | 29 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | pool10x20 | B4 | B5 | 1081 | 0.1859 | 0.5439 | 0.358 | 398 | 11 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | r1.0 | B0 | B2 | 1095 | 0.305 | 0.2831 | -0.0219 | 84 | 108 | 0.0967 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | r1.0 | B0 | B3 | 1080 | 0.3037 | 0.1843 | -0.1194 | 38 | 167 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | r1.0 | B0 | B4 | 1098 | 0.3097 | 0.1667 | -0.143 | 26 | 183 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | r1.0 | B2 | B3 | 1082 | 0.281 | 0.1904 | -0.0906 | 36 | 134 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | r1.0 | B2 | B4 | 1088 | 0.2849 | 0.1682 | -0.1167 | 32 | 159 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | 7 | r1.0 | B3 | B4 | 1087 | 0.1914 | 0.1665 | -0.0248 | 52 | 79 | 0.0227 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B0 | B1 | 1077 | 0.3668 | 0.4169 | 0.0501 | 142 | 88 | 0.0004 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B0 | B2 | 1087 | 0.3726 | 0.356 | -0.0166 | 94 | 112 | 0.2362 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B0 | B3 | 1088 | 0.3722 | 0.2776 | -0.0947 | 52 | 155 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B0 | B4 | 1096 | 0.3741 | 0.2828 | -0.0912 | 54 | 154 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B0 | B5 | 1079 | 0.3679 | 0.5894 | 0.2215 | 270 | 31 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B0 | B6 | 1103 | 0.3772 | 0.388 | 0.0109 | 103 | 91 | 0.4297 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B0 | B7 | 1097 | 0.3765 | 0.3783 | 0.0018 | 96 | 94 | 0.9422 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B1 | B2 | 1066 | 0.4165 | 0.349 | -0.0675 | 71 | 143 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B1 | B3 | 1077 | 0.415 | 0.2711 | -0.1439 | 44 | 199 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B1 | B4 | 1081 | 0.4154 | 0.2757 | -0.1397 | 42 | 193 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B1 | B5 | 1078 | 0.4137 | 0.5891 | 0.1753 | 229 | 40 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B1 | B6 | 1081 | 0.42 | 0.3793 | -0.0407 | 79 | 123 | 0.0024 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B1 | B7 | 1063 | 0.4158 | 0.3678 | -0.048 | 85 | 136 | 0.0007 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B2 | B3 | 1086 | 0.36 | 0.2799 | -0.0801 | 50 | 137 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B2 | B4 | 1083 | 0.3564 | 0.2789 | -0.0776 | 53 | 137 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B2 | B5 | 1070 | 0.3486 | 0.5907 | 0.2421 | 293 | 34 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B2 | B6 | 1089 | 0.3609 | 0.3838 | 0.023 | 103 | 78 | 0.0741 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B2 | B7 | 1086 | 0.3582 | 0.3803 | 0.0221 | 108 | 84 | 0.0967 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B3 | B4 | 1093 | 0.2772 | 0.2781 | 0.0009 | 82 | 81 | 1.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B3 | B5 | 1079 | 0.2688 | 0.5885 | 0.3197 | 363 | 18 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B3 | B6 | 1093 | 0.28 | 0.3852 | 0.1052 | 156 | 41 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B3 | B7 | 1087 | 0.2778 | 0.3763 | 0.0984 | 161 | 54 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B4 | B5 | 1076 | 0.2723 | 0.5901 | 0.3178 | 359 | 17 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B4 | B6 | 1099 | 0.2866 | 0.3867 | 0.1001 | 155 | 45 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B4 | B7 | 1082 | 0.28 | 0.3725 | 0.0924 | 151 | 51 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B5 | B6 | 1082 | 0.5924 | 0.3789 | -0.2135 | 35 | 266 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B5 | B7 | 1073 | 0.5899 | 0.3691 | -0.2209 | 30 | 267 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 |  | B6 | B7 | 1090 | 0.3826 | 0.3771 | -0.0055 | 97 | 103 | 0.7238 |
| textfooler | reviews | xlmr_base |  | 1914 | full78k | B0 | B2 | 1084 | 0.4262 | 0.3238 | -0.1024 | 57 | 168 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | full78k | B0 | B3 | 1069 | 0.4247 | 0.1403 | -0.2844 | 15 | 319 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | full78k | B0 | B4 | 1070 | 0.4252 | 0.2336 | -0.1916 | 30 | 235 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | full78k | B2 | B3 | 1099 | 0.3312 | 0.1574 | -0.1738 | 28 | 219 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | full78k | B2 | B4 | 1092 | 0.3297 | 0.2427 | -0.087 | 53 | 148 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | full78k | B3 | B4 | 1105 | 0.1566 | 0.248 | 0.0914 | 128 | 27 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | pool10x20 | B0 | B3 | 1080 | 0.3704 | 0.3954 | 0.025 | 158 | 131 | 0.126 |
| textfooler | reviews | xlmr_base |  | 1914 | pool10x20 | B0 | B4 | 1087 | 0.3744 | 0.3349 | -0.0396 | 105 | 148 | 0.0082 |
| textfooler | reviews | xlmr_base |  | 1914 | pool10x20 | B0 | B5 | 1086 | 0.3702 | 0.6133 | 0.2431 | 284 | 20 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | pool10x20 | B3 | B4 | 1083 | 0.3952 | 0.3269 | -0.0683 | 59 | 133 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | pool10x20 | B3 | B5 | 1072 | 0.3937 | 0.6091 | 0.2155 | 270 | 39 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | pool10x20 | B4 | B5 | 1073 | 0.3262 | 0.6114 | 0.2852 | 331 | 25 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r0.25 | B0 | B2 | 1110 | 0.3784 | 0.3306 | -0.0477 | 72 | 125 | 0.0002 |
| textfooler | reviews | xlmr_base |  | 1914 | r0.25 | B0 | B3 | 1104 | 0.3732 | 0.2382 | -0.135 | 36 | 185 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r0.25 | B0 | B4 | 1101 | 0.3751 | 0.257 | -0.1181 | 44 | 174 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r0.25 | B2 | B3 | 1105 | 0.3294 | 0.2443 | -0.0851 | 50 | 144 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r0.25 | B2 | B4 | 1101 | 0.3333 | 0.2598 | -0.0736 | 52 | 133 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r0.25 | B3 | B4 | 1105 | 0.2443 | 0.2615 | 0.0172 | 81 | 62 | 0.132 |
| textfooler | reviews | xlmr_base |  | 1914 | r1.0 | B0 | B2 | 1084 | 0.3718 | 0.3054 | -0.0664 | 72 | 144 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r1.0 | B0 | B3 | 1099 | 0.374 | 0.192 | -0.182 | 29 | 229 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r1.0 | B0 | B4 | 1082 | 0.3678 | 0.2264 | -0.1414 | 37 | 190 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r1.0 | B2 | B3 | 1069 | 0.304 | 0.1787 | -0.1254 | 32 | 166 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r1.0 | B2 | B4 | 1070 | 0.2991 | 0.2243 | -0.0748 | 50 | 130 | 0.0 |
| textfooler | reviews | xlmr_base |  | 1914 | r1.0 | B3 | B4 | 1076 | 0.1766 | 0.2258 | 0.0493 | 96 | 43 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B0 | B1 | 1098 | 0.3843 | 0.3124 | -0.0719 | 65 | 144 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B0 | B2 | 1104 | 0.3868 | 0.3207 | -0.0661 | 60 | 133 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B0 | B3 | 1103 | 0.3835 | 0.2076 | -0.1759 | 39 | 233 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B0 | B4 | 1111 | 0.3924 | 0.2583 | -0.1341 | 47 | 196 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B0 | B5 | 1103 | 0.3844 | 0.495 | 0.1106 | 183 | 61 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B0 | B6 | 1095 | 0.3854 | 0.3954 | 0.01 | 105 | 94 | 0.4785 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B0 | B7 | 1088 | 0.3814 | 0.3971 | 0.0156 | 118 | 101 | 0.2796 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B1 | B2 | 1125 | 0.3262 | 0.328 | 0.0018 | 85 | 83 | 0.9385 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B1 | B3 | 1111 | 0.3177 | 0.2079 | -0.1098 | 33 | 155 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B1 | B4 | 1118 | 0.3247 | 0.2558 | -0.0689 | 54 | 131 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B1 | B5 | 1119 | 0.3217 | 0.4987 | 0.1769 | 232 | 34 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B1 | B6 | 1102 | 0.3167 | 0.3956 | 0.0789 | 148 | 61 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B1 | B7 | 1101 | 0.3152 | 0.4024 | 0.0872 | 159 | 63 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B2 | B3 | 1116 | 0.3226 | 0.2124 | -0.1102 | 36 | 159 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B2 | B4 | 1127 | 0.331 | 0.2609 | -0.0701 | 46 | 125 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B2 | B5 | 1120 | 0.3241 | 0.4991 | 0.175 | 235 | 39 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B2 | B6 | 1110 | 0.3261 | 0.4009 | 0.0748 | 149 | 66 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B2 | B7 | 1115 | 0.3265 | 0.4099 | 0.0834 | 151 | 58 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B3 | B4 | 1117 | 0.2149 | 0.2543 | 0.0394 | 95 | 51 | 0.0003 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B3 | B5 | 1114 | 0.2118 | 0.4973 | 0.2855 | 340 | 22 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B3 | B6 | 1104 | 0.2101 | 0.3976 | 0.1875 | 239 | 32 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B3 | B7 | 1104 | 0.2047 | 0.4022 | 0.1975 | 246 | 28 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B4 | B5 | 1122 | 0.2602 | 0.5018 | 0.2415 | 298 | 27 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B4 | B6 | 1116 | 0.2616 | 0.4041 | 0.1425 | 197 | 38 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B4 | B7 | 1106 | 0.2505 | 0.406 | 0.1555 | 205 | 33 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B5 | B6 | 1105 | 0.4995 | 0.3991 | -0.1005 | 62 | 173 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B5 | B7 | 1103 | 0.4941 | 0.4025 | -0.0916 | 65 | 166 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 |  | B6 | B7 | 1094 | 0.3958 | 0.4049 | 0.0091 | 97 | 87 | 0.5071 |
| textfooler | reviews | xlmr_base |  | 2024 | full78k | B0 | B2 | 1087 | 0.3698 | 0.2079 | -0.1619 | 38 | 214 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | full78k | B0 | B3 | 1095 | 0.3735 | 0.3735 | 0.0 | 142 | 142 | 1.0 |
| textfooler | reviews | xlmr_base |  | 2024 | full78k | B0 | B4 | 1099 | 0.374 | 0.3312 | -0.0428 | 92 | 139 | 0.0024 |
| textfooler | reviews | xlmr_base |  | 2024 | full78k | B2 | B3 | 1098 | 0.214 | 0.378 | 0.1639 | 250 | 70 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | full78k | B2 | B4 | 1079 | 0.2057 | 0.3244 | 0.1186 | 187 | 59 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | full78k | B3 | B4 | 1101 | 0.3787 | 0.3288 | -0.05 | 86 | 141 | 0.0003 |
| textfooler | reviews | xlmr_base |  | 2024 | pool10x20 | B0 | B3 | 1094 | 0.3876 | 0.2303 | -0.1572 | 40 | 212 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | pool10x20 | B0 | B4 | 1088 | 0.3824 | 0.2702 | -0.1121 | 51 | 173 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | pool10x20 | B0 | B5 | 1081 | 0.3765 | 0.6078 | 0.2313 | 269 | 19 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | pool10x20 | B3 | B4 | 1097 | 0.2297 | 0.2707 | 0.041 | 98 | 53 | 0.0003 |
| textfooler | reviews | xlmr_base |  | 2024 | pool10x20 | B3 | B5 | 1074 | 0.2225 | 0.6089 | 0.3864 | 429 | 14 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | pool10x20 | B4 | B5 | 1073 | 0.261 | 0.6039 | 0.343 | 381 | 13 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | r1.0 | B0 | B2 | 1102 | 0.3875 | 0.3494 | -0.0381 | 88 | 130 | 0.0054 |
| textfooler | reviews | xlmr_base |  | 2024 | r1.0 | B0 | B3 | 1087 | 0.3864 | 0.2328 | -0.1536 | 45 | 212 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | r1.0 | B0 | B4 | 1086 | 0.3831 | 0.2532 | -0.1298 | 45 | 186 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | r1.0 | B2 | B3 | 1096 | 0.3467 | 0.2363 | -0.1104 | 43 | 164 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | r1.0 | B2 | B4 | 1101 | 0.3506 | 0.2589 | -0.0917 | 41 | 142 | 0.0 |
| textfooler | reviews | xlmr_base |  | 2024 | r1.0 | B3 | B4 | 1099 | 0.2402 | 0.2548 | 0.0146 | 87 | 71 | 0.2326 |
| textfooler | reviews | xlmr_base |  | 7 |  | B0 | B1 | 1098 | 0.3361 | 0.378 | 0.0419 | 128 | 82 | 0.0018 |
| textfooler | reviews | xlmr_base |  | 7 |  | B0 | B2 | 1097 | 0.3382 | 0.3236 | -0.0146 | 91 | 107 | 0.2864 |
| textfooler | reviews | xlmr_base |  | 7 |  | B0 | B3 | 1093 | 0.3358 | 0.3669 | 0.0311 | 140 | 106 | 0.0352 |
| textfooler | reviews | xlmr_base |  | 7 |  | B0 | B4 | 1097 | 0.3418 | 0.2753 | -0.0665 | 67 | 140 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B0 | B5 | 1091 | 0.3336 | 0.5096 | 0.176 | 236 | 44 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B0 | B6 | 1096 | 0.3367 | 0.4024 | 0.0657 | 147 | 75 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B0 | B7 | 1101 | 0.3406 | 0.3315 | -0.0091 | 93 | 103 | 0.5204 |
| textfooler | reviews | xlmr_base |  | 7 |  | B1 | B2 | 1112 | 0.3849 | 0.3291 | -0.0558 | 66 | 128 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B1 | B3 | 1105 | 0.381 | 0.371 | -0.01 | 96 | 107 | 0.4829 |
| textfooler | reviews | xlmr_base |  | 7 |  | B1 | B4 | 1105 | 0.3846 | 0.2796 | -0.105 | 46 | 162 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B1 | B5 | 1101 | 0.3824 | 0.5141 | 0.1317 | 191 | 46 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B1 | B6 | 1105 | 0.3801 | 0.4072 | 0.0271 | 107 | 77 | 0.0322 |
| textfooler | reviews | xlmr_base |  | 7 |  | B1 | B7 | 1097 | 0.3792 | 0.3291 | -0.0501 | 71 | 126 | 0.0001 |
| textfooler | reviews | xlmr_base |  | 7 |  | B2 | B3 | 1104 | 0.3252 | 0.3705 | 0.0453 | 137 | 87 | 0.001 |
| textfooler | reviews | xlmr_base |  | 7 |  | B2 | B4 | 1112 | 0.3309 | 0.2842 | -0.0468 | 58 | 110 | 0.0001 |
| textfooler | reviews | xlmr_base |  | 7 |  | B2 | B5 | 1101 | 0.3261 | 0.5141 | 0.188 | 241 | 34 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B2 | B6 | 1101 | 0.3233 | 0.4051 | 0.0817 | 153 | 63 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B2 | B7 | 1096 | 0.3257 | 0.3321 | 0.0064 | 100 | 93 | 0.6659 |
| textfooler | reviews | xlmr_base |  | 7 |  | B3 | B4 | 1104 | 0.3732 | 0.2808 | -0.0924 | 49 | 151 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B3 | B5 | 1096 | 0.3686 | 0.5137 | 0.1451 | 209 | 50 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B3 | B6 | 1099 | 0.3694 | 0.4086 | 0.0391 | 131 | 88 | 0.0044 |
| textfooler | reviews | xlmr_base |  | 7 |  | B3 | B7 | 1089 | 0.3691 | 0.3269 | -0.0422 | 89 | 135 | 0.0026 |
| textfooler | reviews | xlmr_base |  | 7 |  | B4 | B5 | 1099 | 0.2766 | 0.5141 | 0.2375 | 288 | 27 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B4 | B6 | 1101 | 0.277 | 0.4105 | 0.1335 | 190 | 43 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B4 | B7 | 1100 | 0.2745 | 0.3282 | 0.0536 | 132 | 73 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B5 | B6 | 1097 | 0.5114 | 0.4066 | -0.1048 | 57 | 172 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B5 | B7 | 1092 | 0.5147 | 0.3288 | -0.1859 | 35 | 238 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 |  | B6 | B7 | 1090 | 0.4073 | 0.3239 | -0.0835 | 66 | 157 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | full78k | B0 | B2 | 1090 | 0.3716 | 0.3596 | -0.0119 | 102 | 115 | 0.4154 |
| textfooler | reviews | xlmr_base |  | 7 | full78k | B0 | B3 | 1084 | 0.3708 | 0.1946 | -0.1762 | 36 | 227 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | full78k | B0 | B4 | 1103 | 0.379 | 0.2738 | -0.1052 | 66 | 182 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | full78k | B2 | B3 | 1092 | 0.3617 | 0.1987 | -0.163 | 39 | 217 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | full78k | B2 | B4 | 1103 | 0.3636 | 0.2711 | -0.0925 | 69 | 171 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | full78k | B3 | B4 | 1093 | 0.1995 | 0.2653 | 0.0659 | 153 | 81 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | pool10x20 | B0 | B3 | 1094 | 0.3327 | 0.3144 | -0.0183 | 115 | 135 | 0.2294 |
| textfooler | reviews | xlmr_base |  | 7 | pool10x20 | B0 | B4 | 1102 | 0.3412 | 0.2087 | -0.1325 | 39 | 185 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | pool10x20 | B0 | B5 | 1088 | 0.3327 | 0.5625 | 0.2298 | 275 | 25 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | pool10x20 | B3 | B4 | 1092 | 0.3123 | 0.207 | -0.1053 | 60 | 175 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | pool10x20 | B3 | B5 | 1074 | 0.3073 | 0.5605 | 0.2533 | 301 | 29 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | pool10x20 | B4 | B5 | 1081 | 0.2054 | 0.5643 | 0.3589 | 401 | 13 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | r1.0 | B0 | B2 | 1095 | 0.337 | 0.3169 | -0.0201 | 91 | 113 | 0.1413 |
| textfooler | reviews | xlmr_base |  | 7 | r1.0 | B0 | B3 | 1080 | 0.3352 | 0.1972 | -0.138 | 40 | 189 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | r1.0 | B0 | B4 | 1098 | 0.3424 | 0.1758 | -0.1667 | 23 | 206 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | r1.0 | B2 | B3 | 1082 | 0.3152 | 0.2043 | -0.1109 | 33 | 153 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | r1.0 | B2 | B4 | 1088 | 0.318 | 0.1774 | -0.1406 | 28 | 181 | 0.0 |
| textfooler | reviews | xlmr_base |  | 7 | r1.0 | B3 | B4 | 1087 | 0.2042 | 0.1748 | -0.0294 | 56 | 88 | 0.0095 |
| textfooler | unlp | xlmr_base | wsd035 | 1914 |  | B0 | B2 | 287 | 0.3031 | 0.2648 | -0.0383 | 9 | 20 | 0.0614 |
| textfooler | unlp | xlmr_base | wsd035 | 1914 |  | B0 | B3 | 288 | 0.3056 | 0.3021 | -0.0035 | 23 | 24 | 1.0 |
| textfooler | unlp | xlmr_base | wsd035 | 1914 |  | B0 | B4 | 296 | 0.3041 | 0.277 | -0.027 | 14 | 22 | 0.243 |
| textfooler | unlp | xlmr_base | wsd035 | 1914 |  | B2 | B3 | 291 | 0.2887 | 0.3299 | 0.0412 | 29 | 17 | 0.1038 |
| textfooler | unlp | xlmr_base | wsd035 | 1914 |  | B2 | B4 | 296 | 0.2872 | 0.2838 | -0.0034 | 13 | 14 | 1.0 |
| textfooler | unlp | xlmr_base | wsd035 | 1914 |  | B3 | B4 | 300 | 0.3267 | 0.2933 | -0.0333 | 17 | 27 | 0.1742 |
| textfooler | unlp | xlmr_base | wsd035 | 2024 |  | B0 | B2 | 309 | 0.3139 | 0.2265 | -0.0874 | 11 | 38 | 0.0001 |
| textfooler | unlp | xlmr_base | wsd035 | 2024 |  | B0 | B3 | 265 | 0.3472 | 0.2075 | -0.1396 | 31 | 68 | 0.0003 |
| textfooler | unlp | xlmr_base | wsd035 | 2024 |  | B0 | B4 | 295 | 0.3254 | 0.3424 | 0.0169 | 22 | 17 | 0.5224 |
| textfooler | unlp | xlmr_base | wsd035 | 2024 |  | B2 | B3 | 258 | 0.2287 | 0.1938 | -0.0349 | 33 | 42 | 0.3557 |
| textfooler | unlp | xlmr_base | wsd035 | 2024 |  | B2 | B4 | 285 | 0.214 | 0.3193 | 0.1053 | 41 | 11 | 0.0 |
| textfooler | unlp | xlmr_base | wsd035 | 2024 |  | B3 | B4 | 270 | 0.2259 | 0.363 | 0.137 | 62 | 25 | 0.0001 |
| textfooler | unlp | xlmr_base | wsd035 | 7 |  | B0 | B2 | 292 | 0.2877 | 0.2466 | -0.0411 | 22 | 34 | 0.1409 |
| textfooler | unlp | xlmr_base | wsd035 | 7 |  | B0 | B3 | 303 | 0.2937 | 0.3102 | 0.0165 | 21 | 16 | 0.5114 |
| textfooler | unlp | xlmr_base | wsd035 | 7 |  | B0 | B4 | 301 | 0.2791 | 0.2625 | -0.0166 | 17 | 22 | 0.5224 |
| textfooler | unlp | xlmr_base | wsd035 | 7 |  | B2 | B3 | 299 | 0.2575 | 0.2977 | 0.0401 | 30 | 18 | 0.1114 |
| textfooler | unlp | xlmr_base | wsd035 | 7 |  | B2 | B4 | 289 | 0.2353 | 0.2595 | 0.0242 | 30 | 23 | 0.4101 |
| textfooler | unlp | xlmr_base | wsd035 | 7 |  | B3 | B4 | 302 | 0.3013 | 0.2715 | -0.0298 | 15 | 24 | 0.1996 |
| textfooler | unlp | xlmr_base |  | 1914 |  | B0 | B2 | 287 | 0.3206 | 0.2857 | -0.0348 | 12 | 22 | 0.1214 |
| textfooler | unlp | xlmr_base |  | 1914 |  | B0 | B3 | 288 | 0.3264 | 0.3229 | -0.0035 | 21 | 22 | 1.0 |
| textfooler | unlp | xlmr_base |  | 1914 |  | B0 | B4 | 296 | 0.3243 | 0.3041 | -0.0203 | 15 | 21 | 0.405 |
| textfooler | unlp | xlmr_base |  | 1914 |  | B2 | B3 | 291 | 0.3093 | 0.354 | 0.0447 | 25 | 12 | 0.047 |
| textfooler | unlp | xlmr_base |  | 1914 |  | B2 | B4 | 296 | 0.3074 | 0.3108 | 0.0034 | 17 | 16 | 1.0 |
| textfooler | unlp | xlmr_base |  | 1914 |  | B3 | B4 | 300 | 0.35 | 0.32 | -0.03 | 18 | 27 | 0.2327 |
| textfooler | unlp | xlmr_base |  | 2024 |  | B0 | B2 | 309 | 0.3139 | 0.2395 | -0.0744 | 12 | 35 | 0.0011 |
| textfooler | unlp | xlmr_base |  | 2024 |  | B0 | B3 | 265 | 0.3509 | 0.2189 | -0.1321 | 31 | 66 | 0.0005 |
| textfooler | unlp | xlmr_base |  | 2024 |  | B0 | B4 | 295 | 0.3288 | 0.3559 | 0.0271 | 23 | 15 | 0.2559 |
| textfooler | unlp | xlmr_base |  | 2024 |  | B2 | B3 | 258 | 0.2403 | 0.2054 | -0.0349 | 34 | 43 | 0.362 |
| textfooler | unlp | xlmr_base |  | 2024 |  | B2 | B4 | 285 | 0.2281 | 0.3368 | 0.1088 | 43 | 12 | 0.0 |
| textfooler | unlp | xlmr_base |  | 2024 |  | B3 | B4 | 270 | 0.237 | 0.3778 | 0.1407 | 64 | 26 | 0.0001 |
| textfooler | unlp | xlmr_base |  | 7 |  | B0 | B2 | 292 | 0.3082 | 0.274 | -0.0342 | 19 | 29 | 0.1934 |
| textfooler | unlp | xlmr_base |  | 7 |  | B0 | B3 | 303 | 0.3135 | 0.33 | 0.0165 | 22 | 17 | 0.5224 |
| textfooler | unlp | xlmr_base |  | 7 |  | B0 | B4 | 301 | 0.299 | 0.2691 | -0.0299 | 17 | 26 | 0.2221 |
| textfooler | unlp | xlmr_base |  | 7 |  | B2 | B3 | 299 | 0.2876 | 0.3144 | 0.0268 | 27 | 19 | 0.302 |
| textfooler | unlp | xlmr_base |  | 7 |  | B2 | B4 | 289 | 0.2664 | 0.2664 | 0.0 | 23 | 23 | 1.0 |
| textfooler | unlp | xlmr_base |  | 7 |  | B3 | B4 | 302 | 0.3212 | 0.2781 | -0.043 | 14 | 27 | 0.0596 |
