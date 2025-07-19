import speech_recognition as sr
import time

def listen_for_serena():
    """
    Listens for human voice, records it, and detects if 'serena' was said.
    
    Returns:
        bool: True if 'serena' is detected in the speech, False otherwise
    """
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening for voice...")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=2)
        # Lower the energy threshold to make it more sensitive to quieter sounds
        recognizer.energy_threshold = 40
        # Set pause threshold to 1 seconds (how long to wait after silence before stopping)
        recognizer.pause_threshold = 1

        try:
            # Listen for audio with a timeout and phrase time limit
            # timeout: how long to wait for speech to start
            # phrase_time_limit: maximum time to record after speech starts
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            
            # Check if 'serena' is in the recognized text (case-insensitive)
            if 'serena' in text.lower():
                print("Serena detected!")
                return True
            else:
                print("Serena not detected.")
                return False
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period.")
            return False
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return False
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return False

def voice_to_string():
    """
    Records human voice until silence is detected and converts it to a string.
    
    Returns:
        str: The recognized speech as text, or None if no speech was detected/recognized
    """
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Lower the energy threshold to make it more sensitive to quieter sounds
    recognizer.energy_threshold = 40
    # Set pause threshold to 1 second (how long to wait after silence before stopping)
    recognizer.pause_threshold = 2.4
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening for voice...")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        try:
            # Listen for audio with a timeout and phrase time limit
            # timeout: how long to wait for speech to start
            # phrase_time_limit: maximum time to record after speech starts
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            
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

if __name__ == "__main__":
    while True:
        text = voice_to_string()
        if text:
            print(f"Recognized text: {text}")
        else:
            print("Waiting for next attempt...")
            time.sleep(1)
