#!/usr/bin/env python3
"""
Quick test script to verify API configurations.
Tests both Google Gemini API and ElevenLabs API.
"""

import sys
from dotenv import load_dotenv
import os

load_dotenv()

def test_gemini_api():
    """Test Google Gemini API connection."""
    print("=" * 60)
    print("Testing Google Gemini API...")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        print("❌ GOOGLE_GEMINI_API_KEY not found in environment")
        return False
    
    print(f"✓ API Key found: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("✓ Sending test request to Gemini API...")
        response = model.generate_content("Reply with just 'OK'")
        
        if response and response.text:
            print(f"✓ Gemini API response: {response.text.strip()}")
            print("✅ Google Gemini API is working!")
            return True
        else:
            print("❌ No response from Gemini API")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_elevenlabs_api():
    """Test ElevenLabs API connection."""
    print("\n" + "=" * 60)
    print("Testing ElevenLabs API...")
    print("=" * 60)
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")
    
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not found in environment")
        return False
    
    if not voice_id:
        print("❌ ELEVENLABS_VOICE_ID not found in environment")
        return False
    
    print(f"✓ API Key found: {api_key[:10]}...{api_key[-5:]}")
    print(f"✓ Voice ID found: {voice_id}")
    
    try:
        import requests
        
        # Test by making a simple TTS request
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": "Hello, this is a test.",
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.5,
            }
        }
        
        print("✓ Sending test request to ElevenLabs API...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"✓ ElevenLabs API responded with status {response.status_code}")
            print("✅ ElevenLabs API is working!")
            return True
        else:
            print(f"❌ ElevenLabs API returned status {response.status_code}")
            try:
                error = response.json()
                print(f"   Error details: {error}")
            except:
                print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("API Configuration Test Script")
    print("=" * 60)
    
    gemini_ok = test_gemini_api()
    elevenlabs_ok = test_elevenlabs_api()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Google Gemini API: {'✅ WORKING' if gemini_ok else '❌ NOT WORKING'}")
    print(f"ElevenLabs API:    {'✅ WORKING' if elevenlabs_ok else '❌ NOT WORKING'}")
    
    if gemini_ok and elevenlabs_ok:
        print("\n🎉 All APIs are configured correctly!")
        print("You can now run the main application with: python main.py")
        return 0
    else:
        print("\n⚠️  Some APIs are not working. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())