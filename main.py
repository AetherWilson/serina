from recorder import listen_for_serena, voice_to_string
from speaker import *
import gpt_handler
import asyncio

async def main():
    while True:
        serina_heard = listen_for_serena()
        if serina_heard:
            await play_tts_immediately("Yes?")
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
                print("Please repeat, I didn't catch that.")

if __name__ == "__main__":
    asyncio.run(main())