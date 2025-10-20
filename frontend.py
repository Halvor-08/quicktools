from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Input, Static

from quicklist_backend import DataBackend


class AddModeForm(Container):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter name", id="add_name")
        yield Input(placeholder="Enter type", id="add_type")
        yield Input(placeholder="Enter other", id="add_other")


class ContentBox(DataTable):
    def on_mount(self): ...


class SearchBar(Input): ...


class Quicklist(Container):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.backend = DataBackend()

    def compose(self) -> ComposeResult:
        yield ContentBox()
        yield SearchBar(
            placeholder="Enter search term",
            type="text",
        )  # Add suggester support

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.backend.data[0].keys())
        self.update_table(self.backend.data)

        self.query_one(Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        query = event.value
        results = self.backend.search({"name": query})
        self.update_table(results)

    def update_table(self, data: list[dict]) -> None:
        # Update the datatable component
        table = self.query_one(DataTable)
        table.clear()

        if data:
            rows = [tuple(d.values()) for d in data]
            table.add_rows(rows)


class InsertMode(Screen):
    def compose(self) -> ComposeResult:
        yield Quicklist()
        yield AddModeForm()


class NormalMode(Screen):
    def compose(self) -> ComposeResult:
        yield Quicklist()


class QuickListApp(App):
    # TODO:
    # - implement mode switching
    """
    Main application class, handles:
    - keybinds
    - mode switching
    - application wide settings
    """

    BINDINGS = [
        ("s", "switch_mode('normal_mode')", "Enter Search Mode"),
        ("a", "switch_mode('add_mode')", "Enter Insertion Mode"),
        ("d", "delete_mode", "Enter Deletion Mode"),
        ("l", "loading_mode", "Enter File Loading Mode"),
        ("esc", "switch_mode('normal_mode')", "Enter Normal Mode"),
    ]
    MODES = {
        "add_mode": InsertMode,
        "normal_mode": NormalMode,
    }
    CSS_PATH = "quicklist.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Quicklist()
        yield Footer()


if __name__ == "__main__":
    frontend = QuickListApp()
    frontend.run()
