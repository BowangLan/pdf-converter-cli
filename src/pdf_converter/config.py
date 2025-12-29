"""Configuration management for PDF converter."""

import json
import sys
from pathlib import Path


class PDFConverterConfig:
    """Configuration manager for PDF converter."""

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config
            default_config = {
                "text_filename_format": "{name}_Cover_Letter.txt",
                "pdf_filename_format": "{name}_Cover_Letter.pdf",
                "conversion_script": "./scripts/convert_to_pdf.sh",
                "style_template": "./templates/style.tex",
                "output_directory": "./documents"
            }
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
        except json.JSONDecodeError:
            sys.exit(1)

    def get_filename(self, name, format_key):
        """Generate filename from config format and name."""
        format_str = self.config.get(format_key, "")
        filename = format_str.format(name=name)

        # Add output directory if configured
        output_dir = self.config.get("output_directory", "")
        if output_dir:
            return str(Path(output_dir) / filename)
        return filename

    def get_conversion_script(self):
        """Get the path to the conversion script."""
        return self.config.get("conversion_script", "./scripts/convert_to_pdf.sh")

    def get_style_template(self):
        """Get the path to the style template."""
        return self.config.get("style_template", "./templates/style.tex")
