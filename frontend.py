from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, RichLog
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


class InsertBlock(Container):
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


class CellInput(Input):
    def on_input_submitted(self, event: Input.Submitted) -> None:
        caller = self.query_ancestor(DataContainer)
        caller.update_cell_value(event.value)


class DataContainer(Container):
    insert_flag = reactive(False)

    # {
    #     'row': '',
    #     'col': '',
    # }

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield RichLog()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*DB_ENTRY.data[0].keys())
        self.update_table(DB_ENTRY.data)

    def update_table(self, data: list[dict]) -> None:
        # Update the datatable component
        table = self.query_one(DataTable)
        table.clear()

        if data:
            rows = [tuple(d.values()) for d in data]
            table.add_rows(rows)

    def watch_insert_flag(self):
        if self.insert_flag is True:
            self.update_cell()

    def update_cell(self):
        datatable = self.query_one(DataTable)
        cell = datatable.cursor_coordinate
        self.query_one(RichLog).write(
            f"Cell at {cell}, with data {datatable.get_cell_at(cell)}"
        )
        self.mount(Input())
        cell_input = self.query_one(Input)
        cell_input.focus()

    def update_cell_value(self, new_value):
        dt = self.query_one(DataTable)
        row = dt.cursor_coordinate.row
        dt_coordinate = dt.update_cell(row, column, new_value)


class QuickListApp(App):
    # TODO:
    # - implement mode switching
    """
    Main application class, handles:
    - keybinds
    - application wide settings
    """

    # TODO:
    # - Add o and O for column insertions
    BINDINGS = [
        ("n", "set_mode('normal')", "Enter Normal Mode"),
        ("a", "set_mode('add_after')", "Enter Insertion Mode"),
        ("i", "set_mode('add_before')", "Insert a new entry"),
        ("d", "set_mode('delete')", "Enter Deletion Mode"),
        Binding("escape", "set_mode('normal')", priority=True),
    ]

    CSS_PATH = "quicklist.tcss"

    mode = reactive("normal")

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataContainer()
        yield SearchBar(
            placeholder="Enter search term",
            type="text",
        )  # Add suggester support
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        query = event.value
        results = DB_ENTRY.search({"name": query})
        table = self.query_one(DataContainer)
        table.update_table(results)

    def action_set_mode(self, mode):
        self.mode = mode

    def watch_mode(self):
        self.query_one(SearchBar).placeholder = self.mode
        self.query_one(DataContainer).insert_flag = True


if __name__ == "__main__":
    frontend = QuickListApp()
    frontend.run()
