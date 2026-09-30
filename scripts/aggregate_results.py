"""Aggregate per-example attack results (examples.jsonl) into macro-F1, cASR, and
flip-rate, which ukr-synonym-robustness/src/evaluation/metrics.py does not compute.

Also reuse ukr-synonym-robustness/src/evaluation/stats.py for Wilson CIs / paired
bootstrap across seeds.

Walks one or more result roots for `{textfooler,bert_attack}/<cell>/examples.jsonl`
and derives, per cell, everything needed for the RESEARCH_PLAN.md metrics table:

  - clean_accuracy, clean_macro_f1        (orig_label vs true_label)
  - adv_accuracy, adv_macro_f1            (adv_label vs true_label)
  - delta = clean_accuracy - adv_accuracy
  - cASR = P(adv_label != true_label | orig_label == true_label)
  - flip_rate = P(orig_label != adv_label)

Cell directory names are parsed as `<dataset>__<model>[__<condition>][__seed<seed>][__wsd035]`
(condition/seed are absent for the existing B0 cells produced by
ukr-synonym-robustness/scripts/run_paper_experiments.py; they appear once this project's
own evaluate_robustness.py starts writing cells for B1-B4).

Usage:
    python scripts/aggregate_results.py \
        --root ../ukr-synonym-robustness/results \
        --root results \
        --out results/baseline_metrics
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ukr-synonym-robustness"))
from src.evaluation.stats import mcnemar_exact, wilson_ci  # noqa: E402

CELL_RE = re.compile(
    r"^(?P<dataset>[^_]+)__(?P<model>[a-z0-9]+(?:_[a-z0-9]+)*?)"
    r"(?:__(?P<condition>B\d))?"
    r"(?:__seed(?P<seed>\d+))?"
    # Ablation tag written by run_pilot.py --variant (pool10x20, r0.25, full78k...).
    # The lookahead keeps it from swallowing the trailing __wsd035 marker.
    # single underscores only, so a trailing __wsd035 cannot be absorbed into it
    r"(?:__(?P<variant>(?!wsd\d)[a-z0-9][a-z0-9.]*(?:_[a-z0-9.]+)*))?"
    r"(?:__(?P<wsd>wsd\d+))?$"
)


def parse_cell_name(name: str) -> dict:
    m = CELL_RE.match(name)
    if not m:
        return {"dataset": None, "model": None, "condition": "B0", "seed": None,
                "variant": None, "wsd": None, "raw": name}
    d = m.groupdict()
    d["condition"] = d["condition"] or "B0"
    d["variant"] = d["variant"] or ""
    d["raw"] = name
    return d


def load_examples(path: Path) -> pd.DataFrame:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return pd.DataFrame(rows)


def prediction_spread(orig: pd.Series) -> dict:
    """How concentrated are the model's CLEAN predictions?

    cASR is conditioned on examples the model gets right when clean, and on an
    imbalanced dataset those are dominated by the majority class -- which is also the
    hardest class to flip away from. A model that has quietly stopped predicting its
    minority classes therefore scores a *better* cASR without being more robust. These
    columns make that failure visible next to every cASR number rather than leaving it
    to be discovered later.
    """
    counts = orig.value_counts()
    share = counts / len(orig)
    ent = float(-(share * np.log2(share)).sum())
    n_possible = max(int(orig.max()) + 1, len(counts))
    return {
        "majority_pred_share": float(share.max()),
        "n_classes_predicted": int(len(counts)),
        "pred_entropy": ent / np.log2(n_possible) if n_possible > 1 else 0.0,
    }


def compute_cell_metrics(df: pd.DataFrame) -> dict:
    true = df["true_label"]
    orig = df["orig_label"]
    adv = df["adv_label"]

    clean_acc = (true == orig).mean()
    adv_acc = (true == adv).mean()
    clean_f1 = f1_score(true, orig, average="macro")
    adv_f1 = f1_score(true, adv, average="macro")
    flip_rate = (orig != adv).mean()

    eligible = df[true == orig]
    n_eligible = len(eligible)
    casr = (eligible["adv_label"] != eligible["true_label"]).mean() if n_eligible else float("nan")
    n_fooled = int((eligible["adv_label"] != eligible["true_label"]).sum()) if n_eligible else 0
    casr_ci = wilson_ci(n_fooled, n_eligible) if n_eligible else None

    return {
        **prediction_spread(orig),
        "casr_ci_lo": casr_ci.lo if casr_ci else float("nan"),
        "casr_ci_hi": casr_ci.hi if casr_ci else float("nan"),
        "n_total": len(df),
        "n_conditional_eligible": n_eligible,
        "clean_accuracy": clean_acc,
        "clean_macro_f1": clean_f1,
        "adv_accuracy": adv_acc,
        "adv_macro_f1": adv_f1,
        "delta": clean_acc - adv_acc,
        "cASR": casr,
        "flip_rate": flip_rate,
    }


def paired_comparison(baseline_df: pd.DataFrame, cond_df: pd.DataFrame) -> dict | None:
    """Compare a condition against the baseline on the examples BOTH classify
    correctly when clean -- the only rows on which "was this attack successful"
    is defined for both models. Every condition attacks the same test examples,
    so this pairing is valid and far more sensitive than comparing two independent
    cASR intervals.

    McNemar's exact test on the discordant pairs:
      b = baseline resisted, condition was fooled   (condition is WORSE)
      c = baseline was fooled, condition resisted   (condition is BETTER)
    """
    merged = baseline_df.merge(cond_df, on="id", suffixes=("_base", "_cond"))
    both_clean_correct = merged[
        (merged["true_label_base"] == merged["orig_label_base"])
        & (merged["true_label_cond"] == merged["orig_label_cond"])
    ]
    n = len(both_clean_correct)
    if n == 0:
        return None

    base_fooled = both_clean_correct["adv_label_base"] != both_clean_correct["true_label_base"]
    cond_fooled = both_clean_correct["adv_label_cond"] != both_clean_correct["true_label_cond"]

    b = int((~base_fooled & cond_fooled).sum())
    c = int((base_fooled & ~cond_fooled).sum())
    test = mcnemar_exact(b, c)
    return {
        "n_paired": n,
        "baseline_casr_paired": float(base_fooled.mean()),
        "condition_casr_paired": float(cond_fooled.mean()),
        "casr_delta": float(cond_fooled.mean() - base_fooled.mean()),
        "b_worse": b,
        "c_better": c,
        "p_value": test["p_value"],
    }



def write_across_seed_tables(out_df: pd.DataFrame, paired_df: pd.DataFrame, path: Path) -> None:
    """Summarise across seeds -- the table that decides what can actually be claimed.

    Two things live here that the per-seed tables cannot show:

      * cASR per seed, with mean and range. If the seed-to-seed range is comparable to
        the gap between two conditions, that gap is not a result no matter how small
        its within-seed p-value was.
      * A pooled McNemar per condition pair, summing discordant counts over seeds.
        Pooling treats the seed as part of the method's randomness (each seed retrains
        every condition and regenerates its augmentation), which is the quantity of
        interest; it is not a substitute for a proper mixed model, so the per-seed
        consistency column is reported next to it.
    """
    lines = ["# Across-seed summary\n"]

    seeded = out_df[out_df["seed"].notna()].copy()
    if seeded.empty:
        path.write_text("\n".join(lines) + "\nNo seeded cells found.\n", encoding="utf-8")
        return

    lines.append("\n## cASR by seed (lower = more robust)\n")
    keys = ["attack", "dataset", "model", "wsd", "variant", "condition"]
    grouped = seeded.groupby(keys, dropna=False)["cASR"]
    rows = []
    for key, series in grouped:
        vals = [v for v in series.tolist() if pd.notna(v)]
        if not vals:
            continue
        rows.append({
            **dict(zip(keys, key)),
            "n_seeds": len(vals),
            "casr_mean": sum(vals) / len(vals),
            "casr_min": min(vals),
            "casr_max": max(vals),
            "casr_range": max(vals) - min(vals),
        })
    if rows:
        summary = pd.DataFrame(rows).sort_values(keys)
        scols = keys + ["n_seeds", "casr_mean", "casr_min", "casr_max", "casr_range"]
        lines.append("| " + " | ".join(scols) + " |")
        lines.append("|" + "|".join("---" for _ in scols) + "|")
        for row in summary[scols].round(4).itertuples(index=False, name=None):
            lines.append("| " + " | ".join(str(v) for v in row) + " |")
        single = summary[summary["n_seeds"] < 2]
        if not single.empty:
            lines.append(f"\n**{len(single)} of {len(summary)} cells have only one seed** -- "
                         "directional only, not claimable.")

    lines.append("\n\n## Pooled paired comparisons across seeds (McNemar exact)\n")
    lines.append("`n_seeds_agreeing` counts seeds whose casr_delta has the same sign as the "
                 "pooled delta -- 3/3 with a significant pooled p is a result; 2/3 is not.\n")
    pkeys = ["attack", "dataset", "model", "wsd", "variant", "reference", "condition"]
    prows = []
    for key, grp in paired_df.groupby(pkeys, dropna=False):
        b = int(grp["b_worse"].sum())
        c = int(grp["c_better"].sum())
        n = int(grp["n_paired"].sum())
        delta = float((grp["casr_delta"] * grp["n_paired"]).sum() / n) if n else float("nan")
        agree = int((grp["casr_delta"].apply(lambda d: (d < 0) == (delta < 0))).sum())
        prows.append({
            **dict(zip(pkeys, key)),
            "n_seeds": len(grp), "n_seeds_agreeing": agree, "n_paired": n,
            "casr_delta": delta, "b_worse": b, "c_better": c,
            "p_value": mcnemar(b, c),
        })
    if prows:
        pooled = pd.DataFrame(prows).sort_values(pkeys)
        cols = pkeys + ["n_seeds", "n_seeds_agreeing", "n_paired", "casr_delta",
                        "b_worse", "c_better", "p_value"]
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "|".join("---" for _ in cols) + "|")
        for row in pooled[cols].round(4).itertuples(index=False, name=None):
            lines.append("| " + " | ".join(str(v) for v in row) + " |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {path}")


def mcnemar(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value that also survives large discordant counts.

    ukr-synonym-robustness's `mcnemar_exact` sums binomial coefficients over 2**n, which
    overflows a float64 once b + c exceeds ~1023 -- reachable here as soon as discordant
    pairs are pooled across seeds. scipy's binomtest computes the same exact two-sided
    binomial test in log space, so it is used whenever it is available; the original is
    kept for small n so previously reported numbers stay reproducible.
    """
    n = b + c
    if n == 0:
        return 1.0
    if n <= 1000:
        return mcnemar_exact(b, c)["p_value"]
    from scipy import stats

    return float(stats.binomtest(min(b, c), n, 0.5).pvalue)


