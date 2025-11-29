import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment.")
    exit(1)

genai.configure(api_key=api_key)

def test_model(model_name):
    print(f"Testing model: {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, reply with 'OK' if you can hear me.")
        print(f"Success! Response: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"Failed to use {model_name}. Error: {e}")
        return False

print("--- Checking Gemini 1.5 Availability ---")
flash_ok = test_model('gemini-1.5-flash')
pro_ok = test_model('gemini-1.5-pro')

if not flash_ok and not pro_ok:
    print("\nListing available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
