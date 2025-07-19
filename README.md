# Serina - Voice Assistant

A Python-based voice assistant that listens for the wake word "Serena", processes voice commands, and responds using AI-generated text converted to speech.
This is a self-project and also a toy project, expect slow update.
Feel free to suggest improvements or report bugs as I'm only a hobbyist.

## Features

- **Wake word detection**: Listens for "Serena" to activate
- **Speech-to-text**: Converts voice input to text using Google Speech Recognition
- **AI responses**: Uses OpenAI/DeepSeek API for intelligent responses
- **Text-to-speech**: High-quality voice synthesis using Microsoft Edge TTS
- **Continuous listening**: Runs in a loop for ongoing interaction

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
3. Say "Serena" to activate the assistant
4. When you hear "Yes?", speak your question or command
5. The assistant will process your input and respond with speech

## Project Structure

```
serina/
├── main.py              # Main application entry point
├── recorder.py          # Speech recognition and wake word detection
├── speaker.py           # Text-to-speech using Edge TTS
├── gpt_handler.py       # OpenAI API integration
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

## Configuration

### Voice Settings
You can customize the voice in `speaker.py`:
```python
# Available voices:
# en-US-AriaNeural (default)
# en-US-JennyNeural  
# en-US-MichelleNeural
await play_tts_immediately(text, voice="en-US-JennyNeural")
```

### Speech Recognition Settings
Adjust sensitivity in `recorder.py`:
```python
recognizer.energy_threshold = 40    # Lower = more sensitive
recognizer.pause_threshold = 1.4    # Silence duration before stopping
```

### AI Model Settings
Change the AI model in `main.py`:
```python
response = gpt_handler.completion_response(
    model="deepseek-v3-250324",  # or "gpt-3.5-turbo", "gpt-4", etc.
    system_prompt="You are a helpful assistant.",
    user_prompt=recognized_text,
    temperature=1.0
)
```

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
