"""Fine-tune a classifier for a given (dataset, model, training_condition, seed) on
clean + cached augmented data.

Adapted from xml-roberta-finetune-reviews/main.py's loop (tokenize -> DataLoader ->
AdamW + linear warmup -> periodic eval/save) with these deliberate changes (see
CURRENT_STATE.md hygiene flags):
  - no hardcoded wandb API key -- reads WANDB_API_KEY env var, or skip with --no-wandb;
  - parameterized by --dataset/--model/--condition/--augmented-csv/--seed instead of
    hand-edited constants;
  - tracks macro-F1 (not just accuracy) for checkpoint selection, since Reviews is
    class-imbalanced (RESEARCH_PLAN.md metrics section);
  - B0 is never trained here -- reuse the existing checkpoint from configs/*.yaml.

M_robust = Train(D_clean ∪ D_aug) -- trained from the pretrained base, same recipe as
B0, just with the augmented rows concatenated onto the clean train set (offline
adversarial augmentation, article_plan.md Step 10). Not a continuation of B0's weights.

Usage:
    python scripts/train_augmented.py \
        --dataset reviews --model xlmr_base --condition B2 --seed 1914 \
        --augmented-csv results/augmented/reviews__wsd__r0.5__seed1914/augmented.csv \
        --output-dir results/checkpoints/reviews__xlmr_base__B2__seed1914
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import yaml
from sklearn.metrics import classification_report, f1_score
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers.optimization import get_linear_schedule_with_warmup

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NCLASSES = {"reviews": 5, "news": 5, "unlp": 2}
NEWS_LABELS = ["бізнес", "новини", "політика", "спорт", "технології"]
NEWS_LABEL2ID = {label: i for i, label in enumerate(NEWS_LABELS)}


def load_config(dataset: str) -> dict:
    with open(PROJECT_ROOT / "configs" / f"{dataset}.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_clean_split(dataset: str, path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if dataset == "reviews":
        return pd.DataFrame({"text": df["text"].astype(str), "label": df["label"].astype(int) - 1})
    if dataset == "news":
        df = df.dropna(subset=["target"])
        return pd.DataFrame({"text": df["title"].astype(str), "label": df["target"].map(NEWS_LABEL2ID).astype(int)})
    if dataset == "unlp":
        return pd.DataFrame({"text": df["text"].astype(str), "label": df["label"].astype(int)})
    raise ValueError(f"unknown dataset: {dataset!r}")


class TextClassificationDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.encodings = tokenizer(list(texts), truncation=True, padding="max_length", max_length=max_length)
        self.labels = list(labels)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item


def evaluate(model, loader, device, amp: bool = False):
    model.eval()
    all_preds, all_labels = [], []
    total_loss = 0.0
    with torch.no_grad():
        for batch in loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=amp):
                outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            total_loss += outputs.loss.item()
            preds = torch.argmax(outputs.logits, dim=-1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    accuracy = float(np.mean(np.array(all_preds) == np.array(all_labels)))
    macro_f1 = f1_score(all_labels, all_preds, average="macro")
    model.train()
    return accuracy, macro_f1, total_loss / max(len(loader), 1), all_labels, all_preds


def train(model, train_loader, eval_loader, optim, scheduler, config, output_dir, device, run=None):
    output_dir.mkdir(parents=True, exist_ok=True)
    best_macro_f1 = -1.0
    rounds_without_improvement = 0
    batch_count = 0
    amp = config["amp"]
    scaler = torch.amp.GradScaler(device.type, enabled=amp)

    for epoch in range(config["num_epochs"]):
        model.train()
        for step, batch in enumerate(train_loader):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=amp):
                outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss / config["grad_accum_steps"]
            scaler.scale(loss).backward()

            if (step + 1) % config["grad_accum_steps"] == 0:
                scaler.step(optim)
                scaler.update()
                scheduler.step()
                optim.zero_grad()

            if run is not None:
                run.log({"train/loss": outputs.loss.item()})

            if batch_count > 0 and batch_count % config["eval_every"] == 0:
                accuracy, macro_f1, eval_loss, all_labels, all_preds = evaluate(
                    model, eval_loader, device, amp=amp
                )
                print(f"[epoch {epoch} batch {batch_count}] eval_loss={eval_loss:.3f} "
                      f"acc={accuracy:.3f} macro_f1={macro_f1:.3f}")
                print(classification_report(all_labels, all_preds))
                if run is not None:
                    run.log({"eval/loss": eval_loss, "eval/accuracy": accuracy, "eval/macro_f1": macro_f1})

                if macro_f1 > best_macro_f1:
                    best_macro_f1 = macro_f1
                    rounds_without_improvement = 0
                    model.save_pretrained(output_dir, from_pt=True)
                    print(f"saved new best checkpoint to {output_dir} (macro_f1={macro_f1:.3f})")
                else:
                    rounds_without_improvement += 1

                if rounds_without_improvement >= config["early_stopping"]:
                    print(f"early stopping: no improvement for {config['early_stopping']} eval rounds")
                    return best_macro_f1

            batch_count += 1

    return best_macro_f1


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", choices=["reviews", "news", "unlp"], required=True)
    p.add_argument("--model", choices=["ukr_roberta", "xlmr_base"], required=True)
    p.add_argument("--condition",
                   choices=["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"], required=True,
                   help="B0 = baseline retrained with THIS loop on the same clean data "
                        "(no --augmented-csv), so B1-B4 are compared against an "
                        "identically-trained reference rather than the published checkpoint.")
    p.add_argument("--augmented-csv", type=str, default=None,
                   help="CSV with text,label columns (0-indexed). Omit for --condition B0.")
    p.add_argument("--clean-csv", type=str, default=None,
                   help="Clean train CSV in the dataset's native schema. Defaults to the "
                        "full configs/<dataset>.yaml train-path; pass a fixed subsample so "
                        "every condition trains on identical clean data.")
    p.add_argument("--no-amp", action="store_true", help="Disable mixed precision.")
    p.add_argument("--seed", type=int, default=1914)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--lr", type=float, default=2e-6)
    p.add_argument("--num-epochs", type=int, default=20)
    p.add_argument("--early-stopping", type=int, default=50, help="Eval rounds without improvement.")
    p.add_argument("--grad-accum-steps", type=int, default=8)
    p.add_argument("--eval-every", type=int, default=500, help="Batches between eval rounds.")
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--limit", type=int, default=None, help="Debug cap on combined train rows.")
    p.add_argument("--eval-limit", type=int, default=None, help="Debug cap on eval rows.")
    p.add_argument("--output-dir", type=str, required=True)
    p.add_argument("--no-wandb", action="store_true")
    p.add_argument("--wandb-project", type=str, default="ukr-adversarial-augmentation")
    args = p.parse_args(argv)

    torch.manual_seed(args.seed)
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    cfg = load_config(args.dataset)
    hf_name = cfg["models"][args.model]["hf-name"]
    nclasses = NCLASSES[args.dataset]

    clean_train = load_clean_split(args.dataset, args.clean_csv or cfg["train-path"])
    if args.condition == "B0":
        if args.augmented_csv:
            sys.exit("--condition B0 is the un-augmented baseline; drop --augmented-csv")
        augmented = pd.DataFrame({"text": [], "label": []}).astype({"label": int})
    else:
        if not args.augmented_csv:
            sys.exit(f"--condition {args.condition} requires --augmented-csv")
        augmented = pd.read_csv(args.augmented_csv)
    combined = pd.concat([clean_train, augmented], ignore_index=True)
    combined = combined.sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    if args.limit is not None:
        combined = combined.iloc[: args.limit]
    print(f"train rows: clean={len(clean_train)} augmented={len(augmented)} combined={len(combined)}")

    eval_df = load_clean_split(args.dataset, cfg["eval-path"])
    if args.eval_limit is not None:
        eval_df = eval_df.iloc[: args.eval_limit]

    tokenizer = AutoTokenizer.from_pretrained(hf_name)
    train_ds = TextClassificationDataset(combined["text"], combined["label"], tokenizer, args.max_length)
    eval_ds = TextClassificationDataset(eval_df["text"], eval_df["label"], tokenizer, args.max_length)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=4, pin_memory=True)
    eval_loader = DataLoader(eval_ds, batch_size=args.batch_size, shuffle=False, num_workers=4, pin_memory=True)

    model = AutoModelForSequenceClassification.from_pretrained(hf_name, num_labels=nclasses).to(device)

    optim = torch.optim.AdamW(model.parameters(), lr=args.lr)
    total_steps = (len(train_loader) // args.grad_accum_steps) * args.num_epochs
    warmup_steps = int(0.1 * total_steps)
    scheduler = get_linear_schedule_with_warmup(optim, num_warmup_steps=warmup_steps, num_training_steps=total_steps)

    run = None
    if not args.no_wandb:
        try:
            import wandb

            api_key = os.environ.get("WANDB_API_KEY")
            if api_key:
                wandb.login(key=api_key)
            run = wandb.init(project=args.wandb_project, config=vars(args))
        except Exception as exc:  # noqa: BLE001
            print(f"wandb init failed ({exc!r}); continuing without logging")
            run = None

    train_config = {
        "num_epochs": args.num_epochs,
        "grad_accum_steps": args.grad_accum_steps,
        "eval_every": args.eval_every,
        "early_stopping": args.early_stopping,
        "amp": (not args.no_amp) and device.type == "cuda",
    }
    output_dir = Path(args.output_dir)
    best_macro_f1 = train(model, train_loader, eval_loader, optim, scheduler, train_config, output_dir, device, run=run)
    print(f"best eval macro_f1: {best_macro_f1:.3f}")

    # The checkpoint on disk is rewritten at every eval round that improves macro-F1, so
    # its mere existence does NOT mean training finished -- a run killed midway leaves a
    # valid but undertrained checkpoint behind. This marker is what run_pilot.py's
    # skip-if-exists check keys on, so an interrupted training is redone rather than
    # silently reused.
    (output_dir / "TRAINING_COMPLETE").write_text(
        json.dumps({"best_macro_f1": best_macro_f1, "condition": args.condition,
                    "seed": args.seed, "finished": datetime.now().isoformat()},
                   indent=2) + "\n", encoding="utf-8")

    if run is not None:
        run.finish()

    torch.cuda.empty_cache()
    gc.collect()


if __name__ == "__main__":
    main()
