#!/usr/bin/env python3
"""
Test script to verify the SQLite database integration for the chat system.
This script tests all database operations without requiring an OpenAI API key.
"""

import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chat_engine.memory import DatabaseManager, ConversationMemory, MemoryManager


def test_database_manager():
    """Test the DatabaseManager class."""
    print("=" * 60)
    print("Testing DatabaseManager")
    print("=" * 60)

    # Use a test database
    test_db = "test_chat_memory.db"

    # Clean up any existing test database
    if os.path.exists(test_db):
        os.remove(test_db)

    # Create database manager
    db_manager = DatabaseManager(test_db)
    print(f"✓ Database created at: {test_db}")

    # Test save_message
    msg_id1 = db_manager.save_message("user", "Hello, how are you?")
    msg_id2 = db_manager.save_message("assistant", "I'm doing well, thank you!")
    msg_id3 = db_manager.save_message("user", "What's the weather like?")

    assert msg_id1 is not None, "Failed to save user message"
    assert msg_id2 is not None, "Failed to save assistant message"
    assert msg_id3 is not None, "Failed to save second user message"
    print(f"✓ Saved 3 messages with IDs: {msg_id1}, {msg_id2}, {msg_id3}")

    # Test load_history
    messages = db_manager.load_history()
    assert len(messages) == 3, f"Expected 3 messages, got {len(messages)}"
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
    assert messages[2]["role"] == "user"
    print(f"✓ Loaded {len(messages)} messages from database")

    # Test load with limit
    messages_limited = db_manager.load_history(limit=2)
    assert len(messages_limited) == 2, f"Expected 2 messages, got {len(messages_limited)}"
    print(f"✓ Loaded {len(messages_limited)} messages with limit=2")

    # Test get_message_count
    count = db_manager.get_message_count()
    assert count == 3, f"Expected 3 messages, got {count}"
    print(f"✓ Message count: {count}")

    # Test get_user_message_count
    user_count = db_manager.get_user_message_count()
    assert user_count == 2, f"Expected 2 user messages, got {user_count}"
    print(f"✓ User message count: {user_count}")

    # Test get_assistant_message_count
    assistant_count = db_manager.get_assistant_message_count()
    assert assistant_count == 1, f"Expected 1 assistant message, got {assistant_count}"
    print(f"✓ Assistant message count: {assistant_count}")

    # Test clear_all_messages
    deleted = db_manager.clear_all_messages()
    assert deleted == 3, f"Expected 3 deleted, got {deleted}"
    count_after_clear = db_manager.get_message_count()
    assert count_after_clear == 0, f"Expected 0 after clear, got {count_after_clear}"
    print(f"✓ Cleared {deleted} messages, database now empty")

    # Test invalid role
    invalid_result = db_manager.save_message("invalid_role", "Test")
    assert invalid_result is None, "Should return None for invalid role"
    print("✓ Invalid role correctly rejected")

    # Test empty content
    empty_result = db_manager.save_message("user", "")
    assert empty_result is None, "Should return None for empty content"
    print("✓ Empty content correctly rejected")

    # Close the database
    db_manager.close()
    print("✓ Database connection closed")

    # Clean up test database
    if os.path.exists(test_db):
        os.remove(test_db)
    # Also remove WAL and SHM files if they exist
    for ext in ['-wal', '-shm']:
        wal_file = test_db + ext
        if os.path.exists(wal_file):
            os.remove(wal_file)

    print("\nDatabaseManager tests passed! ✓\n")


def test_conversation_memory():
    """Test the ConversationMemory class with SQLite persistence."""
    print("=" * 60)
    print("Testing ConversationMemory")
    print("=" * 60)

    test_db = "test_conversation_memory.db"

    # Clean up any existing test database
    if os.path.exists(test_db):
        os.remove(test_db)

    # Create conversation memory with auto_load
    memory = ConversationMemory(
        system_prompt="You are a helpful assistant.",
        db_path=test_db,
        auto_load=True,
        max_history_load=50
    )
    print("✓ ConversationMemory initialized")

    # Add messages
    memory.add_user_message("Hello!")
    memory.add_assistant_message("Hi there! How can I help you?")
    memory.add_user_message("Tell me a joke.")
    memory.add_assistant_message("Why did the chicken cross the road? To get to the other side!")

    print("✓ Added 4 messages (2 user, 2 assistant)")

    # Verify messages are saved
    messages = memory.get_messages()
    assert len(messages) == 5, f"Expected 5 messages (including system), got {len(messages)}"
    assert messages[0]["role"] == "system"
    print(f"✓ Memory contains {len(messages)} messages")

    # Test get_last_n_messages
    last_2 = memory.get_last_n_messages(2)
    assert len(last_2) == 2
    print(f"✓ get_last_n_messages(2) returned {len(last_2)} messages")

    # Test counts
    user_count = memory.get_user_messages_count()
    assistant_count = memory.get_assistant_messages_count()
    assert user_count == 2, f"Expected 2 user messages, got {user_count}"
    assert assistant_count == 2, f"Expected 2 assistant messages, got {assistant_count}"
    print(f"✓ User: {user_count}, Assistant: {assistant_count}")

    # Test is_empty
    assert not memory.is_empty(), "Memory should not be empty"
    print("✓ is_empty() returns False")

    # Test clear
    memory.clear()
    assert memory.is_empty(), "Memory should be empty after clear"
    messages_after_clear = memory.get_messages()
    # Should still have system prompt
    assert len(messages_after_clear) == 1 and messages_after_clear[0]["role"] == "system"
    print("✓ clear() works correctly, system prompt preserved")

    # Close
    memory.db_manager.close()

    # Clean up
    if os.path.exists(test_db):
        os.remove(test_db)
    for ext in ['-wal', '-shm']:
        wal_file = test_db + ext
        if os.path.exists(wal_file):
            os.remove(wal_file)

    print("\nConversationMemory tests passed! ✓\n")


