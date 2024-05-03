import speech_recognition as sr
from openai import OpenAI
import pyttsx3
import os
import time
import random
import pygame

client = OpenAI(api_key = "")


def listen_microphone():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Processing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return "Tell me a random historical fact"
    except sr.RequestError as e:
        print(f"Sorry, an error occurred. {e}")
        return ""

def query_chatgpt(prompt):
    response = client.completions.create(
      model="gpt-3.5-turbo-instruct",
      prompt=prompt + "  Please format your response in a dry, snarky or funny tone and keep the response very brief. Also, your a robot assistant and your name is Peach.",
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].text.strip()

def speak_text(text, rate=0.3):
    engine = pyttsx3.init()
    newVoiceRate = 185
    engine.setProperty('rate',newVoiceRate)
    engine.say(text)
    engine.runAndWait()

def main():
    pygame.mixer.init()
    
    while True:
        print("Please speak:")
        query = listen_microphone()
        print("You said:", query)
        gptresponse = query_chatgpt(query)

        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=f"{gptresponse}",
        ) as response:
            response.stream_to_file("speech.mp3")

        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()

        # Wait for the mp3 to finish playing
        while pygame.mixer.music.get_busy():
            continue


if __name__ == "__main__":
    main()



