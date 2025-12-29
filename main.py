#!/usr/bin/env python3
"""
PDF Converter CLI - Main entry point
Run with: uv run main.py
"""

import os
import sys
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent

# Check if we're in a virtual environment, if not try to use .venv
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    venv_python = script_dir / ".venv" / "bin" / "python3"
    if venv_python.exists():
        # Re-execute with the venv Python
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)

# Add src to path so we can import pdf_converter
sys.path.insert(0, str(script_dir / "src"))

from pdf_converter.__main__ import main

if __name__ == "__main__":
    main()
