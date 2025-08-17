# Serina - Voice Assistant

A Python-based voice assistant that listens for the wake word "Serina", processes voice commands, and responds using AI-generated text converted to speech. Features professional console interface, OpenAI TTS integration, and pre-recorded audio support.

This is a self-project and also a toy project, expect slow updates.
Feel free to suggest improvements or report bugs as I'm only a hobbyist.

## ✨ Features

- **🎯 Wake word detection**: Listens for "Serina" to activate
- **🎤 Speech-to-text**: Converts voice input to text using OpenAI Whisper
- **🤖 AI responses**: Uses OpenAI/DeepSeek API for intelligent responses
- **🎵 TTS**: OpenAI TTS-1 API with multiple voice options (nova, alloy, echo, fable, onyx, shimmer)
- **📁 Pre-recorded audio**: Instant responses using pre-recorded audio files with smart folder organization
- **🔄 Continuous listening**: Runs in a loop for ongoing interaction
- **⚙️ Configurable settings**: Easy-to-edit JSON settings file
- **💬 Chat history**: Maintains conversation context with automatic pruning
- **🎨 Professional UI**: Clean console interface with timestamps and status indicators
- **🔀 Redirect URL support**: Custom API endpoints for proxy/redirect configurations
- **💾 MP3 export**: Save TTS to organized MP3 files for reuse

## 🆕 What's New

**Major Updates:**
- ✅ **OpenAI TTS Integration**: Replaced Edge TTS with OpenAI TTS-1 for better quality
- ✅ **Pre-recorded Audio Support**: Instant responses using pre-recorded MP3 files
- ✅ **Professional Console UI**: Clean interface with timestamps and status indicators
- ✅ **MP3 Export Feature**: Save any text as MP3 files with organized folder structure
- ✅ **Redirect URL Support**: Use custom API endpoints and proxies
- ✅ **Multiple Voice Options**: 6 different OpenAI voices to choose from
- ✅ **Async Architecture**: Non-blocking audio playback and processing
- ✅ **Enhanced Error Handling**: Graceful startup/shutdown and better error messages

**Technical Improvements:**
- Cleaner code organization with `speaker_api.py`
- Environment variable standardization (`gpt_api_key` format)
- Pygame message suppression for cleaner output
- Smart fallback systems for audio playback

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
     gpt_api_key=your_openai_api_key_here
     gpt_redirect_url=your_custom_endpoint_url_or_leave_empty
     ```

5. Create pre-recorded audio folder structure (optional):
   ```bash
   mkdir -p pre-recorded-audio/nova
   ```

## 🚀 Usage

1. Run the main program:
   ```bash
   python main.py
   ```

2. You'll see a professional interface like this:
   ```
   ============================================================
   🤖 SERINA - AI Voice Assistant
   ============================================================
   📅 Started: 2025-01-17 14:30:45
   🎯 Wake word: 'Serina'
   🎤 Ready to listen...
   ============================================================
   
   [14:30:45] ℹ️ Initializing wake word detector...
   [14:30:46] 👂 Listening for wake word 'Serina'...
   ```

3. Say "Serina" to activate the assistant
4. When you hear a pre-recorded response or see status updates, speak your question or command
5. The assistant will process your input and respond with speech

## 📁 Project Structure

```
serina/
├── main.py                    # Main application with professional console UI
├── recorder.py                # Advanced speech recognition and wake word detection
├── speaker_api.py             # OpenAI TTS integration with MP3 export capabilities
├── speaker.py                 # Legacy Edge TTS (still available)
├── gpt_handler.py             # OpenAI/DeepSeek API integration with redirect support
├── json_handle.py             # Settings and chat history management
├── txt_handle.py              # Text file utilities
├── personality.txt            # AI personality configuration
├── settings.json              # Configuration settings
├── chat_history.json          # Conversation history (auto-generated)
├── pre-recorded-audio/        # Organized audio file storage
│   ├── nova/                  # Pre-recorded responses for nova voice
│   ├── alloy/                 # Pre-recorded responses for alloy voice
│   └── [other-voices]/        # Additional voice folders
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Environment variables (API keys) - DO NOT COMMIT
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

## 📋 File Descriptions

### `main.py`
The main application with professional console interface:
- Clean timestamped status messages with emojis
- Listens for the wake word "Serina" 
- Uses pre-recorded audio for instant responses
- Graceful startup/shutdown with professional headers
- Integrated error handling and status tracking

### `speaker_api.py` ⭐ **NEW**
OpenAI TTS integration:
- **Multiple voice options**: nova, alloy, echo, fable, onyx, shimmer
- **TTS-1 model**: High-quality OpenAI text-to-speech
- **MP3 export**: Save responses to organized folder structure
- **Redirect URL support**: Custom API endpoints
- **Async support**: Non-blocking audio playback
- **Interactive testing**: Built-in voice testing interface

### `recorder.py`
Speech recognition and wake word detection:
- Optimized wake word detection for "Serina"
- Multiple fallback recognition methods
- Advanced microphone calibration
- Voice activity detection

