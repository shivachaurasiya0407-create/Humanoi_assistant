"""
Test script for the simulated eye-tracking system.
Demonstrates integration with human mouse and UI detection.
"""

import time
import logging
from automation.human_mouse import human_mouse, eye_tracker
from vision.ui_detector import YOLOUIDetector

def test_eye_tracker():
    """Test basic eye-tracking functionality."""
    print("Testing Eye-Tracking System...")

    # Initialize components
    ui_detector = YOLOUIDetector()

    # Test gaze tracking
    print("1. Testing gaze tracking...")
    eye_tracker.start_tracking(mode='auto')

    # Simulate gaze to different positions
    positions = [(100, 100), (500, 300), (800, 600), (300, 200)]
    for x, y in positions:
        print(f"   Gazing at ({x}, {y})")
        eye_tracker.gaze_at_position(x, y, fixation_time=0.5)
        time.sleep(0.2)

    # Test UI element detection and gaze
    print("2. Testing UI detection integration...")
    try:
        elements = ui_detector.generate_ui_map()
        if elements:
            print(f"   Detected {len(elements)} UI elements")
            # Gaze at first element
            first_element = elements[0]
            eye_tracker.set_task_context(first_element.get('text', ''))
            eye_tracker.gaze_to(eye_tracker.current_focus_areas[0])
        else:
            print("   No UI elements detected")
    except Exception as e:
        print(f"   UI detection failed: {e}")

    # Test scanning patterns
    print("3. Testing scanning patterns...")
    eye_tracker.scan_screen(pattern='horizontal')
    time.sleep(0.5)
    eye_tracker.scan_screen(pattern='vertical')

    # Get statistics
    stats = eye_tracker.get_tracking_stats()
    print(f"4. Tracking statistics: {stats}")

    eye_tracker.stop_tracking()
    print("Eye-tracking test completed!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_eye_tracker()