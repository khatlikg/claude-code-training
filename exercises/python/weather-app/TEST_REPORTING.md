# Weather App E2E Test Reporting Guide

Comprehensive guide to viewing and generating test reports for the Weather App E2E test suite.

## 📊 Available Reporting Formats

The test suite supports multiple reporting formats to suit different needs:

### 1. **HTML Reports** (Recommended for Humans)
Beautiful, interactive HTML reports with detailed test results, screenshots, and videos.

### 2. **Console Output** (Quick Feedback)
Real-time terminal output showing test progress and results.

### 3. **JUnit XML** (CI/CD Integration)
Machine-readable XML reports for continuous integration systems.

### 4. **Allure Reports** (Advanced Analytics)
Professional test reports with trend analysis, historical data, and detailed dashboards.

---

## 🌐 HTML Report (Primary Method)

### Quick Start - Generate HTML Report

```bash
# Option 1: Use the convenience script
./generate_test_report.sh

# Option 2: Run pytest directly
pytest tests/ --html=report.html --self-contained-html

# Option 3: Generate report for specific tests
pytest tests/test_home_page.py --html=home-page-report.html --self-contained-html
```

### What's in the HTML Report?

The HTML report includes:

✅ **Summary Dashboard**
- Total tests run
- Pass/fail/skip/error counts
- Total execution time
- Test environment info (Python version, OS, packages)

✅ **Detailed Test Results**
- Each test name and status (✓ Passed, ✗ Failed, ⊘ Skipped)
- Execution time per test
- Full error messages and stack traces for failures
- Test metadata and markers (@smoke, @e2e, etc.)

✅ **Visual Evidence** (on test failure)
- Screenshots of the browser state when test failed
- Video recordings of the test execution
- Console logs and network requests

✅ **Interactive Features**
- Collapsible sections for each test
- Filter tests by status (show only failures)
- Sort by execution time, name, or outcome
- Search functionality

### View the HTML Report

```bash
# macOS - Opens in default browser
open report.html

# Linux
xdg-open report.html

# Windows
start report.html

# Or just double-click report.html in file explorer
```

### Report Location

By default, HTML reports are saved in:
```
/exercises/python/weather-app/report.html
```

You can customize the location:
```bash
pytest tests/ --html=tests/test-results/my-custom-report.html --self-contained-html
```

---

## 📺 Console Output

### Default Console Report

When you run tests, pytest automatically shows progress in the terminal:

```bash
pytest tests/ -v
```

**Output includes:**
- Test collection summary
- Real-time test execution (. for pass, F for fail, E for error)
- Detailed failure/error messages
- Final summary with counts

### Enhanced Console Output

```bash
# Show more details
pytest tests/ -vv

# Show print statements and logging
pytest tests/ -vv -s

# Show short tracebacks
pytest tests/ --tb=short

# Show only failed tests in output
pytest tests/ --tb=line --no-header -q
```

### Colored Output

pytest automatically adds colors:
- 🟢 **Green**: Passed tests
- 🔴 **Red**: Failed tests
- 🟡 **Yellow**: Warnings and skipped tests

---

## 📸 Screenshots & Videos (Automatic on Failure)

### How It Works

Playwright automatically captures:
- **Screenshot**: Taken at the moment a test fails
- **Video**: Records the entire test execution (saved only on failure)
- **Trace**: Detailed timeline of all actions (optional)

### Location

Artifacts are saved to:
```
tests/test-results/
├── test-home-page-py-test-home-page-loads-chromium/
│   ├── test-failed-1.png          # Screenshot
│   └── video.webm                  # Video recording
└── test-weather-display-py-test-current-temperature-chromium/
    ├── test-failed-1.png
    └── video.webm
```

### View Screenshots & Videos

```bash
# Navigate to test results
cd tests/test-results

# List all test artifacts
ls -la

# View specific test folder
cd test-home-page-py-test-home-page-loads-chromium

# macOS - View screenshot
open test-failed-1.png

# macOS - Play video
open video.webm
```

### Configuration

Control screenshot/video capture in `pytest.ini`:

```ini
[pytest]
addopts =
    --screenshot only-on-failure    # or: on, off, only-on-failure
    --video retain-on-failure       # or: on, off, retain-on-failure
    --output tests/test-results     # output directory
```

---

## 📋 JUnit XML Reports (CI/CD)

### Generate JUnit XML

```bash
# Generate JUnit XML report
pytest tests/ --junit-xml=junit-report.xml

# Custom location
pytest tests/ --junit-xml=tests/test-results/junit.xml
```

### What's in JUnit XML?

```xml
<?xml version="1.0"?>
<testsuite tests="47" errors="2" failures="3" skipped="1">
  <testcase classname="tests.test_home_page" name="test_home_page_loads" time="0.543">
    <!-- Passed test -->
  </testcase>
  <testcase classname="tests.test_weather_display" name="test_temperature" time="1.234">
    <failure message="Temperature mismatch">
      <!-- Failure details -->
    </failure>
  </testcase>
</testsuite>
```

### Use with CI/CD

**GitHub Actions:**
```yaml
- name: Run tests
  run: pytest tests/ --junit-xml=test-results/junit.xml

- name: Publish test results
  uses: EnricoMi/publish-unit-test-result-action@v2
  with:
    files: test-results/junit.xml
```

