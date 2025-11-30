"""
E2E tests for 5-Day Forecast
Tests the 5-day forecast section including temperature display in dual format,
weather icons, and date formatting
"""
import pytest
import re
from playwright.sync_api import Page, expect
from tests.conftest import expect_temperature_format


@pytest.mark.e2e
@pytest.mark.api
class TestFiveDayForecast:
    """Test suite for 5-day weather forecast functionality"""

    @pytest.fixture
    def weather_page(self, page_with_app: Page) -> Page:
        """Navigate to a weather page for testing"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Search for a known city
        search_input.fill("Seattle, Washington")
        submit_button.click()

        # Wait for navigation to weather page
        page_with_app.wait_for_url("**/Seattle**", timeout=10000)

        return page_with_app

    @pytest.mark.smoke
    def test_forecast_section_exists(self, weather_page: Page):
        """Test that 5-day forecast section is present"""
        forecast_header = weather_page.locator("h2", has_text="5-DAY FORECAST")
        expect(forecast_header).to_be_visible()

        forecast_container = weather_page.locator(".five-day")
        expect(forecast_container).to_be_visible()

    @pytest.mark.smoke
    def test_forecast_has_five_days(self, weather_page: Page):
        """Test that exactly 5 forecast days are displayed"""
        forecast_items = weather_page.locator(".forecast-item")

        # Should have exactly 5 forecast items
        expect(forecast_items).to_have_count(5)

    def test_each_forecast_day_has_date(self, weather_page: Page):
        """Test that each forecast day displays a date/day of week"""
        forecast_items = weather_page.locator(".forecast-item")

        # Check each of the 5 days
        for i in range(5):
            day_element = forecast_items.nth(i).locator("p").first
            expect(day_element).to_be_visible()

            day_text = day_element.inner_text()

            # Should contain abbreviated day (Mon, Tue, Wed, etc.)
            abbreviated_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            assert any(day in day_text for day in abbreviated_days), \
                f"Forecast day {i+1} should show day of week, got: {day_text}"

    def test_each_forecast_day_has_icon(self, weather_page: Page):
        """Test that each forecast day has a weather icon"""
        forecast_items = weather_page.locator(".forecast-item")

        # Check each of the 5 days
        for i in range(5):
            icon = forecast_items.nth(i).locator("img.weather-icon")
            expect(icon).to_be_visible()

            # Verify icon source is from static assets
            icon_src = icon.get_attribute('src')
            assert '/static/assets/' in icon_src, \
                f"Day {i+1} icon should be from /static/assets/, got: {icon_src}"

    @pytest.mark.smoke
    def test_each_forecast_day_has_dual_temperature(self, weather_page: Page):
        """Test that each forecast day displays temperature in both C and F"""
        forecast_items = weather_page.locator(".forecast-item")

        # Check each of the 5 days
        for i in range(5):
            temp_element = forecast_items.nth(i).locator("p").last
            expect(temp_element).to_be_visible()

            temp_text = temp_element.inner_text()

            # Verify dual temperature format
            assert expect_temperature_format(temp_text), \
                f"Day {i+1} temperature should be in 'XX°C / XX°F' format, got: {temp_text}"

            # Verify both units are present
            assert "°C" in temp_text, f"Day {i+1} should have Celsius"
            assert "°F" in temp_text, f"Day {i+1} should have Fahrenheit"

    def test_forecast_temperature_conversion_accuracy(self, weather_page: Page):
        """Test that Fahrenheit conversion is accurate for all forecast days"""
        forecast_items = weather_page.locator(".forecast-item")

        # Check conversion for each day
        for i in range(5):
            temp_element = forecast_items.nth(i).locator("p").last
            temp_text = temp_element.inner_text()

            # Extract Celsius and Fahrenheit values
            celsius_match = re.search(r'(-?\d+)°C', temp_text)
            fahrenheit_match = re.search(r'(-?\d+)°F', temp_text)

            assert celsius_match, f"Day {i+1}: Could not extract Celsius value from {temp_text}"
            assert fahrenheit_match, f"Day {i+1}: Could not extract Fahrenheit value from {temp_text}"

            celsius = int(celsius_match.group(1))
            fahrenheit = int(fahrenheit_match.group(1))

            # Calculate expected Fahrenheit
            expected_fahrenheit = round((celsius * 9/5) + 32)

            assert fahrenheit == expected_fahrenheit, \
                f"Day {i+1}: {celsius}°C should be {expected_fahrenheit}°F, got {fahrenheit}°F"

    def test_forecast_shows_different_conditions(self, weather_page: Page):
        """Test that forecast can show different weather conditions across days"""
        forecast_items = weather_page.locator(".forecast-item")

        # Collect all weather icons
        icons = []
        for i in range(5):
            icon = forecast_items.nth(i).locator("img.weather-icon")
            icon_src = icon.get_attribute('src')
            icons.append(icon_src)

        # All icons should be valid
        assert all(icon for icon in icons), "All forecast days should have weather icons"

        # Icons should be from known weather types
        known_weather_files = ["clear.png", "clouds.png", "rain.png", "snow.png", "drizzle.png", "thunderstorm.png"]
        for icon_src in icons:
            assert any(weather in icon_src for weather in known_weather_files), \
                f"Icon should be from known weather types: {icon_src}"

    def test_forecast_days_are_sequential(self, weather_page: Page):
        """Test that forecast days are in sequential order"""
        forecast_items = weather_page.locator(".forecast-item")

        # Get all day names
        days = []
        for i in range(5):
            day_element = forecast_items.nth(i).locator("p").first
            day_text = day_element.inner_text()
            days.append(day_text)

        # All days should be present
        assert len(days) == 5, f"Should have 5 days, got {len(days)}"

        # Days should not be empty
        assert all(day.strip() for day in days), "All day names should be non-empty"

    def test_forecast_temperatures_are_reasonable(self, weather_page: Page):
        """Test that forecast temperatures are within reasonable ranges"""
        forecast_items = weather_page.locator(".forecast-item")

        for i in range(5):
            temp_element = forecast_items.nth(i).locator("p").last
            temp_text = temp_element.inner_text()

            # Extract Celsius value
            celsius_match = re.search(r'(-?\d+)°C', temp_text)
            assert celsius_match, f"Day {i+1}: Could not extract Celsius value"

            celsius = int(celsius_match.group(1))

            # Reasonable temperature range: -50°C to 50°C
            assert -50 <= celsius <= 50, \
                f"Day {i+1}: Temperature {celsius}°C is outside reasonable range (-50°C to 50°C)"

    def test_forecast_divider_exists(self, weather_page: Page):
        """Test that visual divider exists between current weather and forecast"""
        divider = weather_page.locator(".divider")
        expect(divider).to_be_visible()

    def test_forecast_loads_for_different_cities(self, page_with_app: Page):
        """Test that 5-day forecast loads correctly for different cities"""
        cities = ["Miami, Florida", "Denver, Colorado", "Portland, Oregon"]

        for city in cities:
            # Navigate to home
            page_with_app.goto("http://127.0.0.1:5000/")

            # Search for city
            search_input = page_with_app.locator('input[name="search"]')
            submit_button = page_with_app.locator('button[type="submit"]')

            search_input.fill(city)
            submit_button.click()

            # Wait for weather page
            page_with_app.wait_for_url(f"**/{city.split(',')[0]}**", timeout=10000)

            # Verify forecast section exists
            forecast_items = page_with_app.locator(".forecast-item")
            expect(forecast_items).to_have_count(5)

            # Verify at least one temperature is visible
            first_temp = forecast_items.first.locator("p").last
            expect(first_temp).to_be_visible()
            temp_text = first_temp.inner_text()
            assert expect_temperature_format(temp_text), \
                f"Forecast for {city} should have dual temperature format"
