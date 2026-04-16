import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

# Get HF_TOKEN from environment
HF_TOKEN = os.getenv('HF_TOKEN')

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env file")

print(f"HF_TOKEN: {HF_TOKEN[:20]}")

# Initialize the InferenceClient
client = InferenceClient(api_key=HF_TOKEN)

# Conversation history
messages = []

def chat(user_message):
    """Send a message and get a response from the model"""
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b:groq",
            messages=messages,
        )
        
        assistant_message = completion.choices[0].message.content
        messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main chatbot loop"""
    print("\n" + "="*50)
    print("Welcome to HF GPT-OSS Chatbot!")
    print("Type 'exit' to quit")
    print("="*50 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("\nBot: Thinking...", end="", flush=True)
        response = chat(user_input)
        print("\rBot: " + response + "\n")

if __name__ == "__main__":
    main()
