from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio
load_dotenv()

import speech_recognition as sr
from .graph import graph

messages = []

openai = AsyncOpenAI()

async def tts(text: str):
    async with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="coral",
        input=text,
        instructions="Speak in a funny tone",
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    r = sr.Recognizer()  # Speech to Text

    with sr.Microphone() as source:  # Mic Access
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        while True:
            print("Speak something...")
            audio = r.listen(source)

            print("Processing Audio... (STT)")
            stt = r.recognize_google(audio)

            print("You said:", stt)
            messages.append({ "role": "user", "content": stt })

            for event in graph.stream({ "messages": messages }, stream_mode="values"):
                if "messages" in event:
                    messages.append({ "role": "assistant", "content": event["messages"][-1].content })
                    event["messages"][-1].pretty_print()


# main()

asyncio.run(tts(text="Hey! (laugh) Nice to meet you. How can I help you with coding"))