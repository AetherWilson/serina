# Serina - Voice Assistant

A Python-based voice assistant that listens for the wake word "Serena", processes voice commands, and responds using AI-generated text converted to speech.
This is a self-project and also a toy project, expect slow update.
Feel free to suggest improvements or report bugs as I'm only a hobbyist.

## Features

- **Wake word detection**: Listens for "Serena" to activate
- **Speech-to-text**: Converts voice input to text using OpenAI Whisper
- **AI responses**: Uses OpenAI/DeepSeek API for intelligent responses
- **Text-to-speech**: High-quality voice synthesis using Microsoft Edge TTS
- **Continuous listening**: Runs in a loop for ongoing interaction
- **Configurable settings**: Easy-to-edit JSON settings file
- **Chat history**: Maintains conversation context with automatic pruning

## Requirements

- Python 3.7+
- Microphone and speakers
- Internet connection (for speech recognition and AI responses)

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv_serina
   .venv_serina\Scripts\activate  # On Windows
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API keys:
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your API keys:
     ```
     GPT_API_KEY=your_openai_api_key_here
     GPT_REDIRECT_URL=your_custom_endpoint_url_or_leave_empty
     ```

## Usage

1. Run the main program:
   ```bash
   python main.py
   ```

2. Wait for the program to start listening
3. Say "Serena" to activate the assistant (**Tip**: Say it twice for better detection)
4. When you hear "Yes?", speak your question or command
5. The assistant will process your input and respond with speech

**Note**: Due to current wake word detection limitations, you may need to say "Serena" twice for reliable activation. See the Debug section for more details and potential improvements.

## Project Structure

```
serina/
├── main.py              # Main application entry point
├── recorder.py          # Speech recognition and wake word detection
├── speaker.py           # Text-to-speech using Edge TTS
├── gpt_handler.py       # OpenAI API integration
├── json_handle.py       # Settings and chat history management
├── txt_handle.py        # Text file utilities
├── settings.json        # Configuration settings
├── chat_history.json    # Conversation history (auto-generated)
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Environment variables (API keys) - DO NOT COMMIT
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## File Descriptions

### `main.py`
The main application loop that:
- Listens for the wake word "Serena"
- Activates voice recording when detected
- Sends recognized text to AI for processing
- Converts AI response back to speech

### `recorder.py`
Contains two main functions:
- `listen_for_serena()`: Detects the wake word "Serena"
- `voice_to_string()`: Records and transcribes voice input

### `speaker.py`
Text-to-speech functionality using Microsoft Edge TTS:
- High-quality neural voices
- Supports multiple voice options (Jenny, Aria, Michelle)
- Plays audio directly without saving files

### `gpt_handler.py`
Handles communication with OpenAI/DeepSeek API:
- Sends user prompts to AI model
- Manages conversation context
- Returns AI-generated responses

### `json_handle.py`
Manages settings and chat history:
- Loads configuration from `settings.json`
- Saves and manages chat history with automatic pruning
- Provides universal functions for reading/writing settings

### `txt_handle.py`
Text file utilities for reading text files safely.

## Configuration

Serina uses a `settings.json` file for easy configuration. Edit this file to customize your experience:

```json
{
  "serina_language": "auto",
  "serina_voice_model": "en-US-AriaNeural", 
  "microphone_threshold": 80,
  "pause_threshold": 1
}
```

### Settings Explained

- **`serina_language`**: Speech recognition language
  - `"en"` - English only
  - `"zh"` - Chinese only  
  - `"auto"` - Auto-detect language
  
- **`serina_voice_model`**: Text-to-speech voice
  - `"en-US-AriaNeural"` - Female English (default)
  - `"en-US-JennyNeural"` - Female English (alternative)
  - `"en-US-MichelleNeural"` - Female English (alternative)
  - `"zh-CN-XiaoxiaoNeural"` - Female Chinese
  
- **`microphone_threshold`**: Microphone sensitivity (20-100)
  - Lower values = more sensitive
  - Higher values = less sensitive
  
- **`pause_threshold`**: Silence duration before stopping recording (seconds)
  - Lower values = faster response
  - Higher values = more patient listening

## Debug

### Microphone Threshold Issues

The `microphone_threshold` setting in `settings.json` controls how sensitive the microphone is to sound:

**Problem: Serina keeps saying "Serena not detected. Listening for voice..." repeatedly**
- **Solution**: Turn UP the `microphone_threshold` value in `settings.json`
- Try increasing from 80 to 100, 120, or higher
- This makes the microphone less sensitive to background noise

**Problem: Console doesn't show anything after you speak (no response within 2 seconds)**
- **Solution**: Turn DOWN the `microphone_threshold` value in `settings.json`
- Try decreasing from 80 to 60, 40, or lower  
- This makes the microphone more sensitive to your voice

**Example adjustments in `settings.json`:**
```json
{
  "microphone_threshold": 40,    // More sensitive (use if not detecting voice)
  "microphone_threshold": 120    // Less sensitive (use if too much background noise)
}
```

### Testing Your Settings

1. Edit `settings.json` and save the file
2. Restart the program: `python main.py`
3. Say "Serena" and observe the console output
4. Adjust the threshold based on the behavior described above

### Wake Word Detection Issues

**Current Limitation**: The wake word detection is not very reliable due to short timeout periods and sensitivity issues.

**Workaround**: **Say "Serena" twice** for better detection:
- First "Serena" - gets the system's attention
- Second "Serena" - usually gets detected and activates the assistant

**Why this happens**:
- Wake word detection uses a 1-second timeout for quick response
- Short timeout makes it miss longer or slower speech
- Background noise can interfere with detection

**Potential Improvements** (for developers):

1. **Increase wake word timeout**:
   ```python
   # In recorder.py, listen_for_serena() function
   text = voice_to_string(selected_language="en", recognizer=recognizer, timeout=3)  # Increase from 1 to 3
   ```

2. **Add multiple wake word variations**:
   ```python
   # Check for multiple variations
   wake_words = ['serena', 'sarina', 'serina', 'sirena']
   if text and any(word in text.lower() for word in wake_words):
   ```

3. **Implement continuous listening with voice activity detection**:
   - Use a more sophisticated voice activity detection system
   - Implement rolling buffer for continuous audio processing
   - Add confidence scoring for wake word detection

4. **Use dedicated wake word detection library**:
   - Consider libraries like `porcupine` or `snowboy` for better wake word detection
   - These are specifically designed for wake word detection vs general speech recognition

## Troubleshooting

### Common Issues

1. **"Could not understand the audio"**
   - Speak more clearly
   - Reduce background noise
   - Adjust `energy_threshold` in recorder.py

2. **"No speech detected"**
   - Check microphone permissions
   - Increase `timeout` values
   - Lower `energy_threshold`

3. **API Key errors**
   - Ensure `.env` file exists with correct API key
   - Check that variable names match: `GPT_API_KEY` and `GPT_REDIRECT_URL`
   - Verify `dotenv.load_dotenv()` is called

4. **Pygame messages**
   - These are suppressed by setting `PYGAME_HIDE_SUPPORT_PROMPT=1`

### Dependencies

If you encounter import errors, install missing packages:
```bash
pip install speech_recognition
pip install openai
pip install python-dotenv
pip install edge-tts
pip install pygame
pip install httpx
```

Or simply use:
```bash
pip install -r requirements.txt
```

## Security Note

- **Never commit your `.env` file** - it contains sensitive API keys
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Use `.env.example` as a template for setting up your environment
- If you accidentally commit API keys, regenerate them immediately

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve Serina!

## License

This project is open source. Feel free to use and modify as needed.
