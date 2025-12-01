#!/bin/bash

# Weather App Test Report Generator
# Generates comprehensive HTML test reports

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Generating Test Report...            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo

# Create test results directory if it doesn't exist
mkdir -p tests/test-results

# Run tests with HTML report generation
echo -e "${YELLOW}Running test suite...${NC}"

pytest tests/ \
    --html=tests/test-results/report.html \
    --self-contained-html \
    -v \
    --tb=short

EXIT_CODE=$?

echo
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${YELLOW}⚠ Some tests failed or had errors${NC}"
fi

echo
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${GREEN}📊 Test Report Generated!${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo
echo -e "${YELLOW}HTML Report:${NC}"
echo "  📄 tests/test-results/report.html"
echo
echo -e "${YELLOW}To view the report:${NC}"
echo "  open tests/test-results/report.html"
echo
echo -e "${YELLOW}Screenshots & Videos (on failure):${NC}"
echo "  📁 tests/test-results/"
echo

# Open report automatically (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}Opening report in browser...${NC}"
    open tests/test-results/report.html
fi

exit $EXIT_CODE
