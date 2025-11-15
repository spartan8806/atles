"""Download a good pre-trained embedding model for ATLES"""
from transformers import AutoTokenizer, AutoModel
import os

model_name = "sentence-transformers/all-mpnet-base-v2"
output_dir = "./models/atles_embedding_model"

print(f"Downloading {model_name}...")
print("This is a high-quality embedding model that scores ~0.83 on STSBenchmark")

os.makedirs(output_dir, exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

print(f"\nSaving to {output_dir}...")
tokenizer.save_pretrained(output_dir)
model.save_pretrained(output_dir)

print("\n" + "="*60)
print("Done! Embedding model ready at:")
print(output_dir)
print("="*60)
print("\nYou can now run MTEB on this model:")
print(f"python -m mteb run -m {output_dir} --output_folder mteb_results")
