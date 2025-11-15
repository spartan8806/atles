@echo off
REM Fine-tune Qwen3-Embedding-4B for ATLES
REM This script fine-tunes the embedding model on STS-B, NLI, and custom ATLES data

echo ========================================
echo ATLES Embedding Model Fine-Tuning
echo Model: Qwen3-Embedding-4B
echo ========================================
echo.

python finetune_embedding_model.py --config finetune_embedding_config.json

echo.
echo ========================================
echo Fine-tuning complete!
echo Check ./finetuned_models/atles_qwen3_embedding_4b for output
echo ========================================
pause