### `speaker.py`
Legacy Microsoft Edge TTS (still available):
- High-quality neural voices
- Multiple voice options
- Direct audio playback

### `gpt_handler.py`
OpenAI/DeepSeek API integration:
- **Redirect URL support**: Use custom endpoints/proxies
- **Environment variable configuration**: Secure API key management
- Conversation context management
- Temperature and model selection

### `json_handle.py`
Settings and chat history management:
- Loads configuration from `settings.json`
- Chat history with automatic pruning
- Universal settings read/write functions

### `txt_handle.py`
Text file utilities for safe file reading.

### `personality.txt`
AI personality configuration file that defines how Serina responds.

## ⚙️ Configuration

### Environment Variables (.env)
```bash
gpt_api_key=your_openai_api_key_here
gpt_redirect_url=https://your-custom-endpoint.com/v1  # Optional for proxies
```

### Settings Configuration
Serina uses a `settings.json` file for configuration:

```json
{
  "serina_language": "auto",
  "serina_voice_model": "en-US-AriaNeural", 
  "microphone_threshold": 80,
  "pause_threshold": 1
}
```

### Pre-recorded Audio Setup ⭐ **NEW**
Create instant responses using pre-recorded audio:

1. **Create voice folders**:
   ```bash
   mkdir -p pre-recorded-audio/nova
   mkdir -p pre-recorded-audio/alloy
   # Add folders for other voices as needed
   ```

2. **Generate audio files using speaker_api.py**:
   ```bash
   python speaker_api.py
   # Choose option 4: "Save text to MP3 file"
   ```

3. **Example folder structure**:
   ```
   pre-recorded-audio/
   ├── nova/
   │   ├── yes.mp3
   │   ├── hello.mp3
   │   ├── listening.mp3
   │   └── whats_up.mp3
   └── alloy/
       ├── greeting.mp3
       └── response.mp3
   ```

4. **Automatic usage**: Serina will randomly select from available audio files in the `voice_to_use` folder (default: "nova")

### Settings Explained

- **`serina_language`**: Speech recognition language
  - `"en"` - English only
  - `"zh"` - Chinese only  
  - `"auto"` - Auto-detect language
  
- **`serina_voice_model`**: Legacy Edge TTS voice (when using speaker.py)
  - `"en-US-AriaNeural"` - Female English (default)
  - `"en-US-JennyNeural"` - Female English (alternative)
  - Note: When using speaker_api.py, voice is controlled by `voice_to_use` variable in main.py
  
- **`microphone_threshold`**: Microphone sensitivity (20-100)
  - Lower values = more sensitive
  - Higher values = less sensitive
  
- **`pause_threshold`**: Silence duration before stopping recording (seconds)
  - Lower values = faster response
  - Higher values = more patient listening

## 🎵 TTS Voice Options (OpenAI)

When using `speaker_api.py` (default), you have access to these OpenAI voices:

| Voice | Description | Best For |
|-------|-------------|----------|
| **nova** | Bright, energetic (default) | General conversation |
| **alloy** | Neutral, balanced | Professional responses |
| **echo** | Clear, articulate | Clear communication |
| **fable** | Warm, engaging | Storytelling |
| **onyx** | Deep, authoritative | Serious topics |
| **shimmer** | Soft, gentle | Calming responses |

**To change voice**: Edit the `voice_to_use` variable in `main.py`

## 🔧 Troubleshooting

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
   - Check variable names: `gpt_api_key` and `gpt_redirect_url`
   - Verify `dotenv.load_dotenv()` is called

4. **Pre-recorded audio not playing**
   - Check that `pre-recorded-audio/nova/` folder exists
   - Ensure audio files (.mp3, .wav, .ogg, .m4a) are present
   - Verify `voice_to_use` variable matches folder name

5. **Console output messy**
   - The new professional interface should be clean
   - If seeing pygame messages, check that suppression is working in speaker_api.py

### Dependencies

If you encounter import errors, install missing packages:
```bash
pip install speech_recognition openai python-dotenv pygame httpx edge-tts
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## 🎛️ Additional Features

### Custom API Endpoints
Use custom OpenAI-compatible endpoints by setting `gpt_redirect_url` in your `.env` file:
```bash
gpt_redirect_url=https://api.deepseek.com/v1
```

### MP3 Export Workflow
1. Run `python speaker_api.py`
2. Choose option 4: "Save text to MP3 file"
3. Enter text, voice, and settings
4. Files are automatically organized in `pre-recorded-audio/{voice}/`

### Voice Testing
Test different voices interactively:
```bash
python speaker_api.py
# Choose option 1 or 2 to test voices
```

## 🔒 Security Note

- **Never commit your `.env` file** - it contains sensitive API keys
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Use `.env.example` as a template for setting up your environment
- If you accidentally commit API keys, regenerate them immediately

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve Serina!

**Areas for contribution:**
- Better wake word detection algorithms
- Additional TTS voice providers
- Mobile app version
- GUI interface
- Voice training capabilities

## 📄 License

This project is open source. Feel free to use and modify as needed.
