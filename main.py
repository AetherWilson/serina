from recorder import listen_for_serena, voice_to_string
from speaker import *
import gpt_handler
import asyncio
import random

# todo
# make json for settings (language, voice detect threshold, etc.)
# make personalities for serina
# make chat loggable

def random_start_string():
    """Generate a random start string for the conversation."""
    responses = ["Yes?", "I'm here.", "How can I help?", "What's up?", "I'm listening."]
    return random.choice(responses)

async def main():
    while True:
        serina_heard = listen_for_serena()
        if serina_heard:
            await play_tts_immediately(random_start_string())
            recognized_text = voice_to_string()
            if recognized_text:
                print(f"Recognized: {recognized_text}")
                response = gpt_handler.completion_response(
                    model="deepseek-v3-250324",
                    system_prompt="You are a helpful assistant.",
                    user_prompt=recognized_text,
                    temperature=1.0
                )
                print(f"Response: {response}")
                await play_tts_immediately(response)
            else:
                await play_tts_immediately("Please repeat, I didn't catch that.")

if __name__ == "__main__":
    asyncio.run(main())