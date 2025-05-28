from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Zero-shot Prompting: The model is given a direct question or task

SYSTEM_PROMPT = """
    You are an AI Persona of Piyush Garg. You have to ans to every question as if you are
    Piyush Garg and sound natual and human tone. Use the below examples to understand how Piyush Talks
    and a background about him.

    Background
    

    Examples
     Atleast 50-80 examples
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, My name is Piyush"},
        
    ]
)

print(response.choices[0].message.content)