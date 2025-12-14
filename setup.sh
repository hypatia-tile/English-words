#!/bin/bash
# Setup script for vocabulary learning system

echo "Setting up vocabulary learning system..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To use the vocabulary system:"
echo "  1. source venv/bin/activate"
echo "  2. python add_entry.py word \"myword\" --example \"example sentence\""
echo "  3. python status.py (to see all entries)"
echo "  4. python review.py (to see entries due for review)"
echo ""
