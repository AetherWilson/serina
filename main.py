from recorder import WakeWordDetector, record_voice_to_string
from speaker_api import play_tts_openai_async
import gpt_handler
import asyncio
import random
from json_handle import read_settings, write_chat_history, read_chat_history
from txt_handle import read_txt_file
import speech_recognition as sr
import datetime
import os
import pygame

# todo
# make personalities for serina
# make chat loggable

voice_to_use = "nova"

def print_header():
    """Print a clean header for the application."""
    print("\n" + "="*60)
    print("🤖 SERINA - AI Voice Assistant")
    print("="*60)
    print(f"📅 Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Wake word: 'Serina'")
    print("🎤 Ready to listen...")
    print("="*60 + "\n")

def print_status(message, status_type="info"):
    """Print formatted status messages."""
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    icons = {
        "info": "ℹ️",
        "listening": "👂",
        "processing": "🔄", 
        "speaking": "🗣️",
        "success": "✅",
        "error": "❌",
        "wake": "🎯"
    }
    icon = icons.get(status_type, "ℹ️")
    print(f"[{timestamp}] {icon} {message}")

async def play_random_start_audio():
    """Play a random pre-recorded start audio from the specified voice folder."""
    # Build path to the voice folder
    audio_folder = os.path.join("pre-recorded-audio", voice_to_use)
    
    # Get all audio files (.mp3, .wav, etc.) from the folder
    audio_files = [f for f in os.listdir(audio_folder) 
                  if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a'))]
    
    # Select a random audio file
    selected_file = random.choice(audio_files)
    file_path = os.path.join(audio_folder, selected_file)
    
    print_status(f"Playing: {selected_file}", "speaking")
    
    # Initialize pygame mixer if not already done
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    # Play the audio file
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
    # Wait for playback to complete
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)  # Non-blocking wait

async def main():
    # Print clean header
    print_header()
    
    # Create a single wake word detector instance to avoid repeated calibration
    print_status("Initializing wake word detector...", "info")
    wake_detector = WakeWordDetector(
        wake_word="serina",
        confidence_threshold=0.7,
        buffer_duration=3.0
    )
    
    print_status("Listening for wake word 'Serina'...", "listening")
    
    while True:
        serina_heard = wake_detector.wake_word_detect_new()
        if serina_heard:
            print_status("Wake word detected! Responding...", "wake")
            
            # Play pre-recorded start audio
            await play_random_start_audio()
            
            print_status("Listening for user input...", "listening")
            recognized_text = record_voice_to_string()  # Uses optimized voice recording
            
            if recognized_text:
                print_status(f"User said: '{recognized_text}'", "success")
                print_status("Processing with AI...", "processing")
                
                chat_history = read_chat_history()
                response = gpt_handler.completion_response(
                    model="gpt-5-chat",
                    system_prompt=read_txt_file("personality.txt"),
                    chat_history=chat_history if chat_history else None,
                    user_prompt=recognized_text,
                    temperature=1.0
                )
                
                print_status(f"AI Response: {response[:100]}{'...' if len(response) > 100 else ''}", "success")
                
                write_chat_history(
                    [{'role': 'user', 'content': recognized_text},
                     {'role': 'assistant', 'content': response}]
                )
                
                print_status("Speaking response...", "speaking")
                await play_tts_openai_async(response, voice=voice_to_use, model="tts-1", speed=0.9, instructions="calm and soothing tone.")

                print_status("Ready for next interaction", "info")
                print("-" * 40)
            else:
                print_status("Could not understand speech", "error")
                await play_tts_openai_async("Please repeat, I didn't catch that.", voice=voice_to_use, model="tts-1")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n" + "="*60)
        print("🛑 SERINA - Shutting down gracefully")
        print("="*60)
        print(f"📅 Stopped: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("👋 Goodbye!")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        print("🔧 Please check your configuration and try again.")