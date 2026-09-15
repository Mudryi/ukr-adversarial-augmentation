# Baseline / augmentation metrics (macro-F1, cASR, flip-rate)

Derived from `examples.jsonl` per-row data; not present in `ukr-synonym-robustness/src/evaluation/metrics.py`'s `Summary`.

| attack | dataset | model | condition | seed | variant | wsd | n_total | clean_accuracy | clean_macro_f1 | adv_accuracy | adv_macro_f1 | delta | cASR | flip_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| textfooler | reviews | xlmr_base | B0 | 1914 |  |  | 1500 | 0.768 | 0.4371 | 0.4653 | 0.216 | 0.3027 | 0.3941 | 0.3027 |
| textfooler | reviews | xlmr_base | B0 | 1914 |  | wsd035 | 1500 | 0.768 | 0.4371 | 0.484 | 0.2293 | 0.284 | 0.3698 | 0.284 |
| textfooler | reviews | xlmr_base | B0 | 2024 |  |  | 1500 | 0.7627 | 0.4656 | 0.4547 | 0.2184 | 0.308 | 0.4038 | 0.308 |
| textfooler | reviews | xlmr_base | B0 | 2024 |  | wsd035 | 1500 | 0.7627 | 0.4656 | 0.4687 | 0.2208 | 0.294 | 0.3855 | 0.294 |
| textfooler | reviews | xlmr_base | B0 | 7 |  |  | 1500 | 0.77 | 0.4443 | 0.4907 | 0.2079 | 0.2793 | 0.3628 | 0.2793 |
| textfooler | reviews | xlmr_base | B0 | 7 |  | wsd035 | 1500 | 0.77 | 0.4443 | 0.5147 | 0.2157 | 0.2553 | 0.3316 | 0.2553 |
| textfooler | reviews | xlmr_base | B1 | 1914 |  |  | 1500 | 0.748 | 0.4755 | 0.4253 | 0.2168 | 0.3227 | 0.4314 | 0.3227 |
| textfooler | reviews | xlmr_base | B1 | 1914 |  | wsd035 | 1500 | 0.748 | 0.4755 | 0.4487 | 0.2332 | 0.2993 | 0.4002 | 0.2993 |
| textfooler | reviews | xlmr_base | B1 | 2024 |  |  | 1500 | 0.77 | 0.4766 | 0.5067 | 0.2109 | 0.2633 | 0.342 | 0.2633 |
| textfooler | reviews | xlmr_base | B1 | 2024 |  | wsd035 | 1500 | 0.77 | 0.4766 | 0.524 | 0.224 | 0.246 | 0.3195 | 0.246 |
| textfooler | reviews | xlmr_base | B1 | 7 |  |  | 1500 | 0.7653 | 0.484 | 0.4587 | 0.2055 | 0.3067 | 0.4007 | 0.3067 |
| textfooler | reviews | xlmr_base | B1 | 7 |  | wsd035 | 1500 | 0.7653 | 0.484 | 0.4807 | 0.2231 | 0.2847 | 0.372 | 0.2847 |
| textfooler | reviews | xlmr_base | B2 | 1914 |  |  | 1500 | 0.7607 | 0.4829 | 0.4687 | 0.1992 | 0.292 | 0.3839 | 0.292 |
| textfooler | reviews | xlmr_base | B2 | 1914 | r0.25 |  | 1500 | 0.7647 | 0.4495 | 0.4973 | 0.2284 | 0.2673 | 0.3496 | 0.2673 |
| textfooler | reviews | xlmr_base | B2 | 1914 | r0.25 | wsd035 | 1500 | 0.7647 | 0.4495 | 0.512 | 0.2355 | 0.2527 | 0.3304 | 0.2527 |
| textfooler | reviews | xlmr_base | B2 | 1914 | r1.0 |  | 1500 | 0.744 | 0.4489 | 0.504 | 0.221 | 0.24 | 0.3226 | 0.24 |
| textfooler | reviews | xlmr_base | B2 | 1914 | r1.0 | wsd035 | 1500 | 0.744 | 0.4489 | 0.5173 | 0.2234 | 0.2267 | 0.3047 | 0.2267 |
| textfooler | reviews | xlmr_base | B2 | 1914 |  | wsd035 | 1500 | 0.7607 | 0.4829 | 0.4893 | 0.2076 | 0.2713 | 0.3567 | 0.2713 |
| textfooler | reviews | xlmr_base | B2 | 2024 |  |  | 1500 | 0.7753 | 0.4953 | 0.506 | 0.2244 | 0.2693 | 0.3474 | 0.2693 |
| textfooler | reviews | xlmr_base | B2 | 2024 |  | wsd035 | 1500 | 0.7753 | 0.4953 | 0.5293 | 0.2349 | 0.246 | 0.3173 | 0.246 |
| textfooler | reviews | xlmr_base | B2 | 7 |  |  | 1500 | 0.772 | 0.5034 | 0.4993 | 0.2171 | 0.2727 | 0.3532 | 0.2727 |
| textfooler | reviews | xlmr_base | B2 | 7 |  | wsd035 | 1500 | 0.772 | 0.5034 | 0.5213 | 0.2293 | 0.2507 | 0.3247 | 0.2507 |
| textfooler | reviews | xlmr_base | B3 | 1914 |  |  | 1500 | 0.762 | 0.5064 | 0.5307 | 0.2563 | 0.2313 | 0.3036 | 0.2313 |
| textfooler | reviews | xlmr_base | B3 | 1914 | pool10x20 |  | 1500 | 0.748 | 0.4706 | 0.4427 | 0.2429 | 0.3053 | 0.4082 | 0.3053 |
| textfooler | reviews | xlmr_base | B3 | 1914 | pool10x20 | wsd035 | 1500 | 0.748 | 0.4706 | 0.4427 | 0.2409 | 0.3053 | 0.4082 | 0.3053 |
| textfooler | reviews | xlmr_base | B3 | 1914 | r0.25 |  | 1500 | 0.7653 | 0.467 | 0.562 | 0.2327 | 0.2033 | 0.2657 | 0.2033 |
| textfooler | reviews | xlmr_base | B3 | 1914 | r0.25 | wsd035 | 1500 | 0.7653 | 0.467 | 0.57 | 0.2406 | 0.1953 | 0.2552 | 0.1953 |
| textfooler | reviews | xlmr_base | B3 | 1914 | r1.0 |  | 1500 | 0.7727 | 0.4775 | 0.6007 | 0.2425 | 0.172 | 0.2226 | 0.172 |
| textfooler | reviews | xlmr_base | B3 | 1914 | r1.0 | wsd035 | 1500 | 0.7727 | 0.4775 | 0.6093 | 0.2487 | 0.1633 | 0.2114 | 0.1633 |
| textfooler | reviews | xlmr_base | B3 | 1914 |  | wsd035 | 1500 | 0.762 | 0.5064 | 0.538 | 0.255 | 0.224 | 0.294 | 0.224 |
| textfooler | reviews | xlmr_base | B3 | 2024 |  |  | 1500 | 0.772 | 0.4701 | 0.5907 | 0.2507 | 0.1813 | 0.2349 | 0.1813 |
| textfooler | reviews | xlmr_base | B3 | 2024 |  | wsd035 | 1500 | 0.772 | 0.4701 | 0.5993 | 0.2594 | 0.1727 | 0.2237 | 0.1727 |
| textfooler | reviews | xlmr_base | B3 | 7 |  |  | 1500 | 0.7627 | 0.4745 | 0.4673 | 0.2242 | 0.2953 | 0.3872 | 0.2953 |
| textfooler | reviews | xlmr_base | B3 | 7 |  | wsd035 | 1500 | 0.7627 | 0.4745 | 0.48 | 0.2215 | 0.2827 | 0.3706 | 0.2827 |
| textfooler | reviews | xlmr_base | B4 | 1914 |  |  | 1500 | 0.7613 | 0.4862 | 0.53 | 0.2529 | 0.2313 | 0.3039 | 0.2313 |
| textfooler | reviews | xlmr_base | B4 | 1914 | pool10x20 |  | 1500 | 0.7493 | 0.4308 | 0.4893 | 0.2419 | 0.26 | 0.347 | 0.26 |
| textfooler | reviews | xlmr_base | B4 | 1914 | pool10x20 | wsd035 | 1500 | 0.7493 | 0.4308 | 0.496 | 0.2367 | 0.2533 | 0.3381 | 0.2533 |
| textfooler | reviews | xlmr_base | B4 | 1914 | r0.25 |  | 1500 | 0.7613 | 0.4562 | 0.5487 | 0.242 | 0.2127 | 0.2793 | 0.2127 |
| textfooler | reviews | xlmr_base | B4 | 1914 | r0.25 | wsd035 | 1500 | 0.7613 | 0.4562 | 0.5607 | 0.2395 | 0.2007 | 0.2636 | 0.2007 |
| textfooler | reviews | xlmr_base | B4 | 1914 | r1.0 |  | 1500 | 0.75 | 0.4601 | 0.562 | 0.2499 | 0.188 | 0.2507 | 0.188 |
| textfooler | reviews | xlmr_base | B4 | 1914 | r1.0 | wsd035 | 1500 | 0.75 | 0.4601 | 0.572 | 0.2533 | 0.178 | 0.2373 | 0.178 |
| textfooler | reviews | xlmr_base | B4 | 1914 |  | wsd035 | 1500 | 0.7613 | 0.4862 | 0.5487 | 0.2578 | 0.2127 | 0.2793 | 0.2127 |
| textfooler | reviews | xlmr_base | B4 | 2024 |  |  | 1500 | 0.778 | 0.4925 | 0.5573 | 0.2325 | 0.2207 | 0.2836 | 0.2207 |
| textfooler | reviews | xlmr_base | B4 | 2024 |  | wsd035 | 1500 | 0.778 | 0.4925 | 0.58 | 0.2418 | 0.198 | 0.2545 | 0.198 |
| textfooler | reviews | xlmr_base | B4 | 7 |  |  | 1500 | 0.766 | 0.4689 | 0.5347 | 0.2374 | 0.2313 | 0.302 | 0.2313 |
| textfooler | reviews | xlmr_base | B4 | 7 |  | wsd035 | 1500 | 0.766 | 0.4689 | 0.546 | 0.244 | 0.22 | 0.2872 | 0.22 |
| textfooler | reviews | xlmr_base | B5 | 1914 |  |  | 1500 | 0.7487 | 0.4682 | 0.2987 | 0.1732 | 0.45 | 0.6011 | 0.45 |
| textfooler | reviews | xlmr_base | B5 | 1914 | pool10x20 |  | 1500 | 0.7547 | 0.4948 | 0.284 | 0.1741 | 0.4707 | 0.6237 | 0.4707 |
| textfooler | reviews | xlmr_base | B5 | 1914 | pool10x20 | wsd035 | 1500 | 0.7547 | 0.4948 | 0.2953 | 0.1783 | 0.4593 | 0.6087 | 0.4593 |
| textfooler | reviews | xlmr_base | B5 | 1914 |  | wsd035 | 1500 | 0.7487 | 0.4682 | 0.3307 | 0.1867 | 0.418 | 0.5583 | 0.418 |
| textfooler | reviews | xlmr_base | B5 | 2024 |  |  | 1500 | 0.7747 | 0.4895 | 0.376 | 0.1895 | 0.3987 | 0.5146 | 0.3987 |
| textfooler | reviews | xlmr_base | B5 | 2024 |  | wsd035 | 1500 | 0.7747 | 0.4895 | 0.4033 | 0.1975 | 0.3713 | 0.4793 | 0.3713 |
| textfooler | reviews | xlmr_base | B5 | 7 |  |  | 1500 | 0.7627 | 0.4825 | 0.3613 | 0.1889 | 0.4013 | 0.5262 | 0.4013 |
| textfooler | reviews | xlmr_base | B5 | 7 |  | wsd035 | 1500 | 0.7627 | 0.4825 | 0.374 | 0.1957 | 0.3887 | 0.5096 | 0.3887 |
| textfooler | reviews | xlmr_base | B6 | 1914 |  |  | 1500 | 0.7653 | 0.4927 | 0.452 | 0.2008 | 0.3133 | 0.4094 | 0.3133 |
| textfooler | reviews | xlmr_base | B6 | 1914 |  | wsd035 | 1500 | 0.7653 | 0.4927 | 0.476 | 0.2069 | 0.2893 | 0.378 | 0.2893 |
| textfooler | reviews | xlmr_base | B6 | 2024 |  |  | 1500 | 0.7687 | 0.4891 | 0.446 | 0.1886 | 0.3227 | 0.4198 | 0.3227 |
| textfooler | reviews | xlmr_base | B6 | 2024 |  | wsd035 | 1500 | 0.7687 | 0.4891 | 0.462 | 0.1983 | 0.3067 | 0.399 | 0.3067 |
| textfooler | reviews | xlmr_base | B6 | 7 |  |  | 1500 | 0.7653 | 0.4818 | 0.4387 | 0.1988 | 0.3267 | 0.4268 | 0.3267 |
| textfooler | reviews | xlmr_base | B6 | 7 |  | wsd035 | 1500 | 0.7653 | 0.4818 | 0.4613 | 0.2046 | 0.304 | 0.3972 | 0.304 |
| textfooler | reviews | xlmr_base | B7 | 1914 |  |  | 1500 | 0.7613 | 0.4638 | 0.456 | 0.2074 | 0.3053 | 0.4011 | 0.3053 |
| textfooler | reviews | xlmr_base | B7 | 1914 |  | wsd035 | 1500 | 0.7613 | 0.4638 | 0.488 | 0.217 | 0.2733 | 0.359 | 0.2733 |
| textfooler | reviews | xlmr_base | B7 | 2024 |  |  | 1500 | 0.762 | 0.4719 | 0.4413 | 0.2081 | 0.3207 | 0.4208 | 0.3207 |
| textfooler | reviews | xlmr_base | B7 | 2024 |  | wsd035 | 1500 | 0.762 | 0.4719 | 0.47 | 0.2201 | 0.292 | 0.3832 | 0.292 |
| textfooler | reviews | xlmr_base | B7 | 7 |  |  | 1500 | 0.762 | 0.4463 | 0.496 | 0.2038 | 0.266 | 0.3491 | 0.266 |
| textfooler | reviews | xlmr_base | B7 | 7 |  | wsd035 | 1500 | 0.762 | 0.4463 | 0.516 | 0.2117 | 0.246 | 0.3228 | 0.246 |
| bert_attack | reviews | xlmr_base | B0 | 1914 |  |  | 1500 | 0.768 | 0.4371 | 0.6587 | 0.2917 | 0.1093 | 0.1424 | 0.1093 |
| bert_attack | reviews | xlmr_base | B0 | 2024 |  |  | 1500 | 0.7627 | 0.4656 | 0.6473 | 0.2894 | 0.1153 | 0.1512 | 0.1153 |
| bert_attack | reviews | xlmr_base | B0 | 7 |  |  | 1500 | 0.77 | 0.4443 | 0.6727 | 0.3035 | 0.0973 | 0.1264 | 0.0973 |
| bert_attack | reviews | xlmr_base | B1 | 1914 |  |  | 1500 | 0.748 | 0.4755 | 0.5987 | 0.2883 | 0.1493 | 0.1996 | 0.1493 |
| bert_attack | reviews | xlmr_base | B1 | 2024 |  |  | 1500 | 0.77 | 0.4766 | 0.6467 | 0.2818 | 0.1233 | 0.1602 | 0.1233 |
| bert_attack | reviews | xlmr_base | B1 | 7 |  |  | 1500 | 0.7653 | 0.484 | 0.6473 | 0.2933 | 0.118 | 0.1542 | 0.118 |
| bert_attack | reviews | xlmr_base | B2 | 1914 |  |  | 1500 | 0.7607 | 0.4829 | 0.6307 | 0.2829 | 0.13 | 0.1709 | 0.13 |
| bert_attack | reviews | xlmr_base | B2 | 1914 | r0.25 |  | 1500 | 0.7647 | 0.4495 | 0.638 | 0.2809 | 0.1267 | 0.1656 | 0.1267 |
| bert_attack | reviews | xlmr_base | B2 | 1914 | r1.0 |  | 1500 | 0.744 | 0.4489 | 0.6173 | 0.2745 | 0.1267 | 0.1703 | 0.1267 |
| bert_attack | reviews | xlmr_base | B2 | 2024 |  |  | 1500 | 0.7753 | 0.4953 | 0.6513 | 0.2994 | 0.124 | 0.1599 | 0.124 |
| bert_attack | reviews | xlmr_base | B2 | 7 |  |  | 1500 | 0.772 | 0.5034 | 0.6427 | 0.295 | 0.1293 | 0.1675 | 0.1293 |
| bert_attack | reviews | xlmr_base | B3 | 1914 |  |  | 1500 | 0.762 | 0.5064 | 0.6307 | 0.3096 | 0.1313 | 0.1724 | 0.1313 |
| bert_attack | reviews | xlmr_base | B3 | 1914 | pool10x20 |  | 1500 | 0.748 | 0.4706 | 0.6293 | 0.2951 | 0.1187 | 0.1586 | 0.1187 |
| bert_attack | reviews | xlmr_base | B3 | 1914 | r0.25 |  | 1500 | 0.7653 | 0.467 | 0.67 | 0.3231 | 0.0953 | 0.1246 | 0.0953 |
| bert_attack | reviews | xlmr_base | B3 | 1914 | r1.0 |  | 1500 | 0.7727 | 0.4775 | 0.676 | 0.3037 | 0.0967 | 0.1251 | 0.0967 |
| bert_attack | reviews | xlmr_base | B3 | 2024 |  |  | 1500 | 0.772 | 0.4701 | 0.6507 | 0.2884 | 0.1213 | 0.1572 | 0.1213 |
| bert_attack | reviews | xlmr_base | B3 | 7 |  |  | 1500 | 0.7627 | 0.4745 | 0.6487 | 0.2885 | 0.114 | 0.1495 | 0.114 |
| bert_attack | reviews | xlmr_base | B4 | 1914 |  |  | 1500 | 0.7613 | 0.4862 | 0.6373 | 0.3038 | 0.124 | 0.1629 | 0.124 |
| bert_attack | reviews | xlmr_base | B4 | 1914 | pool10x20 |  | 1500 | 0.7493 | 0.4308 | 0.6407 | 0.3037 | 0.1087 | 0.145 | 0.1087 |
| bert_attack | reviews | xlmr_base | B4 | 1914 | r0.25 |  | 1500 | 0.7613 | 0.4562 | 0.638 | 0.2859 | 0.1233 | 0.162 | 0.1233 |
| bert_attack | reviews | xlmr_base | B4 | 1914 | r1.0 |  | 1500 | 0.75 | 0.4601 | 0.644 | 0.2976 | 0.106 | 0.1413 | 0.106 |
| bert_attack | reviews | xlmr_base | B4 | 2024 |  |  | 1500 | 0.778 | 0.4925 | 0.662 | 0.2841 | 0.116 | 0.1491 | 0.116 |
| bert_attack | reviews | xlmr_base | B4 | 7 |  |  | 1500 | 0.766 | 0.4689 | 0.6487 | 0.2991 | 0.1173 | 0.1532 | 0.1173 |
| bert_attack | reviews | xlmr_base | B5 | 1914 |  |  | 1500 | 0.7487 | 0.4682 | 0.5827 | 0.2932 | 0.166 | 0.2217 | 0.166 |
| bert_attack | reviews | xlmr_base | B5 | 1914 | pool10x20 |  | 1500 | 0.7547 | 0.4948 | 0.5793 | 0.2779 | 0.1753 | 0.2323 | 0.1753 |
| bert_attack | reviews | xlmr_base | B5 | 2024 |  |  | 1500 | 0.7747 | 0.4895 | 0.6373 | 0.2849 | 0.1373 | 0.1773 | 0.1373 |
| bert_attack | reviews | xlmr_base | B5 | 7 |  |  | 1500 | 0.7627 | 0.4825 | 0.6133 | 0.2774 | 0.1493 | 0.1958 | 0.1493 |
| bert_attack | reviews | xlmr_base | B6 | 1914 |  |  | 1500 | 0.7653 | 0.4927 | 0.64 | 0.2994 | 0.1253 | 0.1638 | 0.1253 |
| bert_attack | reviews | xlmr_base | B6 | 2024 |  |  | 1500 | 0.7687 | 0.4891 | 0.664 | 0.301 | 0.1047 | 0.1362 | 0.1047 |
| bert_attack | reviews | xlmr_base | B6 | 7 |  |  | 1500 | 0.7653 | 0.4818 | 0.6453 | 0.294 | 0.12 | 0.1568 | 0.12 |
| bert_attack | reviews | xlmr_base | B7 | 1914 |  |  | 1500 | 0.7613 | 0.4638 | 0.6593 | 0.3028 | 0.102 | 0.134 | 0.102 |
| bert_attack | reviews | xlmr_base | B7 | 2024 |  |  | 1500 | 0.762 | 0.4719 | 0.6587 | 0.2982 | 0.1033 | 0.1356 | 0.1033 |
| bert_attack | reviews | xlmr_base | B7 | 7 |  |  | 1500 | 0.762 | 0.4463 | 0.6773 | 0.2868 | 0.0847 | 0.1111 | 0.0847 |

## Paired condition comparisons (McNemar exact), per seed

Restricted to examples BOTH models classify correctly when clean. `casr_delta` < 0 means `condition` is MORE robust than `reference`; `p_value` is a two-sided exact test on the discordant pairs. These capture EVALUATION sampling noise only -- not training-run variance, which is what the across-seed table below is for.

| attack | dataset | model | wsd | seed | variant | reference | condition | n_paired | reference_casr_paired | condition_casr_paired | casr_delta | b_worse | c_better | p_value |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
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
