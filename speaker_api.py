import openai
import httpx
import io
import os
# Suppress pygame welcome message BEFORE importing pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from dotenv import load_dotenv
import tempfile
import asyncio

# Load environment variables
load_dotenv()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Get environment variables for OpenAI configuration
redirect_url = os.getenv('gpt_redirect_url')
api_key = os.getenv('gpt_api_key')

# Create OpenAI client with redirect URL support
if redirect_url:
    openai_client = openai.OpenAI(
        api_key=api_key,
        base_url=redirect_url,
        http_client=httpx.Client(
            base_url=redirect_url,
            follow_redirects=True,
        ),
    )
else:
    openai_client = openai.OpenAI(
        api_key=api_key
    )

def play_tts_openai(text, voice="nova", model="tts-1", speed=1.0, instructions=None):
    """
    Convert text to speech using OpenAI TTS-1 API and play it automatically.
    Does not save any audio files - plays directly from memory.
    
    Args:
        text (str): The text to convert to speech
        voice (str): Voice to use. Options: alloy, echo, fable, onyx, nova, shimmer
        model (str): TTS model to use. Options: tts-1, tts-1-hd
        speed (float): Speech speed (0.25 to 4.0)
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Generate speech using OpenAI TTS API with pre-configured client
        response = openai_client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            speed=speed,
            instructions=instructions
        )
        
        # Get audio data as bytes
        audio_data = response.content
        
        # Create a temporary file-like object in memory
        audio_buffer = io.BytesIO(audio_data)
        
        # Play audio directly from memory using pygame
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()
        
        # Wait for playback to complete
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        print(f"✓ Successfully played TTS: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        return True
        
    except Exception as e:
        print(f"❌ Error in OpenAI TTS playback: {e}")
        return False

async def play_tts_openai_async(text, voice="nova", model="tts-1", speed=1.0, instructions=None):
    """
    Async version of play_tts_openai for use in async contexts.
    
    Args:
        text (str): The text to convert to speech
        voice (str): Voice to use. Options: alloy, echo, fable, onyx, nova, shimmer
        model (str): TTS model to use. Options: tts-1, tts-1-hd
        speed (float): Speech speed (0.25 to 4.0)
        instructions (str): Optional instructions for the voice tone/style
    
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Run the synchronous function in a thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, play_tts_openai, text, voice, model, speed, instructions)
        return result
        
    except Exception as e:
        print(f"❌ Error in async OpenAI TTS playback: {e}")
        return False

