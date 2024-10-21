import torch
from transformers import pipeline

model_id = "Llama-3.2-1B-Instruct-Q4_K_M"
MODEL_PATH = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"
pipe = pipeline(
    "text-generation",
    
    MODEL_PATH=MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]
outputs = pipe(
    messages,
    max_new_tokens=256,
)
print(outputs[0]["generated_text"][-1])
