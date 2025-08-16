import speech_recognition as sr
import numpy as np
import time
import threading
import queue
from collections import deque
import re

class WakeWordDetector:
    def __init__(self, wake_word="serina", confidence_threshold=0.7, buffer_duration=3.0):
        """
        Initialize wake word detector with optimized settings.
        
        Args:
            wake_word (str): The wake word to detect
            confidence_threshold (float): Minimum confidence for detection
            buffer_duration (float): Duration of audio buffer to analyze
        """
        self.wake_word = wake_word.lower()
        self.confidence_threshold = confidence_threshold
        self.buffer_duration = buffer_duration
        
        # Audio processing
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Optimize recognizer settings for wake word detection
        self.recognizer.energy_threshold = 300  # Higher threshold to reduce false positives
        self.recognizer.pause_threshold = 0.5   # Shorter pause for faster response
        self.recognizer.phrase_threshold = 0.3  # Minimum audio before considering speech
        self.recognizer.non_speaking_duration = 0.3  # Quick detection of silence
        
        # Detection history for loop prevention
        self.detection_history = deque(maxlen=10)
        self.last_detection_time = 0
        self.min_detection_interval = 2.0  # Minimum seconds between detections
        
        # Audio queue for continuous processing
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
        # Calibrate microphone
        self._calibrate_microphone()
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise."""
        print("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print("Microphone calibrated.")
    
    def _normalize_text(self, text):
        """Normalize text for better matching."""
        if not text:
            return ""
        
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', '', text.lower())
        
        # Handle common speech-to-text variations
        variations = {
            'serena': 'serina',
            'sarina': 'serina', 
            'serina': 'serina',
            'sirena': 'serina',
            'marina': 'serina',  # Common misrecognition
            'arena': 'serina',   # Common misrecognition
        }
        
        for variant, target in variations.items():
            text = text.replace(variant, target)
        
        return text.strip()
    
    def _calculate_similarity(self, text):
        """Calculate similarity score between detected text and wake word."""
        normalized_text = self._normalize_text(text)
        
        if not normalized_text:
            return 0.0
        
        # Direct match
        if self.wake_word in normalized_text:
            return 1.0
        
        # Fuzzy matching for partial matches
        words = normalized_text.split()
        best_score = 0.0
        
        for word in words:
            # Simple character-based similarity
            if len(word) >= 3:  # Only consider words with 3+ characters
                common_chars = sum(1 for c in self.wake_word if c in word)
                similarity = common_chars / max(len(self.wake_word), len(word))
                best_score = max(best_score, similarity)
        
        return best_score
    
    def _is_loop_detection(self):
        """Prevent rapid repeated detections (loop detection)."""
        current_time = time.time()
        
        # Check if minimum interval has passed
        if current_time - self.last_detection_time < self.min_detection_interval:
            return True
        
        # Check for rapid successive detections in history
        recent_detections = [t for t in self.detection_history if current_time - t < 5.0]
        if len(recent_detections) >= 3:  # More than 3 detections in 5 seconds
            return True
        
        return False
    
    def _record_detection(self):
        """Record a successful detection."""
        current_time = time.time()
        self.last_detection_time = current_time
        self.detection_history.append(current_time)
    
    def wake_word_detect_new(self):
        """
        Single detection attempt with optimized processing.
        
        Returns:
            bool: True when wake word is detected with high confidence
        """
        try:
            with self.microphone as source:
                # Quick listen with short timeout for responsiveness
                audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=2.0)
            
            # Use Whisper for better accuracy (free and offline)
            try:
                text = self.recognizer.recognize_whisper(audio, model="tiny")  # Tiny model for speed
            except Exception:
                # Fallback to Google (requires internet but free for limited use)
                try:
                    text = self.recognizer.recognize_google(audio, language="en-US")
                except Exception:
                    return False
            
            if text:
                similarity_score = self._calculate_similarity(text)
                
                # Debug output (can be removed in production)
                if similarity_score > 0.3:  # Show potential matches
                    print(f"Detected: '{text}' (similarity: {similarity_score:.2f})")
                
                # Check confidence and loop detection
                if similarity_score >= self.confidence_threshold:
                    if not self._is_loop_detection():
                        self._record_detection()
                        return True
                    else:
                        print("Loop detection: Ignoring rapid successive detection")
            
            return False
            
        except sr.WaitTimeoutError:
            # No speech detected - this is normal, not an error
            return False
        except Exception as e:
            print(f"Detection error: {e}")
            return False
    
    def continuous_detection(self):
        """
        Continuous wake word detection with optimized loop.
        """
        print(f"Starting continuous wake word detection for '{self.wake_word}'...")
        print("Optimized for: Free recognition, High accuracy, Low latency")
        print("Features: Loop detection, Fuzzy matching, Multiple fallbacks")
        print("-" * 60)
        
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while True:
            try:
                if self.wake_word_detect_new():
                    print("🎯 WAKE WORD HEARD!")
                    print("-" * 30)
                    consecutive_errors = 0  # Reset error counter on success
                else:
                    consecutive_errors = 0  # Reset on normal operation
                
                # Small delay to prevent CPU overload while maintaining responsiveness
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\nDetection stopped by user.")
                break
            except Exception as e:
                consecutive_errors += 1
                print(f"Error in continuous detection: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"Too many consecutive errors ({consecutive_errors}). Stopping.")
                    break
                
                # Brief pause before retry
                time.sleep(0.5)

def record_voice_to_string(timeout=10, phrase_time_limit=None, energy_threshold=300, pause_threshold=0.8):
    """
    Records voice on call and converts to string until user stops speaking.
    
    Args:
        timeout (int): Maximum time to wait for speech to start (seconds)
        phrase_time_limit (int): Maximum time to record after speech starts (None = no limit)
        energy_threshold (int): Microphone sensitivity (higher = less sensitive)
        pause_threshold (float): Silence duration before stopping recording (seconds)
    
    Returns:
        str: The recognized speech as text, or None if no speech detected/recognized
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Configure recognizer settings
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = 0.3  # Minimum audio before considering speech
    recognizer.non_speaking_duration = 0.5  # How long to wait after speech ends
    
    try:
        # Calibrate for ambient noise
        print("Adjusting for ambient noise...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
        
        print("Listening for voice... (speak now)")
        
        with microphone as source:
            # Listen for audio
            audio = recognizer.listen(
                source, 
                timeout=timeout, 
                phrase_time_limit=phrase_time_limit
            )
        
        print("Processing speech...")
        
        # Try Whisper first (offline, free, high accuracy)
        try:
            text = recognizer.recognize_whisper(audio, model="base")
            print(f"✓ Whisper recognized: '{text}'")
            return text
            
        except Exception as whisper_error:
            print(f"Whisper failed: {whisper_error}")
            
            # Fallback to Google Speech Recognition
            try:
                text = recognizer.recognize_google(audio, language="en-US")
                print(f"✓ Google recognized: '{text}'")
                return text
                
            except Exception as google_error:
                print(f"Google fallback failed: {google_error}")
                
                # Final fallback to Google with auto language detection
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"✓ Google (auto-lang) recognized: '{text}'")
                    return text
                    
                except Exception as final_error:
                    print(f"All recognition methods failed: {final_error}")
                    return None
    
    except sr.WaitTimeoutError:
        print("⏱️ No speech detected within timeout period")
        return None
        
    except sr.UnknownValueError:
        print("❌ Could not understand the audio")
        return None
        
    except Exception as e:
        print(f"❌ Error during voice recording: {e}")
        return None

