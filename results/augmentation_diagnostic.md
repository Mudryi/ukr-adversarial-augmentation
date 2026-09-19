# Augmentation label-noise diagnostic

Rate of substitutions whose replacement is a known antonym of the original word, i.e. rows whose gold label is probably now wrong. A lower bound on semantic damage: only dictionary-known antonyms are detected.

| cell | strategy | n | n_antonym | antonym_rate |
|---|---|---|---|---|
| reviews__xlmr_base__seed1914__B2__r0.5__full78k | wsd_synonym | 39073 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B3__r0.5__full78k | adversarial_synonym | 39073 | 3 | 0.01% |
| reviews__xlmr_base__seed1914__B4__r0.5__full78k | wsd_adversarial_synonym | 39073 | 0 | 0.00% |
| news__xlmr_base__seed1914__B2__r0.5 | wsd_synonym | 10000 | 0 | 0.00% |
| news__xlmr_base__seed1914__B3__r0.5 | adversarial_synonym | 10000 | 0 | 0.00% |
| news__xlmr_base__seed1914__B4__r0.5 | wsd_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B1__r0.5 | random_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B2__r0.25__r0.25 | wsd_synonym | 5000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B2__r0.5 | wsd_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B2__r1.0__r1.0 | wsd_synonym | 18712 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B3__r0.25__r0.25 | adversarial_synonym | 5000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B3__r0.5 | adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B3__r0.5__pool10x20 | adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B3__r1.0__r1.0 | adversarial_synonym | 19447 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B4__r0.25__r0.25 | wsd_adversarial_synonym | 5000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B4__r0.5 | wsd_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B4__r0.5__pool10x20 | wsd_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B4__r1.0__r1.0 | wsd_adversarial_synonym | 18702 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B5__r0.5 | anti_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B5__r0.5__pool10x20 | anti_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed1914__B6__r0.5 | mlm_random | 10000 | 33 | 0.33% |
| reviews__xlmr_base__seed1914__B7__r0.5 | mlm_adversarial | 10000 | 35 | 0.35% |
| reviews__xlmr_base__seed2024__B1__r0.5 | random_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed2024__B2__r0.5 | wsd_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed2024__B3__r0.5 | adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed2024__B3__r0.5__pool10x20 | adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed2024__B4__r0.5 | wsd_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed2024__B4__r0.5__pool10x20 | wsd_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed2024__B5__r0.5 | anti_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed2024__B5__r0.5__pool10x20 | anti_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed2024__B6__r0.5 | mlm_random | 10000 | 30 | 0.30% |
| reviews__xlmr_base__seed2024__B7__r0.5 | mlm_adversarial | 10000 | 30 | 0.30% |
| reviews__xlmr_base__seed7__B1__r0.5 | random_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed7__B2__r0.5 | wsd_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed7__B3__r0.5 | adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed7__B3__r0.5__pool10x20 | adversarial_synonym | 10000 | 1 | 0.01% |
| reviews__xlmr_base__seed7__B4__r0.5 | wsd_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed7__B4__r0.5__pool10x20 | wsd_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed7__B5__r0.5 | anti_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed7__B5__r0.5__pool10x20 | anti_adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__xlmr_base__seed7__B6__r0.5 | mlm_random | 10000 | 28 | 0.28% |
| reviews__xlmr_base__seed7__B7__r0.5 | mlm_adversarial | 10000 | 26 | 0.26% |
| reviews__ukr_roberta__seed1914__B2__r0.5 | wsd_synonym | 10000 | 0 | 0.00% |
| reviews__ukr_roberta__seed1914__B3__r0.5 | adversarial_synonym | 10000 | 0 | 0.00% |
| reviews__ukr_roberta__seed1914__B4__r0.5 | wsd_adversarial_synonym | 10000 | 0 | 0.00% |
| unlp__xlmr_base__seed1914__B2__r0.5 | wsd_synonym | 1528 | 0 | 0.00% |
| unlp__xlmr_base__seed1914__B3__r0.5 | adversarial_synonym | 1528 | 0 | 0.00% |
| unlp__xlmr_base__seed1914__B4__r0.5 | wsd_adversarial_synonym | 1528 | 0 | 0.00% |
