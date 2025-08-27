#!/bin/bash
# Script to run Python scripts with virtual environment automatically activated

if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh <script_name> [arguments...]"
    echo ""
    echo "Examples:"
    echo "  ./run.sh example.py"
    echo "  ./run.sh scrape_cli.py https://example.com"
    echo "  ./run.sh enhanced_scraper.py"
    echo ""
    echo "Available scripts:"
    echo "  - example.py (run examples)"
    echo "  - enhanced_scraper.py (run enhanced scraper)"
    echo "  - web_scraper.py (run basic scraper)"
    echo "  - scrape_cli.py (command line interface)"
    echo "  - test_setup.py (test setup)"
    exit 1
fi

SCRIPT_NAME=$1
shift  # Remove first argument, keep the rest

# Check if script exists
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "Error: Script '$SCRIPT_NAME' not found!"
    echo "Available scripts:"
    ls -1 *.py
    exit 1
fi

# Activate virtual environment and run script
echo "🚀 Activating virtual environment and running $SCRIPT_NAME..."
echo "Arguments: $@"
echo ""

source venv/bin/activate

# Run the script with remaining arguments
python "$SCRIPT_NAME" "$@"

# Deactivate virtual environment
deactivate

echo ""
echo "✅ Script completed!"
