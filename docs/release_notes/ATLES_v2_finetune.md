# ATLES Fine-Tuning v2 Release Notes

## Overview

This release packages the new v2 training corpus (memory stores + engineering docs) and a reusable fine-tuning entrypoint that targets three model families: `llama3.2`, `gamma3:4b`, and `qwen33.1:7b`. The objectives are:

- consolidate every available memory artifact and vetted documentation into a single dataset
- support repeatable LoRA-style supervised fine-tuning against the same dataset for each base model
- version outputs under `models/v2/<alias>` so the autonomy stack can swap between families without manual wiring

## Data Sources

| Source | Notes |
| --- | --- |
| `atles_app/atles_memory` | latest on-device memory (core, semantic, episodic, user prefs, daemon sessions) |
| `atles_memory` | historical/archived memory tree and checkpoints |
| `docs/guides`, `docs/architecture`, `docs/updates`, `docs/bugs`, `docs/system-analysis`, `docs/memory-system` | coder-facing documentation, fixes, roadmaps, and safety specs |

Dataset build script: `python atles_app/fine_tune/build_dataset_v2.py`

Outputs under `datasets/v2/`:

- `combined_train.jsonl` (5,838 examples)
- `combined_val.jsonl` (649 examples)
- `metadata.json` (counts, directory provenance)

Each example contains:

```json
{
  "prompt": "Instruction: ... Response:",
  "completion": "<ground-truth text>",
  "source": "relative/path",
  "kind": "memory|doc",
  "category": "<i.e., constitutional, guides, etc.>"
}
```

## Fine-Tuning Pipeline

Entrypoint: `python atles_app/fine_tune/fine_tune_v2.py --model <alias> [--dry-run]`

Configs (edit as needed):

| Alias | Config | Base model | Batch | Epochs | Notes |
| --- | --- | --- | --- | --- | --- |
| `llama3.2` | `configs/fine_tune_llama3.2_v2.json` | `meta-llama/Meta-Llama-3-8B-Instruct` | 2 (grad accum 8) | 2 | 4K ctx, LoRA r=16 |
| `gamma3:4b` | `configs/fine_tune_gamma3-4b_v2.json` | `google/gemma-2b-it` | 4 (grad accum 4) | 3 | 3K ctx, LoRA r=32 |
| `qwen33.1:7b` | `configs/fine_tune_qwen33.1-7b_v2.json` | `Qwen/Qwen2.5-7B-Instruct` | 1 (grad accum 16) | 2 | 4K ctx, LoRA r=16 |

The script:

1. loads dataset JSONL files
2. tokenizes to `max_seq_length`
3. applies optional LoRA adapters (PEFT)
4. launches Hugging Face `Trainer` with supplied hyperparameters
5. writes artifacts to `models/v2/<alias_safe>/final` plus tokenizer snapshot

### Example dry-run

```powershell
python atles_app/fine_tune/fine_tune_v2.py --model llama3.2 --dry-run
```

Dry run prints the resolved config/dataset/output paths so you can verify before committing GPU hours.

### Full training

Remove `--dry-run` and ensure `torch`, `transformers`, `datasets`, and `peft` are installed (GPU with ≥24GB recommended for the larger models). Sample invocation:

```powershell
python atles_app/fine_tune/fine_tune_v2.py --model gamma3:4b
```

Monitor logs under `models/v2/<alias_safe>`; intermediate checkpoints save every 200 global steps by default.

## Validation & Reporting

After each training run:

1. capture objective metrics from the console (loss, eval loss) and store in `reports/v2/<alias>.md`
2. record qualitative probes (e.g., memory recall, coding behavior)
3. update the `models` registry / Ollama Modelfiles to reference the new `<alias>-v2` artifacts

## Next Actions

- [ ] Schedule real GPU runs (dry-runs completed for all aliases; actual training pending hardware availability)
- [ ] Create `reports/v2/<alias>.md` once metrics are produced
- [ ] Wire the resulting weights into the autonomous runtime and modelfile builders

