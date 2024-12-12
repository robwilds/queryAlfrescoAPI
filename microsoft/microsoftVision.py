import requests
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from dotenv import load_dotenv
import os
load_dotenv()

#this is used to get info for images

print("\nmicrosoft model is -> "+ os.getenv("microsoft_model") )

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = AutoModelForCausalLM.from_pretrained(os.getenv("microsoft_model"), torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained(os.getenv("microsoft_model"), trust_remote_code=True)

prompt = "<CAPTION>"

url = "https://live.staticflickr.com/65535/54172543481_2c463a309e_6k.jpg"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)

generated_ids = model.generate(
    input_ids=inputs["input_ids"],
    pixel_values=inputs["pixel_values"],
    max_new_tokens=1024,
    do_sample=False,
    num_beams=3,
)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

parsed_answer = processor.post_process_generation(generated_text, task=prompt, image_size=(image.width, image.height))

print(parsed_answer)
