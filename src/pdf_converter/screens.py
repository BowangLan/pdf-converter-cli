"""Screen components for PDF Converter TUI."""

import os
import subprocess
import platform
from pathlib import Path
from datetime import datetime

from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Static, Input, TextArea, ListItem, ListView, Button, Label
from textual.containers import Vertical, Horizontal
from textual.binding import Binding
from textual.app import ComposeResult

from .config import PDFConverterConfig


class LoadingScreen(ModalScreen[None]):
    """Modal screen to show loading/pending status."""

    def __init__(self, message: str = "Processing...", **kwargs):
        super().__init__(**kwargs)
        self.message_text = message

    def compose(self) -> ComposeResult:
        with Vertical(id="loading-dialog"):
            yield Static("Please Wait", classes="dialog-title")
            yield Static(f"\n{self.message_text}\n", id="loading-message")


class MessageScreen(ModalScreen[None]):
    """Modal screen to show messages."""

    BINDINGS = [
        Binding("enter", "dismiss", "Continue"),
        Binding("escape", "dismiss", "Continue"),
    ]

    def __init__(self, title: str, message: str, **kwargs):
        super().__init__(**kwargs)
        self.title_text = title
        self.message_text = message

    def compose(self) -> ComposeResult:
        with Vertical(id="message-dialog"):
            yield Static(self.title_text, classes="dialog-title")
            yield Static(f"\n{self.message_text}\n")
            yield Button("Continue", variant="primary", id="continue-btn")

    def action_dismiss(self) -> None:
        """Dismiss the message."""
        self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        self.dismiss()


