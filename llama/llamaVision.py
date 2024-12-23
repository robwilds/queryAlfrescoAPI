import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor
from dotenv import load_dotenv
import os
load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "True"


def llamavision(prompt,image):
    try:
        model_id = os.getenv("llama_vision_model")
        #model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
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
        url = image
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
        screenoutput = processor.decode(output[0], skip_special_tokens=True)
        print('printing screen output --> ')
        print(screenoutput)

        return(screenoutput)
    except Exception as e:
        print ('error-> '+ str(e))
        return('error-> '+ str(e))

if __name__ == '__main__':
    llamavision('what is happening in this picture?','https://live.staticflickr.com/65535/54172543481_2c463a309e_6k.jpg')
