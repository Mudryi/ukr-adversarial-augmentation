# Stage-A pilot, archived 2026-09-13

The original pilot's attack cells, evaluated on **400** test examples. Archived when
the campaign standardised on 1500 examples, so that `results/{textfooler,bert_attack}/`
holds one homogeneous grid and the resumability check in `run_pilot.py` does not treat
these smaller cells as already-done work.

Nothing here is deleted or superseded -- the campaign's seed-1914 cells are a strict
superset in eval size, but these are the numbers quoted in RESEARCH_PLAN.md's
"Stage-A results" section. Re-aggregate them with:

    python scripts/aggregate_results.py --root results/archive/stageA_pilot_n400 \
        --out results/archive/stageA_pilot_n400/metrics

The matching checkpoints and augmented data live in `results/pilot_seed1914/` (renamed
from `results/pilot/`), which the campaign reuses rather than regenerating.
