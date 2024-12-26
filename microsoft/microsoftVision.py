import requests
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from dotenv import load_dotenv
import os, json
load_dotenv()

#this is used to get info for images

def msVision(prt,img):
    print("\nmicrosoft model is -> "+ os.getenv("microsoft_model") )

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForCausalLM.from_pretrained(os.getenv("microsoft_model"), torch_dtype=torch_dtype, trust_remote_code=True).to(device)
    processor = AutoProcessor.from_pretrained(os.getenv("microsoft_model"), trust_remote_code=True)

    prompt = prt

    #url = img
    print('opening image')
    image = Image.open(requests.get(img, stream=True).raw)

    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)

    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=500,
        do_sample=False,
        num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

    parsed_answer = processor.post_process_generation(generated_text, task=prompt, image_size=(image.width, image.height))

    print(json.dumps(parsed_answer))

    return (json.dumps(parsed_answer))

if __name__ == '__main__':
    msVision('<MORE_DETAILED_CAPTION>','https://live.staticflickr.com/65535/54157051527_8fa4f6af98_6k.jpg')
