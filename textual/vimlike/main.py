from textual.app import ComposeResult, App
from textual.binding import Binding
from textual.widgets import TextArea

from enum import Enum

# TODO: Implement a VIM like mode-based application
# - Add a modehandler class which maintains a global variable


MODES = Enum("normal_mode", "insert_mode", "visual_mode")
MODES_DICT = {
    "normal": {
        "insert": ["cur_before", "cur_after", "line_before", "line_after"],
        "command": [],
    }
}


class AppClass(App):
    BINDINGS = [
        Binding("escape", "set_mode('normal_mode')", priority=True),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = "normal"

    def compose(self) -> ComposeResult:
        yield TextArea(read_only=True)

    def action_set_mode(self, mode: str) -> None:
        self.mode = mode
        self.query_one(TextArea).text = self.mode


if __name__ == "__main__":
    AppClass().run()
