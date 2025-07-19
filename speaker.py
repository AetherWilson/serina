import asyncio
import edge_tts
import tempfile
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time

async def play_tts_immediately(text, voice="en-US-AriaNeural"):
    """Play TTS audio immediately using a temporary file"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tmp_filename = tmp_file.name
    
    try:
        # Generate speech and save to temporary file
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp_filename)
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Load and play the audio file
        pygame.mixer.music.load(tmp_filename)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
    finally:
        # Clean up the temporary file
        pygame.mixer.quit()
        if os.path.exists(tmp_filename):
            os.unlink(tmp_filename)

if __name__ == "__main__":
    # Test the function
    test_text = "Hello, I'm under the water, please help me."
    print(f"Speaking: {test_text}")
    play_tts_immediately(test_text, voice="en-US-JennyNeural") #en-US-AriaNeural en-US-JennyNeural en-US-MichelleNeural