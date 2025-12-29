#!/bin/bash
#
# Quick run script for PDF Converter CLI
#

cd "$(dirname "$0")"

# Run with uv
PYTHONPATH=src uv run python -m pdf_converter "$@"
