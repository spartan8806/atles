#!/bin/bash
# RunPod Quick Setup - Execute immediately after pod starts

# Install dependencies
pip install sentence-transformers datasets transformers torch accelerate huggingface_hub -q

# Download Google Drive data
pip install gdown -q
cd /workspace
gdown --folder https://drive.google.com/drive/folders/1iHN8EhlDzEoX3vgypFRAIfrYvSnZEU_4

# Clone repo
git clone https://github.com/spartan8806/atles.git
cd atles

# Start fine-tuning immediately
python finetune_embedding_model.py
