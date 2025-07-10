from openai import OpenAI
import os
from dotenv import load_dotenv

client = OpenAI()

#os.getenv("OPENAI_API_KEY")

completion = client.chat.completions.create(

    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)
