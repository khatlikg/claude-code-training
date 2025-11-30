# Weather App E2E Test Suite

Comprehensive end-to-end test suite for the Weather App using Playwright and pytest.

## Overview

This test suite provides complete E2E coverage for the Weather App, including:
- Home page functionality
- Weather data display with dual temperature format (Celsius/Fahrenheit)
- 5-day weather forecast
- Error handling and edge cases
- Cross-browser compatibility
- Responsive design testing

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_home_page.py        # Home page and search functionality tests
├── test_weather_display.py  # Weather data display tests
├── test_forecast.py         # 5-day forecast tests
├── test_error_handling.py   # Error handling and edge case tests
└── test-results/            # Test artifacts (screenshots, videos, traces)
```

## Prerequisites

### Install Dependencies

```bash
# Install test dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Environment Setup

Ensure you have a valid OpenWeatherMap API key in `.env`:

```
OWM_API_KEY=your_api_key_here
```

## Running Tests

### Run All Tests

```bash
# Run complete test suite
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with detailed output and show print statements
pytest tests/ -vv -s
```

### Run Specific Test Files

```bash
# Run only home page tests
pytest tests/test_home_page.py

# Run only weather display tests
pytest tests/test_weather_display.py

# Run only forecast tests
pytest tests/test_forecast.py

# Run only error handling tests
pytest tests/test_error_handling.py
```

### Run Tests by Marker

```bash
# Run smoke tests only (critical functionality)
pytest tests/ -m smoke

# Run regression tests
pytest tests/ -m regression

# Run E2E tests
pytest tests/ -m e2e

# Run tests that interact with external APIs
pytest tests/ -m api
```

### Run in Headless Mode

```bash
# Run without opening browser window
pytest tests/ --headed=false

# Or modify pytest.ini to remove --headed flag
```

### Run with Different Browsers

```bash
# Run with Firefox
pytest tests/ --browser firefox

# Run with WebKit (Safari engine)
pytest tests/ --browser webkit

# Run with multiple browsers
pytest tests/ --browser chromium --browser firefox
```

## Test Configuration

Configuration is managed in `pytest.ini`:

- **Test discovery**: Automatically finds `test_*.py` files
- **Browser**: Chromium (default), can be changed to Firefox or WebKit
- **Headed mode**: Tests run with visible browser (good for debugging)
- **Slow motion**: 100ms delay between actions for better visibility
- **Screenshots**: Captured on test failure
- **Videos**: Recorded on test failure
- **Output directory**: `tests/test-results/`

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.smoke`: Quick smoke tests for critical functionality
- `@pytest.mark.regression`: Full regression test suite
- `@pytest.mark.e2e`: End-to-end integration tests
- `@pytest.mark.api`: Tests that interact with external APIs

## Test Coverage

### Home Page Tests (`test_home_page.py`)
✅ Page loads successfully
✅ Search form is present and functional
✅ Search input validation
✅ Navigation to weather page
✅ Responsive design (mobile, tablet, desktop)

### Weather Display Tests (`test_weather_display.py`)
✅ City name displays correctly
✅ Current date shows day of week
✅ Temperature displays in dual format (XX°C / XX°F)
✅ Temperature conversion accuracy
✅ Min/Max temperature range with both units
✅ Weather condition and icon display
✅ Wind speed display
✅ "Change City" button functionality
✅ Multiple city searches

### 5-Day Forecast Tests (`test_forecast.py`)
✅ Forecast section displays
✅ Exactly 5 days shown
✅ Each day shows date/day of week
✅ Each day has weather icon
✅ Each day shows dual temperature format
✅ Temperature conversion accuracy for all days
✅ Different weather conditions across days
✅ Sequential day ordering
✅ Reasonable temperature ranges
✅ Forecast loads for multiple cities

### Error Handling Tests (`test_error_handling.py`)
✅ Invalid city name handling
✅ Special character input sanitization
✅ Very long input handling
✅ Error page functionality
✅ Unicode/international city names
✅ Whitespace-only input
✅ Case-insensitive search
✅ City search without state
✅ Rapid sequential searches
✅ Browser back button
✅ Page refresh handling

## Debugging Failed Tests

### View Screenshots and Videos

When tests fail, screenshots and videos are automatically saved to `tests/test-results/`:

```
tests/test-results/
├── test-home-page-py-test-home-page-loads-chromium/
│   ├── test-failed-1.png
│   └── video.webm
└── ...
```

### Run Specific Failed Test

```bash
# Run a specific test function
pytest tests/test_weather_display.py::TestWeatherDisplay::test_current_temperature_dual_format -v

# Run with Playwright debug mode
PWDEBUG=1 pytest tests/test_weather_display.py::TestWeatherDisplay::test_current_temperature_dual_format
```

### Common Issues

**Issue**: Tests fail with "Flask app failed to start"
**Solution**: Ensure port 5000 is available and Flask app can start properly

**Issue**: API key errors during tests
**Solution**: Check `.env` file has valid `OWM_API_KEY`

**Issue**: Playwright browser not found
**Solution**: Run `playwright install chromium`

**Issue**: Tests timeout
**Solution**: Increase timeout in test or check network connection

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps chromium
      - name: Run tests
        env:
          OWM_API_KEY: ${{ secrets.OWM_API_KEY }}
        run: pytest tests/ --headed=false
```

## Best Practices

1. **Keep tests independent**: Each test should be able to run in isolation
2. **Use fixtures**: Shared setup logic is in `conftest.py`
3. **Clear test names**: Test names clearly describe what is being tested
4. **Appropriate waits**: Use Playwright's auto-waiting features
5. **Verify, don't assume**: Always use assertions to verify expected behavior
6. **Test real scenarios**: Tests simulate actual user workflows

## Contributing

When adding new tests:

1. Place tests in the appropriate file based on functionality
2. Use descriptive test names following the pattern `test_<what>_<expected_behavior>`
3. Add appropriate markers (`@pytest.mark.smoke`, `@pytest.mark.e2e`, etc.)
4. Include docstrings explaining what the test validates
5. Ensure tests are independent and can run in any order

## Performance

- **Smoke tests**: ~30-60 seconds (critical functionality only)
- **Full test suite**: ~5-10 minutes (all tests, single browser)
- **Multi-browser**: ~15-30 minutes (all tests, 3 browsers)

## Support

For issues with:
- **Playwright**: https://playwright.dev/python/docs/intro
- **pytest**: https://docs.pytest.org/
- **Weather App**: See main README.md
