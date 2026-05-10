from plugins.plugin_loader import get_loader

def test_plugin_interface():
    print("--- Initializing Plugin Loader ---")
    loader = get_loader()
    plugins = loader.get_plugins()
    
    print(f"\n--- Validated Plugins Found: {len(plugins)} ---")
    for p in plugins:
        print(f"Name: {p['name']}, Actions: {p['actions']}")
    
    print("\n--- Testing Standardized Weather Plugin ---")
    weather_result = loader.execute_plugin("weather_plugin", "get_weather", {"location": "Delhi"})
    print(f"Weather Result: {weather_result}")

    print("\n--- Testing Standardized File Plugin ---")
    file_result = loader.execute_plugin("file_plugin", "list_files", {"path": "."})
    print(f"File List Status: {file_result.get('status')}")
    print(f"File Count: {len(file_result.get('result', []))}")

    print("\n--- Testing Invalid Action Handling ---")
    invalid_result = loader.execute_plugin("weather_plugin", "fly_to_moon", {})
    print(f"Invalid Action Result: {invalid_result}")

if __name__ == "__main__":
    test_plugin_interface()
