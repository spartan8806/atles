# Upload Model to Hugging Face - Instructions

## Current Situation

Your Hugging Face repository `spartan8806/atles` currently contains:
- ✅ Source code (439 files)
- ✅ Model files (model.safetensors, config.json, tokenizer files) - **Already uploaded!**

## To Create `spartan8806/atles-large` Model Repository

### Option 1: Upload Existing Model from Root Directory

If you want to upload the model files currently in your root directory to a new `atles-large` repository:

```bash
python upload_model_to_hf.py --model-path "." --repo-id spartan8806/atles-large
```

**Note:** This will upload:
- `model.safetensors` (1.21 GB)
- `config.json`
- `tokenizer.json`, `tokenizer_config.json`, `tokenizer.model`
- `sentence_bert_config.json`
- `modules.json`
- `config_sentence_transformers.json`
- `generation_config.json`
- Pooling/dense layer configs

### Option 2: Upload a Different Model Directory

If you have a fine-tuned model in a different directory:

```bash
python upload_model_to_hf.py --model-path "<path-to-model-dir>" --repo-id spartan8806/atles-large
```

### Option 3: Manual Upload via Web UI

1. Go to https://huggingface.co/spartan8806/atles-large (create repo if needed)
2. Click **Files and versions** → **Add file** → **Upload files**
3. Drag and drop these files from your local directory:
   - `model.safetensors` (or `pytorch_model.bin`)
   - `config.json`
   - `tokenizer.json`
   - `tokenizer_config.json`
   - `tokenizer.model` (if exists)
   - `sentence_bert_config.json` (if exists)
   - `modules.json` (if exists)
   - Any other model-related JSON/config files

## Required Files for MTEB Evaluation

For MTEB to work, your model repository needs:
- ✅ Model weights (`*.safetensors` or `*.bin`)
- ✅ `config.json`
- ✅ Tokenizer files (`tokenizer.json`, `tokenizer_config.json`)
- ✅ `sentence_bert_config.json` (for SentenceTransformer models)
- ✅ `modules.json` (for SentenceTransformer models)

## After Upload

Once uploaded, you can run MTEB evaluation:

```bash
python -m mteb run -m spartan8806/atles-large --tasks "STSBenchmark" --output_folder mteb_results
```

**Note:** Use specific task names instead of `"*"` - MTEB doesn't support wildcard `"*"` for tasks.

Available task categories:
- `"STSBenchmark"` - Semantic Text Similarity
- `"BitextMining"` - Bitext mining
- `"Classification"` - Classification tasks
- `"Clustering"` - Clustering tasks
- `"PairClassification"` - Pair classification
- `"Reranking"` - Reranking tasks
- `"Retrieval"` - Retrieval tasks
- `"Summarization"` - Summarization tasks

Or run all tasks:
```bash
python -m mteb run -m spartan8806/atles-large --output_folder mteb_results
```