def save_tts_to_mp3(text, filename, voice="nova", model="tts-1", speed=1.0, instructions=None):
    """
    Convert text to speech and save as MP3 file in organized folder structure.
    
    Args:
        text (str): The text to convert to speech
        filename (str): Name of the audio file (without extension)
        voice (str): Voice to use. Options: alloy, echo, fable, onyx, nova, shimmer
        model (str): TTS model to use. Options: tts-1, tts-1-hd
        speed (float): Speech speed (0.25 to 4.0)
        instructions (str): Optional instructions for the voice tone/style
    
    Returns:
        str: Full path to the saved MP3 file if successful, None if failed
    """
    try:
        # Create directory structure: pre-recorded-audio/{voice}/
        base_dir = "pre-recorded-audio"
        voice_dir = os.path.join(base_dir, voice)
        os.makedirs(voice_dir, exist_ok=True)
        
        # Generate speech using OpenAI TTS API
        response = openai_client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            speed=speed,
            instructions=instructions,
            response_format="mp3"  # Explicitly request MP3 format
        )
        
        # Create full file path
        mp3_filename = f"{filename}.mp3" if not filename.endswith('.mp3') else filename
        file_path = os.path.join(voice_dir, mp3_filename)
        
        # Save the audio data to MP3 file
        with open(file_path, 'wb') as audio_file:
            audio_file.write(response.content)
        
        print(f"✓ Successfully saved MP3: '{file_path}'")
        print(f"  Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"  Voice: {voice} | Model: {model} | Speed: {speed}")
        
        return file_path
        
    except Exception as e:
        print(f"❌ Error saving TTS to MP3: {e}")
        return None

def test_voices():
    """
    Test all available OpenAI TTS voices.
    """
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    test_text = "Hello, this is a test of the OpenAI TTS voice."
    
    print("🎤 Testing OpenAI TTS voices...")
    print("-" * 50)
    
    for voice in voices:
        print(f"Testing voice: {voice}")
        success = play_tts_openai(test_text, voice=voice)
        if not success:
            print(f"Failed to test voice: {voice}")
        print("-" * 30)

def get_voice_info():
    """
    Get information about available voices and models.
    
    Returns:
        dict: Information about voices and models
    """
    return {
        "voices": {
            "alloy": "Neutral, balanced voice",
            "echo": "Clear, articulate voice", 
            "fable": "Warm, engaging voice",
            "onyx": "Deep, authoritative voice",
            "nova": "Bright, energetic voice",
            "shimmer": "Soft, gentle voice"
        },
        "models": {
            "tts-1": "Standard quality, faster generation",
            "tts-1-hd": "Higher quality, slower generation"
        },
        "speed_range": "0.25 to 4.0 (1.0 is normal speed)",
        "max_input_length": "4096 characters"
    }

if __name__ == "__main__":
    print("=== OpenAI TTS-1 API Speaker ===")
    print("Features:")
    print("✓ Uses OpenAI TTS-1 API")
    print("✓ No audio files saved")
    print("✓ Direct memory playback")
    print("✓ Multiple voice options")
    print("✓ Async support")
    print("✓ MP3 file saving with organized folders")
    print()
    
    # Display voice information
    info = get_voice_info()
    print("Available voices:")
    for voice, description in info["voices"].items():
        print(f"  • {voice}: {description}")
    print()
    
    # Interactive test
    try:
        while True:
            print("Options:")
            print("1. Test single voice")
            print("2. Test all voices")
            print("3. Custom text with voice selection")
            print("4. Save text to MP3 file")
            print("5. Exit")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == "1":
                text = input("Enter text to speak: ")
                voice = input("Enter voice (alloy/echo/fable/onyx/nova/shimmer) [nova]: ").strip() or "nova"
                play_tts_openai(text, voice=voice)
                
            elif choice == "2":
                test_voices()
                
            elif choice == "3":
                text = input("Enter text to speak: ")
                instructions = input("Enter any additional instructions (optional): ").strip() or None
                print("Available voices: alloy, echo, fable, onyx, nova, shimmer")
                voice = input("Enter voice [nova]: ").strip() or "nova"
                model = input("Enter model (tts-1/tts-1-hd/gpt-4o-mini-tts) [tts-1]: ").strip() or "tts-1"
                speed = input("Enter speed (0.25-4.0) [1.0]: ").strip() or "1.0"

                
                try:
                    speed = float(speed)
                    play_tts_openai(text, voice=voice, model=model, speed=speed, instructions=instructions)
                except ValueError:
                    print("Invalid speed value, using 1.0")
                    play_tts_openai(text, voice=voice, model=model)
                    
            elif choice == "4":
                text = input("Enter text to convert to MP3: ")
                instructions = input("Enter any additional instructions (optional): ").strip() or None
                filename = input("Enter filename (without extension): ")
                print("Available voices: alloy, echo, fable, onyx, nova, shimmer")
                voice = input("Enter voice [nova]: ").strip() or "nova"
                model = input("Enter model (tts-1/tts-1-hd) [tts-1]: ").strip() or "tts-1"
                speed = input("Enter speed (0.25-4.0) [1.0]: ").strip() or "1.0"
                
                try:
                    speed = float(speed)
                    saved_path = save_tts_to_mp3(text, filename, voice=voice, model=model, speed=speed, instructions=instructions)
                    if saved_path:
                        print(f"🎵 MP3 saved successfully!")
                        print(f"📁 Location: {saved_path}")
                except ValueError:
                    print("Invalid speed value, using 1.0")
                    save_tts_to_mp3(text, filename, voice=voice, model=model, instructions=instructions)
                    
            elif choice == "5":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice, please try again.")
                
    except KeyboardInterrupt:
        print("\n👋 Program terminated by user.")
    except Exception as e:
        print(f"Program error: {e}")
        print("\nMake sure you have:")
        print("1. Set gpt_api_key in your .env file")
        print("2. Installed required packages: pip install openai pygame python-dotenv httpx")
        print("3. Valid OpenAI API key with TTS access")
        print("4. Optionally set gpt_redirect_url if using a proxy/redirect")