def flag_degeneracy(out_df: pd.DataFrame, tolerance: float = 0.02) -> pd.DataFrame:
    """Mark conditions whose eval-split macro-F1 fell materially below their own B0.

    A robustness gain bought by abandoning minority classes is not a robustness gain.
    The comparison is against the baseline that shares this cell's dataset/model/seed/
    variant -- falling back to the base-variant B0, which ablation runs borrow rather
    than retrain (see run_pilot.py --variant).
    """
    b0 = {(r.dataset, r.model, r.seed, r.variant): r.eval_macro_f1
          for r in out_df.itertuples()
          if r.condition == "B0" and pd.notna(r.eval_macro_f1)}
    flags = []
    for r in out_df.itertuples():
        base = b0.get((r.dataset, r.model, r.seed, r.variant))
        if base is None:
            base = b0.get((r.dataset, r.model, r.seed, ""))
        if r.condition == "B0" or base is None or pd.isna(r.eval_macro_f1):
            flags.append("")
        elif r.eval_macro_f1 < base - tolerance:
            flags.append(f"DEGENERACY_SUSPECT(-{base - r.eval_macro_f1:.3f})")
        else:
            flags.append("")
    out_df["degeneracy_flag"] = flags
    return out_df


def load_training_markers(roots: list[Path]) -> dict[str, float]:
    """checkpoint-dir name -> eval-split macro-F1 at checkpoint selection.

    The `clean_macro_f1` column in the per-cell table is computed on only the attacked
    subset (1500 rows), which is far noisier and, on an imbalanced set, not comparable
    across conditions. `train_augmented.py` records the full eval-split figure in each
    checkpoint's TRAINING_COMPLETE marker; that is the number to judge clean
    performance -- and degeneracy -- on.
    """
    markers: dict[str, float] = {}
    for root in roots:
        for marker in root.glob("*/checkpoints/*/TRAINING_COMPLETE"):
            try:
                markers[marker.parent.name] = float(json.loads(marker.read_text())["best_macro_f1"])
            except (ValueError, KeyError, json.JSONDecodeError):
                continue
    return markers


