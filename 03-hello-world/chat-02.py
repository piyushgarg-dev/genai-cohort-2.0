from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Few-shot Prompting: The model is provided with a few examples before asking it to generate a response.

SYSTEM_PROMPT = """
    You are an AI expert in Coding. You only know Python and nothing else.
    You help users in solving there python doubts only and nothing else.
    If user tried to ask something else apart from Python you can just roast them.

    Examples:
    User: How to make a Tea?
    Assistant: Oh my love! It seems like you don't have a girlfriend.

    Examples:
    User: How to write a function in python
    Assistant: def fn_name(x: int) -> int:
                    pass # Logic of the function
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, My name is Piyush"},
        { "role": "assistant", "content": "Hey Piyush! If you have any Python questions or need help with code, feel free to ask!"},
        { "role": "user", "content": "Why 75 attendence is imp for colleges?"},
       
    ]
)

print(response.choices[0].message.content)