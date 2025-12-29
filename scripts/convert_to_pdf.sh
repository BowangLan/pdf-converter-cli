#!/bin/bash

# PDF Conversion Script
# Usage: ./convert_to_pdf.sh <input_text_file> <output_pdf_file> [style_tex_path]

INPUT_FILE="$1"
OUTPUT_FILE="$2"
STYLE_TEX="$3"

# Check if arguments are provided
if [ -z "$INPUT_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
  echo "Usage: $0 <input_text_file> <output_pdf_file> [style_tex_path]" >&2
  exit 1
fi

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: Input file '$INPUT_FILE' not found!" >&2
  exit 1
fi

# Get script directory for finding style.tex
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use custom style.tex if provided, otherwise use default
if [ -z "$STYLE_TEX" ]; then
  STYLE_TEX="$SCRIPT_DIR/style.tex"
fi

# Check if style.tex exists
if [ ! -f "$STYLE_TEX" ]; then
  echo "Error: Style file '$STYLE_TEX' not found!" >&2
  exit 1
fi

# Convert using pandoc
echo "Converting with pandoc using style: $STYLE_TEX"
pandoc "$INPUT_FILE" \
  -o "$OUTPUT_FILE" \
  --pdf-engine=xelatex \
  --include-in-header="$STYLE_TEX"

if [ $? -eq 0 ]; then
  echo "PDF generated: $OUTPUT_FILE"
  exit 0
else
  echo "Error: Pandoc conversion failed!" >&2
  exit 1
fi
