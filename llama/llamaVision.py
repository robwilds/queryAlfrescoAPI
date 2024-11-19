import requests
import os
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def llamavision(prompt,image):
    model_id = "unsloth/Llama-3.2-11B-Vision-Instruct"
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Proper device setup

    # Load the model
    model = MllamaForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16
    )
    model = model.to(device) 

    # Load the processor
    processor = AutoProcessor.from_pretrained(model_id)

    # Load an image from the web
    url = image #"https://huggingface.co/datasets/huggingface/documentation-images/resolve/0052a70beed5bf71b92610a43a52df6d286cd5f3/diffusers/rabbit.jpg"
    image = Image.open(requests.get(url, stream=True).raw)

    # Create a message list that includes an image and a text prompt
    messages = [
        {"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": prompt}
        ]}
    ]

    # Prepare inputs using the processor
    input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(image, input_text, return_tensors="pt").to(device)

    # Generate output from the model
    output = model.generate(**inputs, max_new_tokens=100)
    print(processor.decode(output[0], skip_special_tokens=True))

    #return 

if __name__ == '__main__':
    llamavision('what is happening in this picture?','http://localhost:9600/static/cce157f5-eb2b-4223-a157-f5eb2bb22362.jpg')