#!/usr/bin/env python3
\"\"\"Test suite for WebAutomation.\"\"\"
import json
from web import web_automation, BrowserControllerError

def test_structured_extraction():
    print(\"Testing structured data extraction...\")
    web_automation.open_url(\"https://example.com\")
    data = web_automation.get_structured_data()
    print(json.dumps(data, indent=2))
    assert data[\"title\"]

def test_form_automation():
    print(\"Testing form filling (demo on example)...\")
    web_automation.open_url(\"https://example.com\")
    # Example form fill
    fields = {\"input[type='email']\": \"test@example.com\"}
    web_automation.fill_form(fields)
    print(\"Form filled successfully.\")

def test_links_tables():
    print(\"Testing links and tables...\")
    web_automation.open_url(\"https://example.com\")
    links = web_automation.extract_links()
    tables = web_automation.extract_tables()
    print(f\"Found {len(links)} links, {len(tables)} tables\")

if __name__ == \"__main__\": 
    try:
        test_structured_extraction()
        test_links_tables()
        test_form_automation()
        print(\"\\n✅ All WebAutomation tests PASSED!\")
    except Exception as e:
        print(f\"\\n❌ Test failed: {e}\")

