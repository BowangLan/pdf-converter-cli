# PDF Converter CLI

A modern TUI (Text User Interface) application built with Textual that lets you create and edit text files, then automatically converts them to PDF. Features a beautiful full-screen interface with modal dialogs and smooth interactions.

## Features

- 📋 **File List View** - Browse all .txt files in the documents directory, sorted by last modified
- ⌨️ **Vim-style Navigation** - Use arrow keys or j/k to navigate through files
- ⚡ **Quick Convert** - Select any file and press Enter to convert it to PDF instantly
- 🚀 **Auto-Open PDF** - PDFs automatically open in your default viewer after conversion
- ✏️ **Full-Screen Editor** - Powerful text editor with syntax highlighting
- 🎨 **Beautiful PDF Output** - Formatted with pandoc (1" margins, 12pt, 1.6 line spacing)
- 🎭 **Modern UI** - Built with Textual for a rich, responsive terminal experience
- ⌨️ **Keyboard Shortcuts** - Efficient keyboard-driven workflow
- 🔧 **Configurable** - Customize file naming, paths, and styling

## Installation

### Prerequisites

1. **Python 3.10+** - Make sure Python is installed
2. **Pandoc** - Required for PDF conversion
3. **XeLaTeX** - Required by pandoc for PDF generation

Install the prerequisites:

```bash
# macOS
brew install pandoc
brew install --cask mactex-no-gui  # For XeLaTeX

# Ubuntu/Debian
sudo apt-get install pandoc texlive-xetex

# Fedora
sudo dnf install pandoc texlive-xetex
```

### Install PDF Converter CLI

#### Quick Install (macOS/Linux)

```bash
# Clone the repository
git clone <your-repo-url>
cd pdf-converter-cli

# Run the installation script
./install.sh
```

The install script will:
- Check if uv is installed (and guide you to install it if not)
- Warn you about missing dependencies (pandoc, xelatex)
- Create config.json from the example
- Install Python dependencies (textual)

#### Manual Installation

**Option 1: Install with uv (recommended)**

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
# Install uv if you don't have it
brew install uv
# or: curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <your-repo-url>
cd pdf-converter-cli

# Install dependencies
uv pip install textual
```

**Option 2: Install with pip**

```bash
# Clone the repository
git clone <your-repo-url>
cd pdf-converter-cli

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install textual
```

## Usage

### Quick Start

After running `./install.sh`, run the application:

**Option 1: Use the run script (easiest)**
```bash
./run.sh
```

**Option 2: Run as a module**
```bash
PYTHONPATH=src uv run python -m pdf_converter
```

**Option 3: Run the main script**
```bash
uv run main.py
```

### Making It Easier to Run (Optional)

Add an alias to your shell for quick access:

```bash
# For zsh (add to ~/.zshrc)
alias pdfconv='cd /path/to/pdf-converter-cli && ./run.sh'

# Or
alias pdfconv='cd /path/to/pdf-converter-cli && PYTHONPATH=src uv run python -m pdf_converter'

# Or
alias pdfconv='cd /path/to/pdf-converter-cli && uv run main.py'
```

Replace `/path/to/pdf-converter-cli` with the actual path to this project.

Then reload your shell:
```bash
source ~/.zshrc
```

### Workflow

1. **Launch the application** - Enters full-screen file list view
2. **Create or select a document**:
   - Press **`N`** to create a new document
   - Or use **`↑/↓`** or **`j/k`** to select an existing file and press **`Enter`**
3. **Edit in the full-screen editor**
4. **Save and convert** - Press **`Ctrl+S`** to save and convert to PDF
5. **PDF auto-opens** in your default viewer

### Keyboard Shortcuts

#### Command Mode (File List)
- **`↑/↓`** or **`j/k`** - Navigate up/down through file list
- **`Enter`** - Convert selected file to PDF
- **`N`** - Create new document
- **`Q`** or **`Ctrl+C`** - Quit application

#### Name Input
- **`Enter`** - Confirm name
- **`Ctrl+Q`** or **`Ctrl+C`** - Cancel

#### Editor Mode
- **`Ctrl+S`** - Save and convert to PDF
- **`Ctrl+L`** - Clear all text (with confirmation)
- **`Ctrl+Q`** - Cancel without saving

## Configuration

Copy the example config and customize it:

```bash
cp config.json.example config.json
```

Edit `config.json`:

```json
{
  "text_filename_format": "{name}_Cover_Letter.txt",
  "pdf_filename_format": "{name}_Cover_Letter.pdf",
  "conversion_script": "./scripts/convert_to_pdf.sh",
  "style_template": "./templates/style.tex",
  "output_directory": "./documents"
}
```

### Configuration Options

- **`text_filename_format`** - Template for text file names (use `{name}` as placeholder)
- **`pdf_filename_format`** - Template for PDF file names (use `{name}` as placeholder)
- **`conversion_script`** - Path to the conversion script
- **`style_template`** - Path to the LaTeX style template
- **`output_directory`** - Directory where documents are saved

### Customizing PDF Style

Edit `templates/style.tex` to customize PDF appearance:

```latex
% Margins
\usepackage[margin=1in]{geometry}

% Font size and line spacing
\usepackage{fontspec}
\setmainfont{Times New Roman}
\linespread{1.6}

% Add your custom styles here
```

## Project Structure

```
pdf-converter-cli/
├── src/
│   └── pdf_converter/           # Main package
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Module entry point
│       ├── app.py               # Main TUI application
│       ├── config.py            # Configuration management
│       └── screens.py           # UI screen components
├── scripts/
│   └── convert_to_pdf.sh        # PDF conversion script
├── templates/
│   └── style.tex                # LaTeX style template
├── documents/                    # Output directory for documents
│   ├── .gitkeep
│   ├── *.txt                    # Text files (git-ignored)
│   └── *.pdf                    # PDF files (git-ignored)
├── main.py                      # Main entry point script
├── install.sh                   # Quick installation script
├── run.sh                       # Quick run script
├── config.json                  # User configuration (auto-created)
├── config.json.example          # Example configuration
├── pyproject.toml               # Project metadata and dependencies
├── LICENSE                      # MIT License
├── README.md                    # This file
└── .gitignore                   # Git ignore patterns
```

## Example Workflow

### Creating a New Document:

```
[App launches - shows file list]
  Text Files (sorted by last modified):

  → Google_Cover_Letter.txt              2025-12-29 14:30:22
    Tesla_Cover_Letter.txt               2025-12-28 09:15:45
    SpaceX_Cover_Letter.txt              2025-12-27 18:22:10

  Use ↑↓ or j/k to navigate | Enter to convert | N for new | Q to quit

[Press 'N']

[Full-screen name input]
Name: Amazon
[Press Enter]

[Full-screen editor opens with Amazon_Cover_Letter.txt]
[Paste/type your cover letter text]
[Press Ctrl+S]

[Loading screen appears]
⏳ Converting Amazon_Cover_Letter.txt to PDF...

This may take a few seconds.

[PDF automatically opens in default viewer]

[Success message]
✓ SUCCESS
File saved: Amazon_Cover_Letter.txt
PDF created: Amazon_Cover_Letter.pdf

PDF opened automatically.
[Press Enter]

[Returns to command mode - Amazon file now appears at top of list]
```

## Development

### Running from Source

```bash
# Clone and navigate to the project
git clone <your-repo-url>
cd pdf-converter-cli

# Install dependencies with uv (recommended)
uv pip install textual

# Or with traditional pip
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install textual

# Run the application
./run.sh
# or
PYTHONPATH=src uv run python -m pdf_converter
# or
uv run main.py
```

### Project Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Textual 0.47.0+
- Pandoc (external dependency)
- XeLaTeX (external dependency)

## Technical Details

This application is built using:
- **Textual** - Modern TUI framework for Python
- **Modal Screens** - For dialogs and user input
- **TextArea Widget** - Full-featured text editor with syntax highlighting
- **ListView Widget** - For browsing files with keyboard navigation
- **CSS Styling** - Custom styling for a polished look
- **Pandoc** - Document converter for generating PDFs
- **XeLaTeX** - LaTeX engine for high-quality PDF output

## Troubleshooting

### "Conversion script not found"
Make sure `scripts/convert_to_pdf.sh` is executable:
```bash
chmod +x scripts/convert_to_pdf.sh
```

### "pandoc: command not found"
Install pandoc:
```bash
# macOS
brew install pandoc

# Ubuntu/Debian
sudo apt-get install pandoc
```

### PDF conversion fails
Ensure XeLaTeX is installed:
```bash
# macOS
brew install --cask mactex-no-gui

# Ubuntu/Debian
sudo apt-get install texlive-xetex
```

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
