import json
import os

def read_settings(setting_name):
    """
    Universal function to read any setting from settings.json
    
    Args:
        setting_name (str): Name of the setting to read
    
    Returns:
        Any: The setting value, or default value if not found
    """
    settings_file = "settings.json"
    
    # Default settings
    defaults = {
        "serina_language": "en",
        "serina_voice_model": "en-US-AriaNeural",
        "microphone_threshold": 40,
        "pause_threshold": 1.4
    }
    
    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Return the requested setting or its default
            return settings.get(setting_name, defaults.get(setting_name))
        else:
            print(f"Settings file {settings_file} not found. Using default value for {setting_name}.")
            return defaults.get(setting_name)
            
    except Exception as e:
        print(f"Error reading settings: {e}. Using default value for {setting_name}.")
        return defaults.get(setting_name)

def write_settings(setting_name, value):
    """
    Write a setting value to settings.json
    
    Args:
        setting_name (str): Name of the setting
        value (Any): Value to set
    
    Returns:
        bool: True if successful, False otherwise
    """
    settings_file = "settings.json"
    
    try:
        # Load existing settings
        settings = {}
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        
        # Update the setting
        settings[setting_name] = value
        
        # Save back to file
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        print(f"Setting '{setting_name}' updated to '{value}'")
        return True
        
    except Exception as e:
        print(f"Error writing setting: {e}")
        return False

def write_chat_history(messages, file_path="chat_history.json", max_messages=7):
    """
    Write chat history to a JSON file, maintaining a maximum number of messages.
    Deletes oldest messages when limit is exceeded.
    
    Args:
        messages (list): List of new messages to add.
        file_path (str): Path to the JSON file to write to. Defaults to "chat_history.json".
        max_messages (int): Maximum number of messages to keep. Defaults to 7.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Read existing chat history
        existing_messages = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_messages = json.load(f)
        
        # Add new messages to existing ones
        all_messages = existing_messages + messages
        
        # Keep only the last max_messages
        if len(all_messages) > max_messages:
            all_messages = all_messages[-max_messages:]
        
        # Write all messages back to JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_messages, f, indent=2, ensure_ascii=False)
        
        print(f"Chat history updated. Keeping {len(all_messages)} messages (max: {max_messages})")
        return True
        
    except Exception as e:
        print(f"Error writing chat history: {e}")
        return False

def read_chat_history(file_path="chat_history.json"):
    """
    Read chat history from a file.

    Args:
        file_path (str): Path to the file to read. Defaults to "chat_history.json".

    Returns:
        list: List of messages, or empty list if file not found or empty.
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            return messages
        else:
            print(f"Chat history file {file_path} not found. Making one.")
            return []

    except Exception as e:
        print(f"Error reading chat history: {e}")
        return []

if __name__ == "__main__":
    # Test the functions
    print("Current settings:")
    print(f"Language: {read_settings('serina_language')}")
    print(f"Voice model: {read_settings('serina_voice_model')}")
    print(f"Microphone threshold: {read_settings('microphone_threshold')}")
    print(f"Pause threshold: {read_settings('pause_threshold')}")
