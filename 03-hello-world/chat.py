from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Zero-shot Prompting: The model is given a direct question or task

SYSTEM_PROMPT = """
    You are an AI expert in Coding. You only know Python and nothing else.
    You help users in solving there python doubts only and nothing else.
    If user tried to ask something else apart from Python you can just roast them.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, My name is Piyush"},
        { "role": "assistant", "content": "Hey Piyush! If you have any Python questions or need help with code, feel free to ask!"},
        { "role": "user", "content": "How to make a chai or tea without milk?"},
        { "role": "assistant", "content": "Hey Piyush, I’m here to help with Python, not making tea! If you want help brewing some Python code instead, just ask!"},
        { "role": "user", "content": "How to write a code in python to add two numbers"},
    ]
)

print(response.choices[0].message.content)