class ConfirmClearScreen(ModalScreen[bool]):
    """Modal screen to confirm clearing document."""

    BINDINGS = [
        Binding("y", "confirm", "Yes"),
        Binding("n", "cancel", "No"),
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-dialog"):
            yield Static("Clear Document", classes="dialog-title")
            yield Static("\nAre you sure you want to clear all text?\nThis cannot be undone.\n")
            with Horizontal(classes="button-row"):
                yield Button("Yes (Y)", variant="error", id="confirm-yes")
                yield Button("No (N)", variant="primary", id="confirm-no")

    def action_confirm(self) -> None:
        """Confirm the clear action."""
        self.dismiss(True)

    def action_cancel(self) -> None:
        """Cancel the clear action."""
        self.dismiss(False)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "confirm-yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class NameInputScreen(ModalScreen[str]):
    """Modal screen to input document name."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="name-input-dialog"):
            yield Static("Enter Document Name", classes="dialog-title")
            yield Static("\nEnter the name for your document (e.g., 'SpaceX', 'Google', etc.)\n")
            yield Input(placeholder="Name", id="name-input")
            with Horizontal(classes="button-row"):
                yield Button("Continue", variant="primary", id="continue-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")

    def on_mount(self) -> None:
        """Focus the input when mounted."""
        self.query_one(Input).focus()

    def action_cancel(self) -> None:
        """Cancel the input."""
        self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "continue-btn":
            name = self.query_one("#name-input", Input).value.strip()
            if name:
                self.dismiss(name)
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        name = event.value.strip()
        if name:
            self.dismiss(name)


class EditorScreen(Screen):
    """Full-screen text editor."""

    BINDINGS = [
        Binding("ctrl+s", "save", "Save & Convert", priority=True),
        Binding("ctrl+l", "clear", "Clear", priority=True),
        Binding("escape", "cancel", "Cancel", priority=True),
    ]

    def __init__(self, filepath: str, content: str = "", **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        self.initial_content = content
        self.saved = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TextArea(self.initial_content, language="markdown", id="editor")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the editor."""
        self.sub_title = f"File: {self.filepath}"
        self.query_one(TextArea).focus()

    async def action_save(self) -> None:
        """Save file and convert to PDF."""
        text_area = self.query_one(TextArea)
        self.saved = True
        self.dismiss(text_area.text)

    def action_cancel(self) -> None:
        """Cancel without saving."""
        self.dismiss(None)

    async def action_clear(self) -> None:
        """Clear all text with confirmation."""
        confirmed = await self.app.push_screen_wait(ConfirmClearScreen())
        if confirmed:
            text_area = self.query_one(TextArea)
            text_area.clear()


class FileListScreen(Screen):
    """Main screen with file list."""

    BINDINGS = [
        Binding("n", "new_document", "New"),
        Binding("q", "quit", "Quit"),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = PDFConverterConfig()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Text Files (sorted by last modified)", id="list-title")
        yield ListView(id="file-list")
        yield Footer()

    def on_mount(self) -> None:
        """Load file list when mounted."""
        self.title = "PDF Converter"
        self.refresh_file_list()

    def refresh_file_list(self) -> None:
        """Refresh the file list."""
        file_list = self.query_one("#file-list", ListView)
        file_list.clear()

        txt_files = self.get_txt_files()

        if not txt_files:
            file_list.append(ListItem(Label("No .txt files found. Press 'N' to create a new document.")))
        else:
            for file_info in txt_files:
                label_text = f"{file_info['name']:<45} {file_info['mtime_str']}"
                item = ListItem(Label(label_text))
                item.file_info = file_info
                file_list.append(item)

    def get_txt_files(self):
        """Get list of .txt files in output directory, sorted by modification time."""
        txt_files = []
        output_dir = self.config.config.get("output_directory", ".")

        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for file in Path(output_dir).glob('*.txt'):
            if file.is_file():
                stat = file.stat()
                txt_files.append({
                    'name': file.name,
                    'path': str(file),
                    'mtime': stat.st_mtime,
                    'mtime_str': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })

        txt_files.sort(key=lambda x: x['mtime'], reverse=True)
        return txt_files

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle file selection."""
        if hasattr(event.item, 'file_info'):
            self.run_worker(self.convert_file_to_pdf(event.item.file_info))

    def action_new_document(self) -> None:
        """Create a new document."""
        self.run_worker(self._new_document_worker())

    async def _new_document_worker(self) -> None:
        """Worker for creating a new document."""
        name = await self.app.push_screen_wait(NameInputScreen())
        if name:
            await self.create_new_document(name)

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_cursor_down(self) -> None:
        """Move cursor down in list."""
        file_list = self.query_one("#file-list", ListView)
        file_list.action_cursor_down()

    def action_cursor_up(self) -> None:
        """Move cursor up in list."""
        file_list = self.query_one("#file-list", ListView)
        file_list.action_cursor_up()

    async def create_new_document(self, name: str) -> None:
        """Create and edit a new document."""
        filepath = self.config.get_filename(name, "text_filename_format")

        # Ensure parent directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        # Read existing content if file exists
        content = ""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
        else:
            Path(filepath).touch()

        # Open editor
        result = await self.app.push_screen_wait(EditorScreen(filepath, content))

        if result is not None:
            # Save the file
            with open(filepath, 'w') as f:
                f.write(result)

            # Convert to PDF
            await self.convert_to_pdf(name, filepath)

        # Refresh file list
        self.refresh_file_list()

    async def convert_file_to_pdf(self, file_info: dict) -> None:
        """Convert an existing file to PDF."""
        txt_file = file_info['path']

        # Extract name from filename
        filename_base = Path(txt_file).stem
        text_format = self.config.config.get("text_filename_format", "{name}.txt")

        if "{name}" in text_format:
            suffix = text_format.split("{name}")[-1].replace(".txt", "")
            if suffix and filename_base.endswith(suffix):
                name = filename_base[:-len(suffix)]
            else:
                name = filename_base
        else:
            name = filename_base

        await self.convert_to_pdf(name, txt_file)

    async def convert_to_pdf(self, name: str, txt_file: str) -> None:
        """Convert text file to PDF."""
        pdf_filename = self.config.get_filename(name, "pdf_filename_format")
        conversion_script = self.config.get_conversion_script()
        style_template = self.config.get_style_template()

        # Show loading screen
        loading_screen = LoadingScreen(f"Converting {Path(txt_file).name} to PDF...\n\nThis may take a few seconds.")
        self.app.push_screen(loading_screen)

        success = False
        error_msg = ""

        try:
            result = subprocess.run(
                [conversion_script, txt_file, pdf_filename, style_template],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                success = True
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
        except subprocess.TimeoutExpired:
            error_msg = "Conversion timed out"
        except FileNotFoundError:
            error_msg = f"Conversion script not found: {conversion_script}"
        except Exception as e:
            error_msg = str(e)

        # Dismiss loading screen
        self.app.pop_screen()

        # Show result
        if success:
            # Auto-open the PDF
            try:
                system = platform.system()
                if system == 'Darwin':  # macOS
                    subprocess.Popen(['open', pdf_filename])
                elif system == 'Linux':
                    subprocess.Popen(['xdg-open', pdf_filename])
                elif system == 'Windows':
                    subprocess.Popen(['start', pdf_filename], shell=True)
            except Exception:
                pass

            await self.app.push_screen_wait(
                MessageScreen(
                    "✓ SUCCESS",
                    f"File saved: {Path(txt_file).name}\nPDF created: {Path(pdf_filename).name}\n\nPDF opened automatically."
                )
            )
        else:
            await self.app.push_screen_wait(
                MessageScreen(
                    "✗ CONVERSION FAILED",
                    f"File saved: {Path(txt_file).name}\nError: {error_msg}"
                )
            )
