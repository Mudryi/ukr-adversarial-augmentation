# Baseline / augmentation metrics (macro-F1, cASR, flip-rate)

Derived from `examples.jsonl` per-row data; not present in `ukr-synonym-robustness/src/evaluation/metrics.py`'s `Summary`.

| attack | dataset | model | condition | wsd | n_total | clean_accuracy | clean_macro_f1 | adv_accuracy | adv_macro_f1 | delta | cASR | flip_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| textfooler | news | sbert_mpnet | B0 |  | 10000 | 0.9368 | 0.9188 | 0.8318 | 0.7984 | 0.105 | 0.1121 | 0.105 |
| textfooler | news | sbert_mpnet | B0 | wsd035 | 10000 | 0.9368 | 0.9188 | 0.8411 | 0.8087 | 0.0957 | 0.1022 | 0.0957 |
| textfooler | news | ukr_roberta | B0 |  | 10000 | 0.9874 | 0.9816 | 0.9073 | 0.8987 | 0.0801 | 0.0811 | 0.0801 |
| textfooler | news | ukr_roberta | B0 | wsd035 | 10000 | 0.9874 | 0.9816 | 0.9159 | 0.9078 | 0.0715 | 0.0724 | 0.0715 |
| textfooler | news | xlmr_base | B0 |  | 10000 | 0.9363 | 0.9181 | 0.8355 | 0.8036 | 0.1008 | 0.1077 | 0.1008 |
| textfooler | news | xlmr_base | B0 | wsd035 | 10000 | 0.9363 | 0.9181 | 0.8444 | 0.8126 | 0.0919 | 0.0982 | 0.0919 |
| textfooler | reviews | sbert_mpnet | B0 |  | 9769 | 0.7758 | 0.4644 | 0.4968 | 0.2121 | 0.279 | 0.3597 | 0.279 |
| textfooler | reviews | sbert_mpnet | B0 | wsd035 | 9769 | 0.7758 | 0.4644 | 0.522 | 0.2242 | 0.2539 | 0.3272 | 0.2539 |
| textfooler | reviews | ukr_roberta | B0 |  | 9769 | 0.7628 | 0.4465 | 0.3719 | 0.1695 | 0.3909 | 0.5125 | 0.3909 |
| textfooler | reviews | ukr_roberta | B0 | wsd035 | 9769 | 0.7628 | 0.4465 | 0.4087 | 0.184 | 0.3541 | 0.4642 | 0.3541 |
| textfooler | reviews | xlmr_base | B0 |  | 9769 | 0.7791 | 0.4747 | 0.509 | 0.223 | 0.2701 | 0.3467 | 0.2701 |
| textfooler | reviews | xlmr_base | B0 | wsd035 | 9769 | 0.7791 | 0.4747 | 0.5411 | 0.2358 | 0.238 | 0.3055 | 0.238 |
| textfooler | unlp | sbert_mpnet | B0 |  | 382 | 0.8168 | 0.8088 | 0.4215 | 0.3616 | 0.3953 | 0.484 | 0.3953 |
| textfooler | unlp | sbert_mpnet | B0 | wsd035 | 382 | 0.8168 | 0.8088 | 0.4581 | 0.4062 | 0.3586 | 0.4391 | 0.3586 |
| textfooler | unlp | ukr_roberta | B0 |  | 382 | 0.8141 | 0.8045 | 0.4895 | 0.409 | 0.3246 | 0.3987 | 0.3246 |
| textfooler | unlp | ukr_roberta | B0 | wsd035 | 382 | 0.8141 | 0.8045 | 0.5 | 0.4211 | 0.3141 | 0.3859 | 0.3141 |
| textfooler | unlp | xlmr_base | B0 |  | 382 | 0.801 | 0.797 | 0.4974 | 0.4482 | 0.3037 | 0.3791 | 0.3037 |
| textfooler | unlp | xlmr_base | B0 | wsd035 | 382 | 0.801 | 0.797 | 0.5052 | 0.454 | 0.2958 | 0.3693 | 0.2958 |
| bert_attack | news | sbert_mpnet | B0 |  | 10000 | 0.9368 | 0.9188 | 0.7359 | 0.6982 | 0.2009 | 0.2145 | 0.2009 |
| bert_attack | news | ukr_roberta | B0 |  | 10000 | 0.9874 | 0.9816 | 0.8471 | 0.8463 | 0.1403 | 0.1421 | 0.1403 |
| bert_attack | news | xlmr_base | B0 |  | 10000 | 0.9363 | 0.9181 | 0.75 | 0.7132 | 0.1863 | 0.199 | 0.1863 |
| bert_attack | reviews | sbert_mpnet | B0 |  | 9769 | 0.7758 | 0.4644 | 0.6615 | 0.2861 | 0.1143 | 0.1474 | 0.1143 |
| bert_attack | reviews | ukr_roberta | B0 |  | 9769 | 0.7628 | 0.4465 | 0.6562 | 0.2811 | 0.1067 | 0.1398 | 0.1067 |
| bert_attack | reviews | xlmr_base | B0 |  | 9769 | 0.7791 | 0.4747 | 0.6809 | 0.3053 | 0.0982 | 0.126 | 0.0982 |
| bert_attack | unlp | sbert_mpnet | B0 |  | 382 | 0.8168 | 0.8088 | 0.6518 | 0.6427 | 0.1649 | 0.2019 | 0.1649 |
| bert_attack | unlp | ukr_roberta | B0 |  | 382 | 0.8141 | 0.8045 | 0.6963 | 0.6831 | 0.1178 | 0.1447 | 0.1178 |
| bert_attack | unlp | xlmr_base | B0 |  | 382 | 0.801 | 0.797 | 0.6859 | 0.6816 | 0.1152 | 0.1438 | 0.1152 |
