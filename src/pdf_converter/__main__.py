"""Entry point for running pdf_converter as a module."""

from .app import PDFConverterApp


def main():
    """Main entry point."""
    app = PDFConverterApp()
    app.run()


if __name__ == "__main__":
    main()
