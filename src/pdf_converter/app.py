"""Main PDF Converter Application."""

from textual.app import App

from .screens import FileListScreen


class PDFConverterApp(App):
    """PDF Converter TUI Application."""

    CSS = """
    #list-title {
        background: $accent;
        color: $text;
        padding: 1;
        text-align: center;
        text-style: bold;
    }

    #file-list {
        border: solid $primary;
    }

    ListView {
        height: 1fr;
    }

    ListItem {
        padding: 0 2;
    }

    /* Modal dialogs */
    ModalScreen {
        align: center middle;
    }

    #confirm-dialog, #message-dialog, #name-input-dialog, #loading-dialog {
        background: $surface;
        border: thick $primary;
        width: 60;
        height: auto;
        padding: 1 2;
    }

    .dialog-title {
        background: $accent;
        color: $text;
        text-align: center;
        text-style: bold;
        padding: 1;
        margin-bottom: 1;
    }

    .button-row {
        align: center middle;
        height: auto;
        margin-top: 1;
    }

    .button-row Button {
        margin: 0 1;
    }

    #name-input {
        margin: 1 0;
    }
    """

    def on_mount(self) -> None:
        """Set up the application."""
        self.push_screen(FileListScreen())
