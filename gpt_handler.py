from openai import OpenAI
import httpx
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

redirect_url = os.getenv('gpt_redirect_url')
api_key = os.getenv('gpt_api_key')

if redirect_url:
    client = OpenAI(
        api_key=api_key,
        base_url=redirect_url,
        http_client=httpx.Client(
            base_url=redirect_url,
            follow_redirects=True,
        ),
    )
else:
    client = OpenAI(
        api_key=api_key
    )

def completion_response(model, system_prompt, user_prompt, chat_history = None, prefix = None, temperature=1.0):
    """
    Generate chat response using OpenAI API.
    :param model: The model name to use.
    :param system_prompt: System prompt message.
    :param user_prompt: User input prompt message.
    :param chat_history: Optional chat history as a dictionary.
    :param prefix: Optional prefix for response content.
    :param temperature: Controls randomness of generated text, default is 1.0.
    :return: Generated response content.
    """
    # Build messages list without empty dictionaries
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # If chat history is provided, append it to the messages
    if chat_history:
        if isinstance(chat_history, list):
            # If chat_history is a list of message dictionaries
            for message in chat_history:
                if isinstance(message, dict) and "role" in message and "content" in message:
                    messages.append({"role": message["role"], "content": message["content"]})
        elif isinstance(chat_history, dict):
            # If chat_history is a dictionary with role:content pairs
            for role, content in chat_history.items():
                messages.append({"role": role, "content": content})

    # Append user prompt 
    messages.append({"role": "user", "content": user_prompt})

    # If prefix is provided, append it to the messages
    if prefix:
        messages.append({"role": "assistant", "content": prefix})
    
    # Create chat completion
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    # Get response content and add prefix if needed
    content = response.choices[0].message.content
    return f"{prefix or ''}{content}"

if __name__ == "__main__":
  completion = completion_response(
      model="deepseek-r1-250528", 
      system_prompt="你是一位專業的小説作家，請根據以下需求撰寫文章：",
      user_prompt="請撰寫一個二百字以内的賽博朋克世界觀。"
  )
  print(completion)