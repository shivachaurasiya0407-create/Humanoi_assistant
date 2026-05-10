"""
Test suite for BrowserController.
Tests all core functionality including navigation, element interaction, and tab management.
"""

import pytest
import time
from web.browser_controller import (
    BrowserController,
    BrowserConfig,
    BrowserControllerError,
    BrowserNotLaunchedError,
    ElementNotFoundError,
    TimeoutExceededError,
)


@pytest.fixture
def controller():
    """Create a browser controller instance for testing."""
    config = BrowserConfig(
        headless=True,  # Use headless for tests
        timeout=15000,
        viewport_width=1024,
        viewport_height=768,
    )
    ctrl = BrowserController(config)
    yield ctrl
    # Cleanup after test
    if ctrl.is_browser_running():
        ctrl.close_browser()


class TestBrowserLifecycle:
    """Test browser launch and close functionality."""
    
    def test_launch_browser(self, controller):
        """Test that browser launches successfully."""
        assert not controller.is_browser_running()
        result = controller.launch_browser()
        assert result is True
        assert controller.is_browser_running()
    
    def test_close_browser(self, controller):
        """Test that browser closes successfully."""
        controller.launch_browser()
        assert controller.is_browser_running()
        result = controller.close_browser()
        assert result is True
        assert not controller.is_browser_running()
    
    def test_double_launch_warning(self, controller, caplog):
        """Test that launching twice doesn't cause issues."""
        controller.launch_browser()
        result = controller.launch_browser()  # Should return True with warning
        assert result is True
    
    def test_operation_without_launch_raises_error(self, controller):
        """Test that operations fail gracefully when browser not launched."""
        with pytest.raises(BrowserNotLaunchedError):
            controller.open_url("https://example.com")


class TestNavigation:
    """Test browser navigation functionality."""
    
    def test_open_url(self, controller):
        """Test navigating to a URL."""
        controller.launch_browser()
        result = controller.open_url("https://www.example.com")
        assert result is True
        assert "example.com" in controller.get_current_url()
    
    def test_get_page_title(self, controller):
        """Test getting page title."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        title = controller.get_page_title()
        assert "Example" in title
    
    def test_go_back_forward(self, controller):
        """Test browser history navigation."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        first_url = controller.get_current_url()
        
        controller.open_url("https://www.google.com")
        second_url = controller.get_current_url()
        assert "google.com" in second_url
        
        controller.go_back()
        back_url = controller.get_current_url()
        assert "example.com" in back_url
        
        controller.go_forward()
        forward_url = controller.get_current_url()
        assert "google.com" in forward_url
    
    def test_reload_page(self, controller):
        """Test page reload."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        result = controller.reload_page()
        assert result is True


class TestSearch:
    """Test search functionality."""
    
    def test_google_search(self, controller):
        """Test performing a Google search."""
        controller.launch_browser()
        result = controller.search_google("test query 12345")
        assert result is True
        assert "google" in controller.get_current_url().lower()


class TestElementInteraction:
    """Test element interaction functionality."""
    
    def test_click_element(self, controller):
        """Test clicking an element."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        
        # Example.com has a link we can click
        result = controller.click_element("a")
        assert result is True
    
    def test_type_text(self, controller):
        """Test typing text into an element."""
        controller.launch_browser()
        controller.open_url("https://www.google.com")
        
        # Type in Google search box
        result = controller.type_text("textarea[name='q']", "hello world")
        assert result is True
    
    def test_scroll_page(self, controller):
        """Test scrolling the page."""
        controller.launch_browser()
        controller.open_url("https://en.wikipedia.org/wiki/Test")
        
        result = controller.scroll_page("down", 500)
        assert result is True
        
        result = controller.scroll_page("top")
        assert result is True
    
    def test_get_element_text(self, controller):
        """Test getting element text."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        
        text = controller.get_element_text("h1")
        assert "Example" in text


class TestWaitStrategies:
    """Test wait functionality."""
    
    def test_wait_for_element(self, controller):
        """Test waiting for an element."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        
        element = controller.wait_for_element("h1", timeout=5000)
        assert element is not None
    
    def test_wait_for_element_timeout(self, controller):
        """Test wait timeout raises error."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        
        with pytest.raises(TimeoutExceededError):
            controller.wait_for_element("#nonexistent-element-xyz", timeout=2000)
    
    def test_wait_for_timeout(self, controller):
        """Test waiting for a duration."""
        controller.launch_browser()
        
        start = time.time()
        controller.wait_for_timeout(1000)  # Wait 1 second
        elapsed = time.time() - start
        
        assert elapsed >= 0.9  # Allow some tolerance


class TestTabManagement:
    """Test tab management functionality."""
    
    def test_open_new_tab(self, controller):
        """Test opening a new tab."""
        controller.launch_browser()
        assert controller.get_tab_count() == 1
        
        index = controller.open_new_tab("https://www.google.com")
        assert index == 1
        assert controller.get_tab_count() == 2
        assert "google.com" in controller.get_current_url()
    
    def test_switch_tab(self, controller):
        """Test switching between tabs."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        
        controller.open_new_tab("https://www.google.com")
        assert "google.com" in controller.get_current_url()
        
        controller.switch_tab(0)
        assert "example.com" in controller.get_current_url()
    
    def test_close_tab(self, controller):
        """Test closing a tab."""
        controller.launch_browser()
        controller.open_new_tab("https://www.google.com")
        assert controller.get_tab_count() == 2
        
        controller.close_tab(1)
        assert controller.get_tab_count() == 1
    
    def test_cannot_close_last_tab(self, controller):
        """Test that the last tab cannot be closed."""
        controller.launch_browser()
        result = controller.close_tab()
        assert result is False


class TestScreenshots:
    """Test screenshot functionality."""
    
    def test_take_screenshot(self, controller):
        """Test taking a screenshot."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        
        screenshot = controller.take_screenshot()
        assert isinstance(screenshot, bytes)
        assert len(screenshot) > 0


class TestJavaScript:
    """Test JavaScript execution functionality."""
    
    def test_execute_script(self, controller):
        """Test executing JavaScript."""
        controller.launch_browser()
        controller.open_url("https://www.example.com")
        
        result = controller.execute_script("return document.title")
        assert "Example" in result
        
        result = controller.execute_script("return 2 + 2")
        assert result == 4


class TestContextManager:
    """Test context manager functionality."""
    
    def test_context_manager(self):
        """Test using browser controller as context manager."""
        with BrowserController(BrowserConfig(headless=True)) as controller:
            assert controller.is_browser_running()
            controller.open_url("https://www.example.com")
            assert "example.com" in controller.get_current_url()
        
        # Browser should be closed after context exit
        assert not controller.is_browser_running()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])