def find_cells(roots: list[Path]):
    for root in roots:
        for attack in ("textfooler", "bert_attack"):
            attack_dir = root / attack
            if not attack_dir.is_dir():
                continue
            for cell_dir in sorted(attack_dir.iterdir()):
                examples_path = cell_dir / "examples.jsonl"
                if examples_path.is_file():
                    yield attack, cell_dir.name, examples_path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root", action="append", dest="roots", required=True,
        help="A results/ directory containing {textfooler,bert_attack}/<cell>/examples.jsonl. "
             "Repeatable.",
    )
    p.add_argument("--out", default="results/baseline_metrics", help="Output path prefix (no extension).")
    args = p.parse_args(argv)

    roots = [Path(r) for r in args.roots]
    markers = load_training_markers(roots)
    records = []
    frames: dict[tuple, pd.DataFrame] = {}
    for attack, cell_name, examples_path in find_cells(roots):
        parsed = parse_cell_name(cell_name)
        df = load_examples(examples_path)
        if df.empty:
            print(f"[skip] empty {examples_path}")
            continue
        metrics = compute_cell_metrics(df)
        frames[(attack, parsed["dataset"], parsed["model"], parsed["wsd"],
                parsed["seed"], parsed["variant"], parsed["condition"])] = df
        ckpt_name = cell_name[: -len("__wsd035")] if cell_name.endswith("__wsd035") else cell_name
        records.append({"attack": attack, **parsed, **metrics,
                        "eval_macro_f1": markers.get(ckpt_name, float("nan")),
                        "source": str(examples_path)})
        print(f"[ok] {attack}/{cell_name}: n={metrics['n_total']} "
              f"clean_acc={metrics['clean_accuracy']:.3f} cASR={metrics['cASR']:.3f} "
              f"flip_rate={metrics['flip_rate']:.3f}")

    if not records:
        print("no cells found under: " + ", ".join(str(r) for r in roots))
        return

    out_df = flag_degeneracy(pd.DataFrame(records))
    out_csv = Path(args.out + ".csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out_csv, index=False)

    out_md = Path(args.out + ".md")
    cols = ["attack", "dataset", "model", "condition", "seed", "variant", "wsd", "n_total",
            "clean_accuracy", "eval_macro_f1", "adv_accuracy",
            "delta", "cASR", "flip_rate", "majority_pred_share", "degeneracy_flag"]
    table_df = out_df[cols].round(4).fillna("")
    header = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    body_lines = [
        "| " + " | ".join(str(v) for v in row) + " |"
        for row in table_df.itertuples(index=False, name=None)
    ]
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Baseline / augmentation metrics (macro-F1, cASR, flip-rate)\n\n")
        f.write("Derived from `examples.jsonl` per-row data; not present in "
                "`ukr-synonym-robustness/src/evaluation/metrics.py`'s `Summary`.\n\n")
        f.write("`eval_macro_f1` is the full eval-split figure from the checkpoint's "
                "TRAINING_COMPLETE marker -- judge clean performance on it, NOT on a "
                "macro-F1 computed over the attacked subset. `majority_pred_share` and "
                "`degeneracy_flag` guard against a cASR 'gain' that is really a model "
                "abandoning its minority classes.\n\n")
        flagged = out_df[out_df["degeneracy_flag"] != ""]
        if not flagged.empty:
            f.write(f"> **{len(flagged)} flagged cell(s).** Their cASR must not be quoted as a "
                    "robustness result without reporting the macro-F1 drop alongside it:\n>\n")
            for r in flagged.drop_duplicates(["dataset","model","condition","seed","variant"]).itertuples():
                f.write(f"> - `{r.dataset}/{r.model}/{r.condition}/seed{r.seed}"
                        f"{'/' + r.variant if r.variant else ''}` "
                        f"eval macro-F1 {r.eval_macro_f1:.3f}, majority share "
                        f"{r.majority_pred_share:.1%} — {r.degeneracy_flag}\n")
            f.write("\n")
        f.write("\n".join([header, sep, *body_lines]))
        f.write("\n")

    # ---- paired comparisons between every pair of conditions (same test examples) ----
    # Not just vs B0: RQ2 is B2-vs-B1 (does WSD filtering beat naive augmentation?), the
    # SAAA claim is B4-vs-B3 (does WSD filtering add anything on top of adversarial
    # selection?), and the RQ3 control is B5-vs-B3 (argmin vs argmax) -- none of which
    # are answered by baseline-only comparisons.
    groups: dict[tuple, dict[str, pd.DataFrame]] = {}
    for (attack, dataset, model, wsd, seed, variant, condition), df in frames.items():
        groups.setdefault((attack, dataset, model, wsd, seed, variant), {})[condition] = df

    # An ablation variant reuses the main grid's B0 (run_pilot.py never suffixes the
    # baseline, since it depends on neither the pool caps nor the ratio), so a variant
    # group has no B0 cell of its own. Inherit it from the base-variant group with the
    # same attack/dataset/model/wsd/seed, or the variant has nothing to compare against.
    for (attack, dataset, model, wsd, seed, variant), by_condition in groups.items():
        if variant and "B0" not in by_condition:
            base = groups.get((attack, dataset, model, wsd, seed, ""), {})
            if "B0" in base:
                by_condition["B0"] = base["B0"]

    paired_rows = []
    for key, by_condition in sorted(groups.items(), key=lambda kv: str(kv[0])):
        attack, dataset, model, wsd, seed, variant = key
        conditions = sorted(by_condition)
        for i, ref in enumerate(conditions):
            for cond in conditions[i + 1:]:
                comp = paired_comparison(by_condition[ref], by_condition[cond])
                if comp:
                    comp["reference_casr_paired"] = comp.pop("baseline_casr_paired")
                    paired_rows.append({"attack": attack, "dataset": dataset, "model": model,
                                        "wsd": wsd or "", "seed": seed or "", "variant": variant,
                                        "reference": ref, "condition": cond, **comp})

    if paired_rows:
        paired_df = pd.DataFrame(paired_rows)
        paired_df.to_csv(Path(args.out + "_paired.csv"), index=False)
        pcols = ["attack", "dataset", "model", "wsd", "seed", "variant", "reference", "condition",
                 "n_paired", "reference_casr_paired", "condition_casr_paired", "casr_delta",
                 "b_worse", "c_better", "p_value"]
        ptable = paired_df[pcols].round(4)
        with open(out_md, "a", encoding="utf-8") as f:
            f.write("\n## Paired condition comparisons (McNemar exact), per seed\n\n")
            f.write("Restricted to examples BOTH models classify correctly when clean. "
                    "`casr_delta` < 0 means `condition` is MORE robust than `reference`; "
                    "`p_value` is a two-sided exact test on the discordant pairs. These "
                    "capture EVALUATION sampling noise only -- not training-run variance, "
                    "which is what the across-seed table below is for.\n\n")
            f.write("| " + " | ".join(pcols) + " |\n")
            f.write("|" + "|".join("---" for _ in pcols) + "|\n")
            for row in ptable.itertuples(index=False, name=None):
                f.write("| " + " | ".join(str(v) for v in row) + " |\n")
        print(f"wrote {Path(args.out + '_paired.csv')}")

        write_across_seed_tables(out_df, paired_df, Path(args.out + "_by_seed.md"))

    print(f"\nwrote {out_csv}")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
