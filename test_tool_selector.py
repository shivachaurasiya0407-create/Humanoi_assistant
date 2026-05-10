from agent.agent_controller import AgentController
import json

def test_tool_selection():
    controller = AgentController()
    
    print("--- Testing AI Tool Selection (Weather) ---")
    # This should trigger ToolSelector
    result = controller.run("What is the weather in Tokyo?")
    
    print(f"Success: {result['success']}")
    if result['execution_results']:
        print(f"Tool Result: {result['execution_results'][0]['output']}")
    else:
        print(f"Error: {result.get('error')}")

    print("\n--- Testing Fallback (General Task) ---")
    # This should NOT trigger ToolSelector (likely) and go to TaskPlanner
    result = controller.run("Open notepad and write hello world")
    print(f"Plan steps: {len(result['plan'])}")
    print(f"First action: {result['plan'][0]['action']}")

if __name__ == "__main__":
    test_tool_selection()
