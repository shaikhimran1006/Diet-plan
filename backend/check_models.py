"""
Quick script to check available Google Gemini models
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("🔍 Checking available Google Gemini models...\n")

try:
    models = genai.list_models()
    
    print("✅ Available models that support generateContent:\n")
    
    compatible_models = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            compatible_models.append(model.name)
            print(f"  • {model.name}")
            print(f"    Display Name: {model.display_name}")
            print(f"    Description: {model.description[:100]}...")
            print()
    
    if compatible_models:
        print(f"\n✨ Found {len(compatible_models)} compatible model(s)")
        print(f"\n💡 Recommended model to use: {compatible_models[0]}")
    else:
        print("\n❌ No compatible models found!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Possible issues:")
    print("  1. Invalid API key")
    print("  2. API key doesn't have access to Gemini models")
    print("  3. Network connection issue")
    print("\n🔗 Get a new API key at: https://aistudio.google.com/app/apikey")
