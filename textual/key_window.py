from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Placeholder
from textual.reactive import reactive
from textual.containers import Container


class Test1(Screen):
    def compose(self) -> ComposeResult:
        yield Quicklist()


class Test2(Screen):
    def compose(self) -> ComposeResult:
        yield Quicklist()


class Quicklist(Container):
    def compose(self) -> ComposeResult:
        yield Placeholder("test2")


class newWindowApp(App):
    BINDINGS = [("a", "add_test", "Add a Test placeholder"), ("d", "delete", "delete")]
    MODES = {"mode1": Test1, "Mode2": Test2}

    mode = reactive(1)

    def compose(self) -> ComposeResult:
        yield Test1()

    def action_add_test(self) -> None:
        self.switch_mode("mode1")

    def action_delete(self) -> None:
        self.switch_mode("Mode2")


if __name__ == "__main__":
    newWindowApp().run()
