import os
import asyncio
import google.generativeai as genai
from google.genai import Client # Import the Client for async usage
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GOOGLE_API_KEY_HERE":
    print("CRITICAL ERROR: GEMINI_API_KEY is missing or invalid. Exiting.")
    exit(1)

# genai.configure(api_key=GEMINI_API_KEY) # Removed global configure

async def test_gemini_basic():
    print(f"GEMINI_API_KEY loaded: {GEMINI_API_KEY[:5]}... (length: {len(GEMINI_API_KEY)})")
    
    # Pass the API key directly to the Client constructor
    async with Client(api_key=GEMINI_API_KEY).aio as aclient:
        print("Gemini async client initialized with explicit API key.")

        try:
            print("Calling generate_content with a simple prompt...")
            response = await aclient.models.generate_content(
                model='gemini-2.5-flash', # Specify the model name directly
                contents="Hello, Gemini!"
            )
            print("Received response from Gemini API.")
            print(f"Response text: {response.text}")
            print("Basic Gemini test successful!")
        except Exception as e:
            print(f"Error during basic Gemini test: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini_basic())
