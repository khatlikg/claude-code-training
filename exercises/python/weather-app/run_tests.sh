#!/bin/bash

# Weather App E2E Test Runner
# Convenient script for running Playwright tests with various configurations

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Print banner
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Weather App E2E Test Suite Runner    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo

# Function to check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"

    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        echo -e "${RED}❌ pytest not found. Installing dependencies...${NC}"
        pip install -r requirements.txt
    fi

    # Check if .env file exists
    if [ ! -f .env ]; then
        echo -e "${RED}❌ .env file not found!${NC}"
        echo -e "${YELLOW}Please create a .env file with OWM_API_KEY${NC}"
        exit 1
    fi

    echo -e "${GREEN}✓ Prerequisites OK${NC}"
    echo
}

# Function to display usage
usage() {
    echo "Usage: $0 [option]"
    echo
    echo "Options:"
    echo "  all          Run all tests"
    echo "  smoke        Run smoke tests only (quick)"
    echo "  home         Run home page tests"
    echo "  weather      Run weather display tests"
    echo "  forecast     Run forecast tests"
    echo "  errors       Run error handling tests"
    echo "  headless     Run all tests in headless mode"
    echo "  debug        Run tests with debugging enabled"
    echo "  install      Install test dependencies and browsers"
    echo "  clean        Clean test results directory"
    echo "  help         Show this help message"
    echo
}

# Function to install dependencies
install_deps() {
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    pip install -r requirements.txt

    echo -e "${YELLOW}Installing Playwright browsers...${NC}"
    playwright install chromium

    echo -e "${GREEN}✓ Installation complete${NC}"
}

# Function to clean test results
clean_results() {
    echo -e "${YELLOW}Cleaning test results...${NC}"
    rm -rf tests/test-results/*
    echo -e "${GREEN}✓ Test results cleaned${NC}"
}

# Main script logic
check_prerequisites

case "${1:-all}" in
    all)
        echo -e "${BLUE}Running all tests...${NC}"
        pytest tests/ -v
        ;;

    smoke)
        echo -e "${BLUE}Running smoke tests...${NC}"
        pytest tests/ -m smoke -v
        ;;

    home)
        echo -e "${BLUE}Running home page tests...${NC}"
        pytest tests/test_home_page.py -v
        ;;

    weather)
        echo -e "${BLUE}Running weather display tests...${NC}"
        pytest tests/test_weather_display.py -v
        ;;

    forecast)
        echo -e "${BLUE}Running forecast tests...${NC}"
        pytest tests/test_forecast.py -v
        ;;

    errors)
        echo -e "${BLUE}Running error handling tests...${NC}"
        pytest tests/test_error_handling.py -v
        ;;

    headless)
        echo -e "${BLUE}Running all tests in headless mode...${NC}"
        pytest tests/ --headed=false -v
        ;;

    debug)
        echo -e "${BLUE}Running tests with debugging...${NC}"
        pytest tests/ -vv -s --slowmo 500
        ;;

    install)
        install_deps
        ;;

    clean)
        clean_results
        ;;

    help)
        usage
        ;;

    *)
        echo -e "${RED}Unknown option: $1${NC}"
        echo
        usage
        exit 1
        ;;
esac

# Print test result summary
EXIT_CODE=$?
echo
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║      ✓ All Tests Passed!               ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
else
    echo -e "${RED}╔════════════════════════════════════════╗${NC}"
    echo -e "${RED}║      ✗ Some Tests Failed               ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════╝${NC}"
    echo -e "${YELLOW}Check test-results/ for screenshots and videos${NC}"
fi

exit $EXIT_CODE