def test_memory_persistence():
    """Test that messages persist across ConversationMemory instances."""
    print("=" * 60)
    print("Testing Message Persistence")
    print("=" * 60)

    test_db = "test_persistence.db"

    # Clean up any existing test database
    if os.path.exists(test_db):
        os.remove(test_db)

    # Create first memory instance and add messages
    memory1 = ConversationMemory(
        system_prompt="Test system prompt",
        db_path=test_db,
        auto_load=True
    )
    memory1.add_user_message("First message")
    memory1.add_assistant_message("First response")
    memory1.db_manager.close()
    print("✓ Created first memory instance with 2 messages")

    # Create second memory instance - should load previous messages
    memory2 = ConversationMemory(
        system_prompt="Test system prompt",
        db_path=test_db,
        auto_load=True
    )
    messages = memory2.get_messages()
    # Should have system + 2 messages from before
    assert len(messages) == 3, f"Expected 3 messages, got {len(messages)}"
    assert messages[1]["content"] == "First message"
    assert messages[2]["content"] == "First response"
    print(f"✓ Second instance loaded {len(messages) - 1} persisted messages")

    # Add more messages to second instance
    memory2.add_user_message("Second message")
    memory2.add_assistant_message("Second response")
    memory2.db_manager.close()

    # Create third memory instance - should have all messages
    memory3 = ConversationMemory(
        system_prompt="Test system prompt",
        db_path=test_db,
        auto_load=True
    )
    messages3 = memory3.get_messages()
    assert len(messages3) == 5, f"Expected 5 messages, got {len(messages3)}"
    print(f"✓ Third instance loaded all {len(messages3) - 1} messages")

    # Clean up
    memory3.db_manager.close()
    if os.path.exists(test_db):
        os.remove(test_db)
    for ext in ['-wal', '-shm']:
        wal_file = test_db + ext
        if os.path.exists(wal_file):
            os.remove(wal_file)

    print("\nPersistence tests passed! ✓\n")


def test_memory_manager():
    """Test the MemoryManager class."""
    print("=" * 60)
    print("Testing MemoryManager")
    print("=" * 60)

    test_db = "test_memory_manager.db"

    # Clean up
    if os.path.exists(test_db):
        os.remove(test_db)

    # Create MemoryManager (without system prompt to simplify testing)
    manager = MemoryManager(
        db_path=test_db,
        system_prompt=None
    )
    print("✓ MemoryManager initialized")

    # Test save_message
    manager.save_message("user", "Hello")
    manager.save_message("assistant", "Hi!")
    print("✓ Saved 2 messages via MemoryManager")

    # Test load_history
    history = manager.load_history()
    assert len(history) == 2
    print(f"✓ Loaded {len(history)} messages via MemoryManager")

    # Test clear_memory
    manager.clear_memory()
    history_after = manager.load_history()
    assert len(history_after) == 0, f"Expected 0 after clear, got {len(history_after)}"
    print("✓ clear_memory() works correctly")

    # Test get_messages
    messages = manager.get_messages()
    assert len(messages) == 0, f"Expected 0 messages in memory, got {len(messages)}"
    print("✓ get_messages() returns empty after clear")

    # Clean up
    manager.memory.db_manager.close()
    if os.path.exists(test_db):
        os.remove(test_db)
    for ext in ['-wal', '-shm']:
        wal_file = test_db + ext
        if os.path.exists(wal_file):
            os.remove(wal_file)

    print("\nMemoryManager tests passed! ✓\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  SQLite Database Integration Tests")
    print("=" * 60 + "\n")

    try:
        test_database_manager()
        test_conversation_memory()
        test_memory_persistence()
        test_memory_manager()

        print("=" * 60)
        print("  ALL TESTS PASSED! ✓")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())