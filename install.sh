#!/bin/bash
#
# Quick installation script for PDF Converter CLI
# This script will install the package using uv
#

set -e

echo "PDF Converter CLI - Installation Script"
echo "========================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed."
    echo ""
    echo "Install uv with one of these methods:"
    echo "  1. curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  2. brew install uv"
    echo ""
    exit 1
fi

echo "✓ uv is installed"
echo ""

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "⚠️  Warning: pandoc is not installed"
    echo "   PDF conversion will not work without it."
    echo "   Install with: brew install pandoc"
    echo ""
fi

# Check if xelatex is installed
if ! command -v xelatex &> /dev/null; then
    echo "⚠️  Warning: xelatex is not installed"
    echo "   PDF conversion will not work without it."
    echo "   Install with: brew install --cask mactex-no-gui"
    echo ""
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/convert_to_pdf.sh

# Create config if it doesn't exist
if [ ! -f config.json ]; then
    echo "Creating config.json from example..."
    cp config.json.example config.json
fi

# Install dependencies
echo "Installing dependencies with uv..."
uv pip install textual

echo ""
echo "✓ Installation complete!"
echo ""
echo "To run the application:"
echo ""
echo "  ./run.sh"
echo ""
echo "Or:"
echo ""
echo "  PYTHONPATH=src uv run python -m pdf_converter"
echo ""
echo "Or:"
echo ""
echo "  uv run main.py"
echo ""
