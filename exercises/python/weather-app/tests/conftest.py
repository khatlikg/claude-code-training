"""
Pytest configuration and fixtures for Weather App E2E tests
"""
import pytest
import subprocess
import time
import os
import signal
from playwright.sync_api import Page, expect


# Flask app process fixture
@pytest.fixture(scope="session")
def flask_app():
    """Start Flask app before tests and stop after all tests complete"""
    # Get the project root directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Start Flask app in background
    process = subprocess.Popen(
        ["python", "-u", "main.py"],
        cwd=project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid  # Create new process group
    )

    # Wait for Flask to start (check if port 5000 is ready)
    max_retries = 30
    for i in range(max_retries):
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 5000))
            sock.close()
            if result == 0:
                print("Flask app started successfully")
                break
        except:
            pass
        time.sleep(0.5)
    else:
        process.kill()
        raise Exception("Flask app failed to start within 15 seconds")

    yield process

    # Cleanup: Stop Flask app
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait()


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the Flask app"""
    return "http://127.0.0.1:5000"


@pytest.fixture(scope="function")
def page_with_app(page: Page, flask_app, base_url):
    """
    Provide a page with the Flask app running and navigated to home page
    """
    page.goto(base_url)
    return page


# Custom assertions and helpers
def expect_temperature_format(text: str) -> bool:
    """
    Verify temperature is in format 'XX°C / XX°F'
    Returns True if format is correct
    """
    import re
    pattern = r'-?\d+°C / -?\d+°F'
    return bool(re.search(pattern, text))


def celsius_to_fahrenheit(celsius: int) -> int:
    """Convert Celsius to Fahrenheit (matches app logic)"""
    return round((celsius * 9/5) + 32)
