from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Placeholder


class ChatScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Button(label="Profile", variant="success", id="change_profile")

    async def on_button_pressed(self) -> None:
        self.app.switch_mode("profile")


class ProfileScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Button(label="Help", variant="success", id="change_profile")
        yield Placeholder("A profile")

    async def on_button_pressed(self) -> None:
        self.app.switch_mode("help")


class HelpScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Button(label="Chat", variant="success", id="change_profile")

    async def on_button_pressed(self) -> None:
        self.app.switch_mode("chat")


class DemoApp(App[None]):
    MODES = {
        "profile": ProfileScreen,
        "chat": ChatScreen,
        "help": HelpScreen,
    }

    def on_mount(self) -> None:
        """On running"""
        # LOGGER.info("Starting")
        self.switch_mode("chat")


if __name__ == "__main__":
    app = DemoApp()
    app.run()
