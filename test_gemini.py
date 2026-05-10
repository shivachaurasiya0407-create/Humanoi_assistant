#!/usr/bin/env python3
"""Test Google Gemini API connectivity."""

from dotenv import load_dotenv
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

load_dotenv()

api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_GEMINI_API_KEY not set in environment")
    sys.exit(1)

print(f"API Key found: {api_key[:20]}...")

url = "https://generativelanguage.googleapis.com/v1beta/models"
full_url = url + "?" + urllib.parse.urlencode({"key": api_key})

print(f"Testing endpoint: {url}")

try:
    req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read().decode("utf-8")
        print(f"\n✓ SUCCESS: Gemini API is accessible")
        print(f"HTTP Status: {resp.status}")
        print(f"\nResponse preview:\n{data[:500]}")
except urllib.error.HTTPError as err:
    body = err.read().decode("utf-8", errors="ignore")
    print(f"\n✗ ERROR: HTTP {err.code}")
    print(f"Response: {body[:500]}")
except urllib.error.URLError as err:
    print(f"\n✗ NETWORK ERROR: {err.reason}")
except Exception as err:
    print(f"\n✗ UNEXPECTED ERROR: {err}")
    import traceback
    traceback.print_exc()
