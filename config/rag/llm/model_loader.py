import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

CHECKPOINT = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

print("Loading SmolLM2 model...")

tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)

model = AutoModelForCausalLM.from_pretrained(
    CHECKPOINT,
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True
)

model.eval()

print("Model loaded successfully!")