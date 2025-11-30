"""
E2E tests for Error Handling
Tests how the application handles invalid inputs, network errors,
and edge cases
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
class TestErrorHandling:
    """Test suite for error handling and edge cases"""

    def test_invalid_city_name(self, page_with_app: Page):
        """Test handling of completely invalid city names"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Try an invalid/non-existent city
        invalid_cities = [
            "XYZ123InvalidCity",
            "NotARealPlace, NotARealState",
            "12345",
        ]

        for invalid_city in invalid_cities:
            # Navigate to home
            page_with_app.goto("http://127.0.0.1:5000/")

            search_input.fill(invalid_city)
            submit_button.click()

            # Should either show error page or redirect
            page_with_app.wait_for_timeout(2000)

            # Check if error page is shown or stayed on home
            current_url = page_with_app.url
            # Either shows error page or redirects back
            assert "/error" in current_url or current_url == "http://127.0.0.1:5000/", \
                f"Invalid city '{invalid_city}' should show error or redirect to home"

    def test_special_characters_in_search(self, page_with_app: Page):
        """Test handling of special characters in city search"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        special_inputs = [
            "<script>alert('test')</script>",
            "'; DROP TABLE cities; --",
            "City!@#$%^&*()",
        ]

        for special_input in special_inputs:
            page_with_app.goto("http://127.0.0.1:5000/")

            search_input.fill(special_input)
            submit_button.click()

            page_with_app.wait_for_timeout(2000)

            # Should handle gracefully without crashing
            # Either shows error or redirects to home
            current_url = page_with_app.url
            assert "/error" in current_url or current_url == "http://127.0.0.1:5000/", \
                f"Special characters should be handled safely"

    def test_very_long_city_name(self, page_with_app: Page):
        """Test handling of extremely long input"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Very long string
        long_input = "A" * 1000

        search_input.fill(long_input)
        submit_button.click()

        page_with_app.wait_for_timeout(2000)

        # Should handle without crashing
        current_url = page_with_app.url
        assert "/error" in current_url or current_url == "http://127.0.0.1:5000/", \
            "Very long input should be handled gracefully"

    def test_error_page_exists(self, page_with_app: Page):
        """Test that error page is accessible and properly formatted"""
        # Navigate directly to error page
        page_with_app.goto("http://127.0.0.1:5000/error")

        # Verify error page loads
        expect(page_with_app).to_have_title("Error")

        # Error page should have some content
        body = page_with_app.locator("body")
        expect(body).to_be_visible()

    def test_unicode_city_names(self, page_with_app: Page):
        """Test handling of unicode/international city names"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Cities with unicode characters
        unicode_cities = [
            "São Paulo, Brazil",
            "München, Germany",
            "東京, Japan",
        ]

        for city in unicode_cities:
            page_with_app.goto("http://127.0.0.1:5000/")

            search_input.fill(city)
            submit_button.click()

            page_with_app.wait_for_timeout(3000)

            # Should handle without crashing (may or may not find city)
            # Just verify page doesn't crash
            body = page_with_app.locator("body")
            expect(body).to_be_visible()

    def test_whitespace_only_input(self, page_with_app: Page):
        """Test handling of whitespace-only input"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Try various whitespace inputs
        whitespace_inputs = ["   ", "\t\t", "\n\n"]

        for ws_input in whitespace_inputs:
            page_with_app.goto("http://127.0.0.1:5000/")

            search_input.fill(ws_input)
            submit_button.click()

            page_with_app.wait_for_timeout(2000)

            # Should handle gracefully
            current_url = page_with_app.url
            assert "/error" in current_url or current_url == "http://127.0.0.1:5000/", \
                "Whitespace-only input should be handled"

    def test_case_insensitive_search(self, page_with_app: Page):
        """Test that city search works regardless of case"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Test different cases for same city
        case_variations = [
            "boston, massachusetts",
            "Boston, Massachusetts",
            "BOSTON, MASSACHUSETTS",
            "BoStOn, MaSsAcHuSeTtS",
        ]

        for city_variant in case_variations:
            page_with_app.goto("http://127.0.0.1:5000/")

            search_input.fill(city_variant)
            submit_button.click()

            # Wait for navigation
            page_with_app.wait_for_timeout(3000)

            # All should navigate to weather page (or at least not error)
            current_url = page_with_app.url
            # Should navigate away from home page
            assert current_url != "http://127.0.0.1:5000/" or "/error" in current_url, \
                f"City variant '{city_variant}' should be searchable"

    def test_city_without_state(self, page_with_app: Page):
        """Test searching for city without specifying state"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Cities without state specified
        cities_no_state = ["London", "Paris", "Tokyo"]

        for city in cities_no_state:
            page_with_app.goto("http://127.0.0.1:5000/")

            search_input.fill(city)
            submit_button.click()

            page_with_app.wait_for_timeout(3000)

            # Should handle without crashing
            body = page_with_app.locator("body")
            expect(body).to_be_visible()

    def test_rapid_sequential_searches(self, page_with_app: Page):
        """Test performing multiple rapid searches"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        cities = ["Austin, Texas", "Phoenix, Arizona", "Atlanta, Georgia"]

        # Perform rapid searches
        for city in cities:
            page_with_app.goto("http://127.0.0.1:5000/")

            search_input.fill(city)
            submit_button.click()

            # Minimal wait
            page_with_app.wait_for_timeout(500)

        # Application should still be functional
        page_with_app.goto("http://127.0.0.1:5000/")
        expect(page_with_app.locator('input[name="search"]')).to_be_visible()

    def test_navigation_back_button(self, page_with_app: Page):
        """Test browser back button functionality"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Search for a city
        search_input.fill("Houston, Texas")
        submit_button.click()

        # Wait for weather page
        page_with_app.wait_for_url("**/Houston**", timeout=10000)

        # Use browser back button
        page_with_app.go_back()

        # Should be back on home page
        page_with_app.wait_for_url("http://127.0.0.1:5000/", timeout=5000)
        expect(page_with_app).to_have_url("http://127.0.0.1:5000/")

        # Home page should still be functional
        expect(search_input).to_be_visible()

    def test_refresh_on_weather_page(self, page_with_app: Page):
        """Test page refresh on weather page"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Navigate to weather page
        search_input.fill("Philadelphia, Pennsylvania")
        submit_button.click()

        page_with_app.wait_for_url("**/Philadelphia**", timeout=10000)

        # Get initial temperature
        initial_temp = page_with_app.locator("#current-temp").inner_text()

        # Refresh page
        page_with_app.reload()

        # Page should reload successfully
        page_with_app.wait_for_timeout(2000)

        # Temperature should still be visible
        refreshed_temp = page_with_app.locator("#current-temp")
        expect(refreshed_temp).to_be_visible()
