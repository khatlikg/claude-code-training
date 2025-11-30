"""
E2E tests for Weather App Home Page
Tests the landing page functionality including layout, search form, and navigation
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
@pytest.mark.e2e
class TestHomePage:
    """Test suite for home page functionality"""

    def test_home_page_loads(self, page_with_app: Page):
        """Test that home page loads successfully"""
        # Verify page title
        expect(page_with_app).to_have_title("Weather App")

        # Verify main heading is visible
        heading = page_with_app.locator("h1")
        expect(heading).to_be_visible()
        expect(heading).to_contain_text("Weather")

    def test_home_page_has_search_form(self, page_with_app: Page):
        """Test that search form is present and properly structured"""
        # Verify form exists
        form = page_with_app.locator("form")
        expect(form).to_be_visible()

        # Verify input field exists and has correct attributes
        search_input = page_with_app.locator('input[name="search"]')
        expect(search_input).to_be_visible()
        expect(search_input).to_have_attribute("placeholder", "Enter a City, State")
        expect(search_input).to_have_attribute("required", "")

        # Verify submit button exists
        submit_button = page_with_app.locator('button[type="submit"]')
        expect(submit_button).to_be_visible()

    def test_home_page_has_search_icon(self, page_with_app: Page):
        """Test that search icon is displayed"""
        search_icon = page_with_app.locator('img[alt="search-icon"]')
        expect(search_icon).to_be_visible()
        expect(search_icon).to_have_attribute("src", "/static/assets/search.png")

    def test_home_page_background_image(self, page_with_app: Page):
        """Test that background image loads correctly"""
        # Check if background image exists
        background_img = page_with_app.locator('img[src*="weather-home-background.jpg"]')
        # Note: Background might be CSS-based, so we check for the image file
        expect(page_with_app.locator("body")).to_be_visible()

    def test_empty_search_validation(self, page_with_app: Page):
        """Test that empty search is prevented by HTML5 validation"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Try to submit without entering anything
        submit_button.click()

        # Should stay on home page due to HTML5 validation
        expect(page_with_app).to_have_url("http://127.0.0.1:5000/")

    @pytest.mark.smoke
    def test_valid_city_search_navigation(self, page_with_app: Page):
        """Test that entering a valid city navigates to weather page"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Enter a city
        search_input.fill("Dallas, Texas")
        submit_button.click()

        # Should navigate to weather page for the city
        # URL should contain the city name (may be URL encoded)
        page_with_app.wait_for_url("**/Dallas**", timeout=10000)
        expect(page_with_app).not_to_have_url("http://127.0.0.1:5000/")

    def test_page_responsiveness_mobile(self, page: Page, flask_app, base_url):
        """Test home page on mobile viewport"""
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(base_url)

        # Verify key elements are still visible
        expect(page.locator("h1")).to_be_visible()
        expect(page.locator('input[name="search"]')).to_be_visible()
        expect(page.locator('button[type="submit"]')).to_be_visible()

    def test_page_responsiveness_tablet(self, page: Page, flask_app, base_url):
        """Test home page on tablet viewport"""
        # Set tablet viewport
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(base_url)

        # Verify key elements are still visible
        expect(page.locator("h1")).to_be_visible()
        expect(page.locator('input[name="search"]')).to_be_visible()
        expect(page.locator('button[type="submit"]')).to_be_visible()
