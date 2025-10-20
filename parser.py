# Provides a framework for handling user input
from parser import create_parser
from database import JsonDatabase

class InputParser:
    def __init__(self):
        self.dict = {}

    def ask_input(self, key: str, stdin_str: str) -> None:
        self.dict[key] = input(stdin_str)