**Jenkins:**
```groovy
post {
    always {
        junit 'test-results/junit.xml'
    }
}
```

---

## 🎯 Allure Reports (Advanced)

### Generate Allure Report

```bash
# Step 1: Run tests and collect Allure data
pytest tests/ --alluredir=allure-results

# Step 2: Generate and open Allure report
allure serve allure-results
```

### Install Allure (if not installed)

```bash
# macOS
brew install allure

# Linux
sudo apt-get install allure

# Windows (using Scoop)
scoop install allure
```

### What's in Allure Report?

✅ **Overview Dashboard**
- Pass/fail pie charts
- Trend graphs across test runs
- Test execution timeline
- Environment information

✅ **Test Suites**
- Organized by test files
- Hierarchical test structure
- Execution time breakdown

✅ **Graphs & Charts**
- Test duration trends
- Test execution history
- Severity distribution
- Feature coverage

✅ **Categories**
- Group failures by type
- Identify patterns in test failures
- Track flaky tests

✅ **Attachments**
- Screenshots embedded in report
- Videos accessible from test details
- Logs and traces

### Allure Report Features

```bash
# Generate static HTML report
allure generate allure-results --clean -o allure-report
open allure-report/index.html

# View historical trends
pytest tests/ --alluredir=allure-results --clean-alluredir=false

# Add custom categories
echo '[{"name": "API Failures", "matchedStatuses": ["failed"], "messageRegex": ".*API.*"}]' > categories.json
```

---

## 🚀 Quick Reference

### Generate All Reports at Once

```bash
pytest tests/ \
    --html=report.html \
    --self-contained-html \
    --junit-xml=junit.xml \
    --alluredir=allure-results \
    -v
```

### Common Scenarios

**Scenario 1: Quick smoke test with HTML report**
```bash
pytest tests/ -m smoke --html=smoke-report.html --self-contained-html
```

**Scenario 2: Full test suite with all reports**
```bash
./generate_test_report.sh
```

**Scenario 3: Run and immediately view report**
```bash
pytest tests/ --html=report.html --self-contained-html && open report.html
```

**Scenario 4: CI/CD pipeline report**
```bash
pytest tests/ --junit-xml=test-results/junit.xml --html=test-results/report.html --self-contained-html
```

**Scenario 5: Debug specific test with video**
```bash
pytest tests/test_weather_display.py::TestWeatherDisplay::test_current_temperature_dual_format \
    --video on \
    --screenshot on \
    -vv
```

---

## 📁 Report Files Summary

| Report Type | File Location | Best For |
|-------------|---------------|----------|
| HTML | `report.html` | Human review, detailed analysis |
| JUnit XML | `junit.xml` | CI/CD integration |
| Allure | `allure-report/` | Advanced analytics, trends |
| Screenshots | `tests/test-results/*/test-failed-*.png` | Visual debugging |
| Videos | `tests/test-results/*/video.webm` | Understanding failures |

---

## 🎨 Customizing Reports

### Custom HTML Report Title

```bash
pytest tests/ --html=report.html --self-contained-html --html-report-title="Weather App E2E Tests"
```

### Add Metadata to Reports

```python
# In conftest.py
def pytest_configure(config):
    config._metadata['Project'] = 'Weather App'
    config._metadata['Test Environment'] = 'Production'
    config._metadata['Tester'] = 'QA Team'
```

### Custom CSS for HTML Reports

Create `pytest_html_style.css`:
```css
body {
    font-family: 'Arial', sans-serif;
}
.passed { background-color: #d4edda !important; }
.failed { background-color: #f8d7da !important; }
```

---

## 🐛 Troubleshooting Reports

### Issue: HTML report not generated
**Solution:**
```bash
# Ensure pytest-html is installed
pip install pytest-html

# Check directory permissions
mkdir -p tests/test-results
chmod 755 tests/test-results
```

### Issue: Screenshots/videos not captured
**Solution:**
```bash
# Verify Playwright is installed
playwright install chromium

# Check pytest.ini configuration
cat pytest.ini | grep screenshot
```

### Issue: Allure report shows no tests
**Solution:**
```bash
# Clean allure results
rm -rf allure-results/*

# Run tests again
pytest tests/ --alluredir=allure-results
```

---

## 📚 Additional Resources

- **pytest-html docs**: https://pytest-html.readthedocs.io/
- **Allure docs**: https://docs.qameta.io/allure/
- **Playwright reporting**: https://playwright.dev/python/docs/test-reporters
- **JUnit XML format**: https://llg.cubic.org/docs/junit/

---

## 💡 Pro Tips

1. **Keep historical reports**: Save reports with timestamps
   ```bash
   pytest tests/ --html=reports/test-$(date +%Y%m%d-%H%M%S).html --self-contained-html
   ```

2. **Compare reports**: Use Allure to track trends across test runs

3. **Share reports**: HTML reports are self-contained - just send the `.html` file

4. **Automate reporting**: Add report generation to your CI/CD pipeline

5. **Review videos carefully**: They often reveal timing issues or unexpected UI behavior

Happy Testing! 🎉
