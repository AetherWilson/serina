import speech_recognition as sr
import time
from json_handle import read_settings

def voice_to_string(selected_language=None):
    """
    Records human voice until silence is detected and converts it to a string.
    
    Args:
        selected_language (str): Language to use for recognition. If None, uses setting from JSON. 
                                Defaults to "en" if no setting found.
    
    Returns:
        str: The recognized speech as text, or None if no speech was detected/recognized
    """
    # Get language from parameter or settings
    if selected_language is None:
        selected_language = read_settings('serina_language') or "en"
    
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Get settings from JSON
    recognizer.energy_threshold = read_settings('microphone_threshold') or 40
    recognizer.pause_threshold = read_settings('pause_threshold') or 1.4

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening for voice...")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        try:
            # Listen for audio with a timeout and phrase time limit
            # timeout: how long to wait for speech to start
            # phrase_time_limit: maximum time to record after speech starts (increased to 15 seconds)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            # Recognize speech using Whisper with selected language
            if selected_language == "en":
                text = recognizer.recognize_whisper(audio, model="base", language="english")
            elif selected_language == "zh":
                text = recognizer.recognize_whisper(audio, model="base", language="chinese")
            elif selected_language == "auto":
                text = recognizer.recognize_whisper(audio, model="base")  # Auto-detect
            else:
                # Default to English for unknown languages
                text = recognizer.recognize_whisper(audio, model="base", language="english")
            
            return text
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period.")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None

def listen_for_serena():
    """
    Listens for human voice, records it, and detects if 'serena' was said.
    Always uses English for wake word detection.
    
    Returns:
        bool: True if 'serena' is detected in the speech, False otherwise
    """
    # Always use English for wake word detection
    text = voice_to_string(selected_language="en")
    if text and 'serena' in text.lower():
        print("Serena detected!")
        return True
    else:
        print("Serena not detected.")
        return False
            

if __name__ == "__main__":
    while True:
        text = voice_to_string()
        if text:
            print(f"Recognized text: {text}")
        else:
            print("Waiting for next attempt...")
            time.sleep(1)
