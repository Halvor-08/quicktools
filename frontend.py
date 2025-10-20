from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.widgets import DataTable, Footer, Header, Input, Button

from quicklist_backend import DataBackend


class ModesBox(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Search", id="search")
        yield Button("Insert", id="insert")
        yield Button("Delete", id="delete")
        yield Button("Load", id="load_file")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        match button_id:
            case "search":
                self.add_class("selected")
            case "insert":
                self.add_class("selected")
            case "delete":
                self.add_class("selected")
            case "load_file":
                self.add_class("selected")


class ContentBox(DataTable):
    def on_mount(self): ...


class Quicklist(Container):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.backend = DataBackend()

    def compose(self) -> ComposeResult:
        yield ContentBox()
        yield Input(
            placeholder="Enter search term", type="text"
        )  # Add suggester support

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.backend.data[0].keys())
        self.update_table(self.backend.data)

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
        ("s", "search_mode", "Enter Search Mode"),
        ("a", "add_mode", "Enter Insertion Mode"),
        ("d", "delete_mode", "Enter Deletion Mode"),
        ("l", "loading_mode", "Enter File Loading Mode"),
        ("esc", "normal_mode", "Enter Normal Mode"),
    ]
    CSS_PATH = "quicklist.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Quicklist()
        yield Footer()

    def action_add_mode(self) -> None:
        search_bar = self.query_one(Quicklist).query_one(Input)
        search_bar.focus()

    def action_delete_mode(self) -> None: ...
    def action_loading_mode(self) -> None: ...
    # Can be replaced by DB loading abstraction
    def action_search_mode(self) -> None:
        search_bar = self.query_one(Quicklist).query_one(Input)
        search_bar.focus()

    def action_normal_mode(self) -> None:
        self.query_one(Quicklist).query_one(DataTable).focus()


if __name__ == "__main__":
    frontend = QuickListApp()
    frontend.run()
