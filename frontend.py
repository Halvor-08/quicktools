from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input
from textual.binding import Binding

from backend import DataBackend
from typing import Literal

InputType = Literal["integer", "number", "text"]
DB_ENTRY = DataBackend()


class MyInput(Input):
    BINDINGS = [Binding("escape", "blur")]

    def action_blur(self) -> None:
        self.blur()


class AddModeForm(Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entry = {}

    def compose(self) -> ComposeResult:
        for elem in DB_ENTRY.entry_template:
            yield MyInput(
                placeholder=elem.key_name,
                type=self.convert_to_input_type(elem.data_type),
                id=elem.key_name,
            )
            yield Button(label="Confirm", id=f"{elem.key_name}_confirm")

    def convert_to_input_type(self, data_type: type) -> InputType:
        if data_type is int:
            return "integer"
        elif data_type is float:
            return "number"
        else:
            return "text"

    def on_input_submitted(self, event: MyInput.Submitted) -> None:
        value = event.value
        key = event.input.id
        self.entry[key] = value

        # TODO: Remove, is a debug feature
        confirm_button = self.query_one(f"#{key}_confirm", Button)
        confirm_button.label = value

    def on_mount(self): ...


class SearchBar(Input):
    BINDINGS = [Binding("escape", "blur")]

    def action_blur(self) -> None:
        self.blur()


class Quicklist(Container):
    def compose(self) -> ComposeResult:
        yield DataTable()
        yield SearchBar(
            placeholder="Enter search term",
            type="text",
        )  # Add suggester support

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*DB_ENTRY.data[0].keys())
        self.update_table(DB_ENTRY.data)

        self.query_one(Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        query = event.value
        results = DB_ENTRY.search({"name": query})
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
    BINDINGS = [
        ("enter", "", "Edit selected cell"),
        ("i", "", "Insert before selection"),
        ("a", "", "Insert after selection"),
        ("d", "", "Deleted selected cell contents"),
        ("c", "", "Select current column"),
        ("r", "", "Select current row"),
    ]  # TODO: Implement this, probably use reactive elements for selectors as flags

    def __init__(
        self, name: str | None = None, id: str | None = None, classes: str | None = None
    ) -> None:
        super().__init__(name, id, classes)
        print("Entered normal mode")

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
        ("n", "switch_mode('normal_mode')", "Enter Normal Mode"),
        ("a", "switch_mode('add_mode')", "Enter Insertion Mode"),
        ("i", "insert_mode", "Insert a new entry"),
        ("d", "delete_mode", "Enter Deletion Mode"),
        ("l", "loading_mode", "Enter File Loading Mode"),
        ("esc", "switch_mode('normal_mode')", "Enter Normal Mode"),
        Binding("escape", "switch_mode('normal_mode')", priority=True),
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
