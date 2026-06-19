import os
import sys
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Check for API key before importing the SDK to give a quick user-friendly message
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key or api_key == "your_actual_api_key_here":
    print("\n\033[91m[Error] GEMINI_API_KEY not found in environment.\033[0m")
    print("Please follow these steps:")
    print("1. Duplicate '.env.template' and rename it to '.env'")
    print("2. Get a free API Key from Google AI Studio: https://aistudio.google.com/")
    print("3. Paste your key into the '.env' file: GEMINI_API_KEY=your_key")
    sys.exit(1)

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("\n\033[91m[Error] Google Gen AI SDK not installed.\033[0m")
    print("Please install dependencies using: pip install -r requirements.txt")
    sys.exit(1)

def main():
    # Initialize the client
    # genai.Client() automatically picks up GEMINI_API_KEY from environment
    client = genai.Client()
    
    # Using the recommended model for chat: gemini-2.5-flash
    model_name = "gemini-2.5-flash"
    
    # Configure default system instruction (personality)
    config = types.GenerateContentConfig(
        system_instruction="You are a helpful, smart, and friendly AI assistant. Answer the user's questions clearly."
    )
    
    print("\033[94m==================================================\033[0m")
    print("\033[92m              Gemini AI Chat Assistant             \033[0m")
    print("\033[94m==================================================\033[0m")
    print(f"Model: {model_name}")
    print("Commands: type 'exit' or 'quit' to end the chat.")
    print("\033[94m--------------------------------------------------\033[0m\n")

    try:
        # Create a new stateful chat session
        chat = client.chats.create(model=model_name, config=config)
    except Exception as e:
        print(f"\033[91mFailed to start chat session: {e}\033[0m")
        sys.exit(1)

    while True:
        try:
            # Get user input
            user_input = input("\033[92mYou > \033[0m").strip()
            
            # Check for exit commands
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("\n\033[93mGoodbye!\033[0m")
                break
                
            print("\033[94mAI > \033[0m", end="", flush=True)
            
            # Send message and stream response for a dynamic feel
            response_stream = chat.send_message_stream(user_input)
            for chunk in response_stream:
                print(chunk.text, end="", flush=True)
            print("\n") # New line after stream ends
            
        except KeyboardInterrupt:
            print("\n\n\033[93mGoodbye! (Chat terminated)\033[0m")
            break
        except Exception as e:
            print(f"\n\033[91mError: {e}\033[0m\n")

if __name__ == "__main__":
    main()
