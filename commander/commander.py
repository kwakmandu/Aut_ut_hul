import contextlib
import subprocess
import sys
from typing import io

from shell.helper import Helper
from logger.logger import Logger

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


class Commander:
    def __init__(self) -> None:
        self.__command: list[str] = []
        self.ssd_path: str = "../ssd"
        self.helper: Helper = Helper()
        self.logger: Logger = Logger()

    def set_command(self, command: list[str]) -> None:
        self.__command = command

    def get_command(self) -> list[str]:
        return self.__command

    def is_valid_command(self) -> bool:
        if self.__command[0] not in ALLOWED_INITIAL_COMMANDS:
            return False

        if self.__command[0] == "write":
            return (
                len(self.__command) == 3
                and self.__is_valid_address(self.__command[1])
                and self.__is_valid_hex(self.__command[2])
            )

        elif self.__command[0] == "read":
            return len(self.__command) == 2 and self.__is_valid_address(
                self.__command[1]
            )

        elif self.__command[0] == "fullwrite":
            return len(self.__command) == 2 and self.__is_valid_hex(self.__command[1])

        elif self.__command[0] == "erase":
            return (
                len(self.__command) == 3
                and self.__is_valid_address(self.__command[1])
                and self.__is_valid_address(self.__command[2])
            )
        elif self.__command[0] == "erase_range":
            return (
                len(self.__command) == 3
                and self.__is_valid_address(self.__command[1])
                and self.__is_valid_address(self.__command[2])
                and int(self.__command[1]) < int(self.__command[2])
            )

        elif len(self.__command) == 1:
            return True

        return False

    def __is_valid_address(self, value: str) -> bool:
        return value.isdigit() and 0 <= int(value) <= 99

    def __is_valid_hex(self, value: str) -> bool:
        if len(value) != 10 or value[:2] != "0x":
            return False
        return all(char in "0123456789ABCDEF" for char in value[2:])

    def execute_command(self) -> None:
        if len(self.__command) < 1:
            return

        match self.__command[0]:
            case "write":
                self.write(self.__command[1], self.__command[2])
            case "read":
                self.read(self.__command[1])
            case "erase":
                self.erase(self.__command[1], self.__command[2])
            case "erase_range":
                self.erase(self.__command[1], self.__command[2])
            case "exit":
                self.exit()
            case "help":
                self.help()
            case "fullwrite":
                self.fullwrite(self.__command[1])
            case "fullread":
                self.fullread()
            case _:
                print("INVALID COMMAND")

    def write(self, address: str, data: str) -> None:
        self.logger.print(f"write {address} {data}")
        subprocess.run(
            [sys.executable, f"{self.ssd_path}/virtual_ssd.py", "W", address, data]
        )

    def read(self, address: str) -> None:
        self.logger.print(f"read {address}")
        subprocess.run(
            [sys.executable, f"{self.ssd_path}/virtual_ssd.py", "R", address]
        )
        try:
            with open(f"{self.ssd_path}/result.txt", "r") as file:
                file_contents = file.read().strip()
                print(file_contents)
        except FileNotFoundError:
            print("파일이 존재하지 않습니다.")

    def erase(self, address: str, size: str) -> None:
        self.logger.print(f"erase {address} {size}")
        isize = int(size)
        while isize > 10:
            subprocess.run(
                [sys.executable, f"{self.ssd_path}/virtual_ssd.py", "E", address, "10"]
            )
            isize -= 10
        subprocess.run(
            [
                sys.executable,
                f"{self.ssd_path}/virtual_ssd.py",
                "E",
                address,
                str(isize),
            ]
        )

    def exit(self) -> None:
        self.logger.print(f"exit")
        self.is_run = False

    def help(self) -> None:
        self.logger.print(f"help")
        for h_info in self.helper.get_help_information():
            print(h_info)

    def fullwrite(self, data: str) -> None:
        self.logger.print(f"fullwrite {data}")
        for i in range(100):
            self.write(str(i), data)

    def fullread(self) -> None:
        self.logger.print(f"fullread")
        for i in range(100):
            self.read(str(i))

    def run_test(self, test_file: str) -> str:
        self.logger.print(f"run {test_file}")
        with open(test_file, "r", encoding="utf-8") as file:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                # 파일을 한 줄씩 읽기
                for line in file:
                    self.execute_command(line.strip().split())

            return output.getvalue()

    def read_test_result(self, file_path: str) -> str:
        """주어진 경로의 파일을 읽어 내용 반환"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def compare_test_result(self, result_file: str, output: str) -> bool:
        return output == self.read_test_result(result_file)
