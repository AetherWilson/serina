from recorder import listen_for_serena, voice_to_string
from speaker import *
import gpt_handler
import asyncio
import random
from json_handle import read_settings, write_chat_history, read_chat_history
from txt_handle import read_txt_file
import speech_recognition as sr

# todo
# make personalities for serina
# make chat loggable

def random_start_string():
    """Generate a random start string for the conversation."""
    responses = ["Yes?", "I'm here.", "What's up?", "I'm listening."]
    return random.choice(responses)

async def main():
    recognizer = sr.Recognizer()
    print("adjusting for ambient noise...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)
    print("Ready to listen for 'Serina'...")
    while True:
        serina_heard = listen_for_serena()
        if serina_heard:
            # Get voice model from settings
            voice_model = read_settings('serina_voice_model') or "en-US-AriaNeural"
            await play_tts_immediately(random_start_string(), voice=voice_model)
            
            recognized_text = voice_to_string(recognizer=recognizer)  # Uses language from settings
            if recognized_text:
                print(f"Recognized: {recognized_text}")
                await play_tts_immediately(f"I heard you said: {recognized_text}, let me think.", voice=voice_model)
                chat_history = read_chat_history()
                response = gpt_handler.completion_response(
                    model="deepseek-v3-250324",
                    system_prompt=read_txt_file("personality.txt"),
                    chat_history=chat_history if chat_history else None,
                    user_prompt=recognized_text,
                    temperature=1.0
                )
                print(f"Response: {response}")
                write_chat_history(
                    [{'role': 'user', 'content': recognized_text},
                     {'role': 'assistant', 'content': response}]
                )
                await play_tts_immediately(response, voice=voice_model)
            else:
                await play_tts_immediately("Please repeat, I didn't catch that.", voice=voice_model)

if __name__ == "__main__":
    asyncio.run(main())