"""
Eye-Tracking Demo Script
Demonstrates practical usage of the simulated eye-tracking system.
"""

import time
import logging
from automation.human_mouse import human_mouse, eye_tracker
from vision.ui_detector import YOLOUIDetector

def demo_basic_gaze():
    """Demonstrate basic gaze tracking."""
    print("=== Basic Gaze Tracking Demo ===")

    # Start eye tracking
    eye_tracker.start_tracking(mode='manual')
    print("Eye tracking started in manual mode")

    # Simulate looking at different screen areas
    gaze_points = [
        (200, 150, "Top-left area"),
        (800, 150, "Top-right area"),
        (500, 400, "Center screen"),
        (200, 600, "Bottom-left area"),
        (800, 600, "Bottom-right area")
    ]

    for x, y, description in gaze_points:
        print(f"Gazing at {description} ({x}, {y})")
        eye_tracker.gaze_at_position(x, y, fixation_time=0.3)
        time.sleep(0.5)

    eye_tracker.stop_tracking()
    print("Basic gaze demo completed\n")

def demo_ui_integration():
    """Demonstrate UI detection integration."""
    print("=== UI Integration Demo ===")

    ui_detector = YOLOUIDetector()

    try:
        # Detect UI elements
        print("Detecting UI elements...")
        elements = ui_detector.generate_ui_map()

        if elements:
            print(f"Found {len(elements)} UI elements")

            # Set focus areas for eye tracker
            eye_tracker.from_ui_elements(elements, eye_tracker.get_screen_size())

            # Start tracking
            eye_tracker.start_tracking(mode='auto')

            # Look at first few elements
            for i, area in enumerate(eye_tracker.current_focus_areas[:3]):
                print(f"Gazing at element {i+1}: {area.label} ({area.element_type})")
                eye_tracker.gaze_to(area, fixation_time=0.4)
                time.sleep(0.3)

            eye_tracker.stop_tracking()
        else:
            print("No UI elements detected")

    except Exception as e:
        print(f"UI integration demo failed: {e}")

    print("UI integration demo completed\n")

def demo_scanning_patterns():
    """Demonstrate different scanning patterns."""
    print("=== Scanning Patterns Demo ===")

    patterns = ['horizontal', 'vertical', 'zigzag']

    for pattern in patterns:
        print(f"Executing {pattern} scan...")
        eye_tracker.scan_screen(pattern=pattern, bounds=(100, 100, 800, 600))
        time.sleep(0.5)

    print("Scanning patterns demo completed\n")

def demo_task_driven():
    """Demonstrate task-driven gaze prediction."""
    print("=== Task-Driven Gaze Demo ===")

    # Simulate a login task
    tasks = ["login", "username", "password", "submit"]

    eye_tracker.start_tracking(mode='task_driven')

    for task in tasks:
        print(f"Setting task context: {task}")
        eye_tracker.set_task_context(task)

        # Simulate finding and gazing at relevant elements
        # In real usage, this would be integrated with action planning
        eye_tracker.update(task_context=task)
        time.sleep(0.3)

    eye_tracker.stop_tracking()
    print("Task-driven demo completed\n")

def demo_statistics():
    """Show tracking statistics."""
    print("=== Tracking Statistics ===")

    stats = eye_tracker.get_tracking_stats()
    print(f"Tracking active: {stats['is_tracking']}")
    print(f"Tracking mode: {stats['tracking_mode']}")
    print(f"Focus areas: {stats['num_focus_areas']}")

    gaze_stats = stats['gaze_stats']
    print(f"Total fixations: {gaze_stats['total_fixations']}")
    print(f"Average fixation duration: {gaze_stats['avg_fixation_duration']:.2f}s")
    print(f"Gaze history length: {gaze_stats['gaze_history_length']}")

    print("Statistics demo completed\n")

def main():
    """Run all eye-tracking demos."""
    print("Eye-Tracking System Demo")
    print("=" * 40)

    # Configure logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise

    try:
        demo_basic_gaze()
        demo_ui_integration()
        demo_scanning_patterns()
        demo_task_driven()
        demo_statistics()

        print("All demos completed successfully!")

    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo failed: {e}")
    finally:
        # Ensure tracking is stopped
        eye_tracker.stop_tracking()
        eye_tracker.reset()

if __name__ == "__main__":
    main()