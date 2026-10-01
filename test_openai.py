import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("API key loaded:", bool(api_key))

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
    messages=[
        {
            "role": "user",
            "content": "Say hello in one short sentence."
        }
    ]
)

print(response.choices[0].message.content)