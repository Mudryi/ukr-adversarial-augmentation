# Baseline / augmentation metrics (macro-F1, cASR, flip-rate)

Derived from `examples.jsonl` per-row data; not present in `ukr-synonym-robustness/src/evaluation/metrics.py`'s `Summary`.

| attack | dataset | model | condition | wsd | n_total | clean_accuracy | clean_macro_f1 | adv_accuracy | adv_macro_f1 | delta | cASR | flip_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| textfooler | reviews | xlmr_base | B0 |  | 400 | 0.74 | 0.3668 | 0.45 | 0.2071 | 0.29 | 0.3919 | 0.29 |
| textfooler | reviews | xlmr_base | B0 | wsd035 | 400 | 0.74 | 0.3668 | 0.455 | 0.2135 | 0.285 | 0.3851 | 0.285 |
| textfooler | reviews | xlmr_base | B1 |  | 400 | 0.72 | 0.4338 | 0.39 | 0.1836 | 0.33 | 0.4583 | 0.33 |
| textfooler | reviews | xlmr_base | B1 | wsd035 | 400 | 0.72 | 0.4338 | 0.41 | 0.2028 | 0.31 | 0.4306 | 0.31 |
| textfooler | reviews | xlmr_base | B2 |  | 400 | 0.7375 | 0.4276 | 0.4575 | 0.1952 | 0.28 | 0.3797 | 0.28 |
| textfooler | reviews | xlmr_base | B2 | wsd035 | 400 | 0.7375 | 0.4276 | 0.4875 | 0.2041 | 0.25 | 0.339 | 0.25 |
| textfooler | reviews | xlmr_base | B3 |  | 400 | 0.73 | 0.4354 | 0.525 | 0.2659 | 0.205 | 0.2808 | 0.205 |
| textfooler | reviews | xlmr_base | B3 | wsd035 | 400 | 0.73 | 0.4354 | 0.545 | 0.2628 | 0.185 | 0.2534 | 0.185 |
| textfooler | reviews | xlmr_base | B4 |  | 400 | 0.7275 | 0.4219 | 0.51 | 0.2144 | 0.2175 | 0.299 | 0.2175 |
| textfooler | reviews | xlmr_base | B4 | wsd035 | 400 | 0.7275 | 0.4219 | 0.5225 | 0.216 | 0.205 | 0.2818 | 0.205 |
| bert_attack | reviews | xlmr_base | B0 |  | 400 | 0.74 | 0.3668 | 0.6475 | 0.2728 | 0.0925 | 0.125 | 0.0925 |
| bert_attack | reviews | xlmr_base | B1 |  | 400 | 0.72 | 0.4338 | 0.57 | 0.2514 | 0.15 | 0.2083 | 0.15 |
| bert_attack | reviews | xlmr_base | B2 |  | 400 | 0.7375 | 0.4276 | 0.6325 | 0.2681 | 0.105 | 0.1424 | 0.105 |
| bert_attack | reviews | xlmr_base | B3 |  | 400 | 0.73 | 0.4354 | 0.6225 | 0.2908 | 0.1075 | 0.1473 | 0.1075 |
| bert_attack | reviews | xlmr_base | B4 |  | 400 | 0.7275 | 0.4219 | 0.6225 | 0.2749 | 0.105 | 0.1443 | 0.105 |

## Paired condition comparisons (McNemar exact)

Restricted to examples BOTH models classify correctly when clean. `casr_delta` < 0 means `condition` is MORE robust than `reference`; `p_value` is a two-sided exact test on the discordant pairs.

