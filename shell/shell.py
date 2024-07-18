import contextlib
import io
import os
import sys
from shell.commander import CommandExecutor, CommandValidator
from logger.logger import Logger
import re

from shell.script_tester import ScriptTester

ALLOWED_INITIAL_COMMANDS = [
    "write",
    "read",
    "erase",
    "erase_range",
    "exit",
    "help",
    "fullwrite",
    "fullread",
]


class Shell:

    def __init__(self) -> None:
        self.is_run = False
        self.ssd_dir: str = "../"
        self.command_executor: CommandExecutor = CommandExecutor()
        self.command_validator: CommandValidator = CommandValidator()
        self.logger: Logger = Logger()
        self.script_tester = ScriptTester(self.command_executor, self.command_validator)

    def run(self) -> None:
        self.logger.print("User IP:192.XX.XX.XX be connected")
        print("Hello ! Welcome to the Aut ut hul shell !")

        self.is_run = True
        while self.is_run:
            try:
                user_inputs = input().split()
                if not self.command_validator.is_valid_command(user_inputs):
                    print("INVALID COMMAND")
                    self.logger.print(f"INVALID COMMAND - {" ".join(user_inputs)}")
                    continue
                self.is_run = self.command_executor.execute_command(user_inputs)

            except Exception as e:
                self.logger.print(e)

        self.logger.print("User IP:192.XX.XX.XX be disconnected")
        print("See you !")

    def run_test_list(self, test_list_file: str) -> None:
        self.script_tester.run_test_list(test_list_file)
