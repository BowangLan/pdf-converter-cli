# Repository Guidelines

## Project Structure & Module Organization
- `src/pdf_converter/` holds the main Textual TUI package (`app.py`, `screens.py`, `config.py`).
- `main.py` and `src/pdf_converter/__main__.py` are entry points for running the app.
- `scripts/convert_to_pdf.sh` performs the pandoc/XeLaTeX PDF conversion.
- `templates/style.tex` defines the LaTeX styling for PDF output.
- `documents/` stores generated `.txt` and `.pdf` files (kept out of git).
- `config.json` is user-specific configuration; copy from `config.json.example`.

## Build, Test, and Development Commands
- `./install.sh` sets up `config.json` and installs Python dependencies.
- `./run.sh` launches the TUI app with the expected environment.
- `PYTHONPATH=src uv run python -m pdf_converter` runs the module directly.
- `uv run main.py` runs the main script entry point.

## Coding Style & Naming Conventions
- Python 3.10+ codebase; follow standard PEP 8 formatting.
- Use 4-space indentation, `snake_case` for functions/variables, `PascalCase` for classes.
- Keep UI logic in `app.py`/`screens.py`, configuration in `config.py`.

## Testing Guidelines
- No automated test suite is currently configured.
- Validate changes by running `./run.sh` and exercising file creation/edit/convert flows.

## Commit & Pull Request Guidelines
- Recent commits use short, descriptive sentences (e.g., “updated readme”).
- Keep commit messages concise, lowercase, and focused on one change.
- Pull requests should describe user-facing impact, list manual test steps, and include screenshots/GIFs for UI changes when feasible.

## Configuration & Dependencies
- Requires external tools: `pandoc` and `xelatex` for PDF conversion.
- Ensure `scripts/convert_to_pdf.sh` remains executable (`chmod +x`).
