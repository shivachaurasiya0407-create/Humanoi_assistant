#!/usr/bin/env python3
# Voice System Test Script for Humanoid AI Assistant

import os
print("1. Python path:", os.sys.executable)
print("2. Working dir:", os.getcwd())

print("\\n3. Testing imports...")
try:
    import sounddevice as sd
    print(" - sounddevice OK")
except ImportError as e:
    print(" - sounddevice FAILED:", e)

try:
    import numpy as np
    print(" - numpy OK")
except ImportError as e:
    print(" - numpy OK:", e)

try:
    from vosk import Model, KaldiRecognizer
    print(" - vosk OK")
except ImportError as e:
    print(" - vosk FAILED:", e)

try:
    import pyttsx3
    print(" - pyttsx3 OK")
except ImportError as e:
    print(" - pyttsx3 FAILED:", e)

print("\\n4. Vosk models:")
models = ['models/vosk-model-small-hi', 'models/vosk-model-small-en-in']
for m in models:
    if os.path.isdir(m):
        print(" - " + m + " OK")
    else:
        print(" - " + m + " MISSING")

print("\\n5. Audio devices:")
try:
    devices = sd.query_devices()
    mics = [d for d in devices if d['max_input_channels'] > 0]
    print(f" - Found {len(mics)} input devices")
    for d in mics[:3]:  # Top 3
        print(f"   - {d['name']} (ch: {d['max_input_channels']})")
except Exception as e:
    print(" - FAILED:", e)

print("\\n6. pyttsx3 voices test:")
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f" - Found {len(voices)} voices")
    for v in voices[:3]:
        print(f"   - {v.name} ({v.id})")
    print(" - Test speak: Listen for 'Voice test complete'")
    engine.say("Voice test complete. If you heard this, TTS works!")
    engine.runAndWait()
    print(" - TTS test complete")
except Exception as e:
    print(" - FAILED:", e)

print("\\nVoice test complete. Run 'python test_voice.py' and share output.")