def wake_word_detect_new():
    """
    Standalone function for single wake word detection.
    
    Returns:
        bool: True when wake word is detected
    """
    detector = WakeWordDetector()
    return detector.wake_word_detect_new()

if __name__ == "__main__":
    print("=== Advanced Wake Word Detection System ===")
    print("Features:")
    print("✓ Free recognition (Whisper + Google fallback)")
    print("✓ High accuracy with fuzzy matching")
    print("✓ Low latency (optimized timeouts)")
    print("✓ Loop detection prevention")
    print("✓ Ambient noise calibration")
    print("✓ Multiple recognition engine fallbacks")
    print()
    
    # Ask user which mode to run
    print("Choose mode:")
    print("1. Wake word detection (continuous)")
    print("2. Voice recording test (single)")
    print("3. Combined demo (wake word + voice recording)")
    
    try:
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice == "1":
            # Wake word detection mode
            detector = WakeWordDetector(
                wake_word="serina",
                confidence_threshold=0.7,
                buffer_duration=3.0
            )
            detector.continuous_detection()
            
        elif choice == "2":
            # Voice recording test mode
            print("\n=== Voice Recording Test ===")
            print("Testing record_voice_to_string() function...")
            
            while True:
                input("\nPress Enter to start recording (or Ctrl+C to quit)...")
                result = record_voice_to_string(
                    timeout=10,           # Wait up to 10 seconds for speech
                    phrase_time_limit=30, # Record up to 30 seconds
                    energy_threshold=300, # Microphone sensitivity
                    pause_threshold=1.0   # Stop after 1 second of silence
                )
                
                if result:
                    print(f"📝 Final result: '{result}'")
                else:
                    print("🔇 No speech detected or recognition failed")
                
        elif choice == "3":
            # Combined demo mode
            print("\n=== Combined Demo ===")
            print("Say 'Serina' to activate, then speak your message...")
            
            detector = WakeWordDetector(wake_word="serina", confidence_threshold=0.7)
            
            while True:
                print("\n👂 Listening for wake word 'Serina'...")
                
                if detector.wake_word_detect_new():
                    print("🎯 WAKE WORD HEARD!")
                    print("🎤 Now recording your message...")
                    
                    message = record_voice_to_string(
                        timeout=5,
                        phrase_time_limit=20,
                        pause_threshold=1.5
                    )
                    
                    if message:
                        print(f"📝 You said: '{message}'")
                    else:
                        print("🔇 No message detected")
                    
                    print("-" * 50)
                
                time.sleep(0.1)  # Small delay to prevent CPU overload
        else:
            print("Invalid choice. Exiting.")
            
    except KeyboardInterrupt:
        print("\n👋 Program terminated by user.")
    except Exception as e:
        print(f"System error: {e}")
        print("\nTroubleshooting:")
        print("1. Check microphone permissions")
        print("2. Ensure microphone is connected")
        print("3. Try adjusting confidence_threshold")
        print("4. Check internet connection for Google fallback")