| attack | dataset | model | wsd | reference | condition | n_paired | reference_casr_paired | condition_casr_paired | casr_delta | b_worse | c_better | p_value |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bert_attack | reviews | xlmr_base |  | B0 | B1 | 274 | 0.0876 | 0.1788 | 0.0912 | 29 | 4 | 0.0 |
| bert_attack | reviews | xlmr_base |  | B0 | B2 | 278 | 0.0935 | 0.1007 | 0.0072 | 12 | 10 | 0.8318 |
| bert_attack | reviews | xlmr_base |  | B0 | B3 | 277 | 0.1011 | 0.1155 | 0.0144 | 15 | 11 | 0.5572 |
| bert_attack | reviews | xlmr_base |  | B0 | B4 | 279 | 0.0932 | 0.1183 | 0.0251 | 16 | 9 | 0.2295 |
| bert_attack | reviews | xlmr_base |  | B1 | B2 | 274 | 0.1788 | 0.1022 | -0.0766 | 5 | 26 | 0.0002 |
| bert_attack | reviews | xlmr_base |  | B1 | B3 | 273 | 0.1795 | 0.1172 | -0.0623 | 6 | 23 | 0.0023 |
| bert_attack | reviews | xlmr_base |  | B1 | B4 | 277 | 0.1841 | 0.13 | -0.0542 | 3 | 18 | 0.0015 |
| bert_attack | reviews | xlmr_base |  | B2 | B3 | 279 | 0.1075 | 0.129 | 0.0215 | 13 | 7 | 0.2632 |
| bert_attack | reviews | xlmr_base |  | B2 | B4 | 275 | 0.0945 | 0.12 | 0.0255 | 17 | 10 | 0.2478 |
| bert_attack | reviews | xlmr_base |  | B3 | B4 | 275 | 0.1127 | 0.1127 | 0.0 | 8 | 8 | 1.0 |
| textfooler | reviews | xlmr_base | wsd035 | B0 | B1 | 274 | 0.3577 | 0.4088 | 0.0511 | 42 | 28 | 0.1196 |
| textfooler | reviews | xlmr_base | wsd035 | B0 | B2 | 278 | 0.3669 | 0.3058 | -0.0612 | 16 | 33 | 0.0213 |
| textfooler | reviews | xlmr_base | wsd035 | B0 | B3 | 277 | 0.3682 | 0.231 | -0.1372 | 10 | 48 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | B0 | B4 | 279 | 0.3584 | 0.2545 | -0.1039 | 14 | 43 | 0.0002 |
| textfooler | reviews | xlmr_base | wsd035 | B1 | B2 | 274 | 0.4161 | 0.3066 | -0.1095 | 16 | 46 | 0.0002 |
| textfooler | reviews | xlmr_base | wsd035 | B1 | B3 | 273 | 0.4066 | 0.2271 | -0.1795 | 10 | 59 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | B1 | B4 | 277 | 0.4116 | 0.2563 | -0.1552 | 10 | 53 | 0.0 |
| textfooler | reviews | xlmr_base | wsd035 | B2 | B3 | 279 | 0.3118 | 0.233 | -0.0789 | 13 | 35 | 0.0021 |
| textfooler | reviews | xlmr_base | wsd035 | B2 | B4 | 275 | 0.3018 | 0.2509 | -0.0509 | 10 | 24 | 0.0243 |
| textfooler | reviews | xlmr_base | wsd035 | B3 | B4 | 275 | 0.2218 | 0.2509 | 0.0291 | 26 | 18 | 0.2912 |
| textfooler | reviews | xlmr_base |  | B0 | B1 | 274 | 0.365 | 0.4416 | 0.0766 | 41 | 20 | 0.0099 |
| textfooler | reviews | xlmr_base |  | B0 | B2 | 278 | 0.3705 | 0.3417 | -0.0288 | 24 | 32 | 0.3497 |
| textfooler | reviews | xlmr_base |  | B0 | B3 | 277 | 0.3718 | 0.2599 | -0.1119 | 13 | 44 | 0.0 |
| textfooler | reviews | xlmr_base |  | B0 | B4 | 279 | 0.3656 | 0.2724 | -0.0932 | 12 | 38 | 0.0003 |
| textfooler | reviews | xlmr_base |  | B1 | B2 | 274 | 0.4453 | 0.3504 | -0.0949 | 16 | 42 | 0.0009 |
| textfooler | reviews | xlmr_base |  | B1 | B3 | 273 | 0.4396 | 0.2564 | -0.1832 | 7 | 57 | 0.0 |
| textfooler | reviews | xlmr_base |  | B1 | B4 | 277 | 0.4404 | 0.278 | -0.1625 | 7 | 52 | 0.0 |
| textfooler | reviews | xlmr_base |  | B2 | B3 | 279 | 0.3584 | 0.2652 | -0.0932 | 13 | 39 | 0.0004 |
| textfooler | reviews | xlmr_base |  | B2 | B4 | 275 | 0.3455 | 0.2691 | -0.0764 | 12 | 33 | 0.0025 |
| textfooler | reviews | xlmr_base |  | B3 | B4 | 275 | 0.2545 | 0.2691 | 0.0145 | 26 | 22 | 0.6655 |
