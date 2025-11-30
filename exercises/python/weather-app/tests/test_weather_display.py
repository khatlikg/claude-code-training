"""
E2E tests for Weather Display Page
Tests weather data display including dual temperature format (Celsius/Fahrenheit),
current conditions, and page navigation
"""
import pytest
import re
from playwright.sync_api import Page, expect
from tests.conftest import expect_temperature_format


@pytest.mark.e2e
@pytest.mark.api
class TestWeatherDisplay:
    """Test suite for weather data display functionality"""

    @pytest.fixture
    def weather_page(self, page_with_app: Page) -> Page:
        """Navigate to a weather page for testing"""
        search_input = page_with_app.locator('input[name="search"]')
        submit_button = page_with_app.locator('button[type="submit"]')

        # Search for a known city
        search_input.fill("Dallas, Texas")
        submit_button.click()

        # Wait for navigation to weather page
        page_with_app.wait_for_url("**/Dallas**", timeout=10000)

        return page_with_app

    @pytest.mark.smoke
    def test_city_name_displays(self, weather_page: Page):
        """Test that city name is displayed correctly"""
        city_heading = weather_page.locator(".city-header h1")
        expect(city_heading).to_be_visible()
        expect(city_heading).to_contain_text("Dallas")

    @pytest.mark.smoke
    def test_current_date_displays(self, weather_page: Page):
        """Test that current date is displayed"""
        date_heading = weather_page.locator(".city-header h2")
        expect(date_heading).to_be_visible()

        # Verify date contains day of week (e.g., "Monday", "Tuesday")
        date_text = date_heading.inner_text()
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        assert any(day in date_text for day in days_of_week), f"Date should contain day of week, got: {date_text}"

    @pytest.mark.smoke
    def test_current_temperature_dual_format(self, weather_page: Page):
        """Test that current temperature displays in both Celsius and Fahrenheit"""
        current_temp = weather_page.locator("#current-temp")
        expect(current_temp).to_be_visible()

        # Get temperature text
        temp_text = current_temp.inner_text()

        # Verify format is "XX°C / XX°F"
        assert expect_temperature_format(temp_text), f"Temperature should be in 'XX°C / XX°F' format, got: {temp_text}"

        # Verify both C and F are present
        assert "°C" in temp_text, "Celsius symbol should be present"
        assert "°F" in temp_text, "Fahrenheit symbol should be present"

    def test_temperature_conversion_accuracy(self, weather_page: Page):
        """Test that Fahrenheit conversion from Celsius is accurate"""
        current_temp = weather_page.locator("#current-temp")
        temp_text = current_temp.inner_text()

        # Extract Celsius and Fahrenheit values
        celsius_match = re.search(r'(-?\d+)°C', temp_text)
        fahrenheit_match = re.search(r'(-?\d+)°F', temp_text)

        assert celsius_match, "Could not extract Celsius value"
        assert fahrenheit_match, "Could not extract Fahrenheit value"

        celsius = int(celsius_match.group(1))
        fahrenheit = int(fahrenheit_match.group(1))

        # Calculate expected Fahrenheit
        expected_fahrenheit = round((celsius * 9/5) + 32)

        assert fahrenheit == expected_fahrenheit, \
            f"Fahrenheit conversion incorrect: {celsius}°C should be {expected_fahrenheit}°F, got {fahrenheit}°F"

    @pytest.mark.smoke
    def test_min_max_temperature_displays(self, weather_page: Page):
        """Test that min/max temperature range displays with dual format"""
        # Find thermometer section
        thermometer_section = weather_page.locator('.daily-section:has(img[src*="thermometer.png"])')
        expect(thermometer_section).to_be_visible()

        # Get temperature range text
        temp_range_text = thermometer_section.locator('.forecast-text').inner_text()

        # Verify format contains both C and F for min and max
        assert "°C" in temp_range_text, "Celsius should be in min/max range"
        assert "°F" in temp_range_text, "Fahrenheit should be in min/max range"
        assert "-" in temp_range_text, "Range should have separator"

        # Verify pattern: XX°C / XX°F - XX°C / XX°F
        pattern = r'-?\d+°C / -?\d+°F - -?\d+°C / -?\d+°F'
        assert re.search(pattern, temp_range_text), \
            f"Min/Max should be in 'XX°C / XX°F - XX°C / XX°F' format, got: {temp_range_text}"

    def test_weather_condition_displays(self, weather_page: Page):
        """Test that weather condition (Clear, Clouds, Rain, etc.) is displayed"""
        weather_condition_section = weather_page.locator('.daily-section').first
        weather_text = weather_condition_section.locator('.forecast-text')

        expect(weather_text).to_be_visible()

        # Verify it's one of the known weather conditions
        condition_text = weather_text.inner_text()
        known_conditions = ["Clear", "Clouds", "Rain", "Snow", "Drizzle", "Thunderstorm"]
        assert any(condition in condition_text for condition in known_conditions), \
            f"Weather condition should be one of {known_conditions}, got: {condition_text}"

    def test_weather_icon_displays(self, weather_page: Page):
        """Test that weather icon is displayed for current conditions"""
        weather_icon = weather_page.locator('.daily-section img.weather-icon').first
        expect(weather_icon).to_be_visible()

        # Verify icon has a valid source
        icon_src = weather_icon.get_attribute('src')
        assert icon_src and '/static/assets/' in icon_src, \
            f"Weather icon should have valid src from /static/assets/, got: {icon_src}"

    def test_wind_speed_displays(self, weather_page: Page):
        """Test that wind speed is displayed"""
        wind_section = weather_page.locator('.daily-section:has(img[src*="wind.png"])')
        expect(wind_section).to_be_visible()

        wind_text = wind_section.locator('.forecast-text')
        expect(wind_text).to_be_visible()

        # Verify wind speed has numeric value and unit
        wind_value = wind_text.inner_text()
        assert "meter/sec" in wind_value or "m/s" in wind_value, \
            f"Wind speed should have unit, got: {wind_value}"

    def test_change_city_button_exists(self, weather_page: Page):
        """Test that 'Change City' button is present"""
        change_button = weather_page.locator('.change-button a')
        expect(change_button).to_be_visible()
        expect(change_button).to_contain_text("CHANGE CITY")

    def test_change_city_button_navigation(self, weather_page: Page):
        """Test that 'Change City' button navigates back to home"""
        change_button = weather_page.locator('.change-button a')
        change_button.click()

        # Should navigate back to home page
        weather_page.wait_for_url("http://127.0.0.1:5000/", timeout=5000)
        expect(weather_page).to_have_url("http://127.0.0.1:5000/")

    def test_multiple_cities_sequential(self, page_with_app: Page):
        """Test searching multiple cities in sequence"""
        cities = ["New York, New York", "Los Angeles, California", "Chicago, Illinois"]

        for city in cities:
            # Navigate to home if not already there
            page_with_app.goto("http://127.0.0.1:5000/")

            # Search for city
            search_input = page_with_app.locator('input[name="search"]')
            submit_button = page_with_app.locator('button[type="submit"]')

            search_input.fill(city)
            submit_button.click()

            # Wait for weather page
            page_with_app.wait_for_url(f"**/{city.split(',')[0]}**", timeout=10000)

            # Verify temperature displays
            current_temp = page_with_app.locator("#current-temp")
            expect(current_temp).to_be_visible()

            temp_text = current_temp.inner_text()
            assert expect_temperature_format(temp_text), \
                f"Temperature for {city} should be in dual format, got: {temp_text}"
