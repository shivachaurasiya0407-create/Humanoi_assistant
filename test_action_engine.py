#!/usr/bin/env python3
\"\"\"Test suite for ActionEngine.\"\"\"
import time
from automation.action_engine import action_engine

def test_find_element():
    ui_map = action_engine.detector.generate_ui_map()
    el = action_engine.find_element(ui_map, \"Desktop\", \"button\")
    print(f\"Test find: {el is not None}\")

def test_simple_plan():
    plan = [
        {\"action\": \"click\", \"target\": \"Start\"},
        {\"action\": \"type\", \"target\": \"search\", \"text\": \"test\"}
    ]
    result = action_engine.perform_action(plan)
    print(f\"Test plan: {result['success']}\")

if __name__ == \"__main__\":
    print(\"[TEST ACTION ENGINE]\")
    action_engine.debug_mode = True  # Confirm prompts
    test_find_element()
    print(\"Run interactive: action_engine.execute_ui_task('click on Desktop')\")
    task = input(\"Enter test task (or Enter to skip): \")
    if task:
        print(action_engine.execute_ui_task(task))
    print(\"Tests complete. Check logs for [ACTION ENGINE]\")

