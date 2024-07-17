import contextlib
import io
import os
import subprocess
import sys
from helper import Helper
from logger.logger import Logger
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
        self.ssd_dir: str = "../ssd"
        self.test_script_dir: str = "../testscript"
        self.helper: Helper = Helper()
        self.logger: Logger = Logger()

    def is_valid_command(self, inputs: list[str]) -> bool:
        if inputs[0] not in ALLOWED_INITIAL_COMMANDS:
            return False

        # write
        if inputs[0] == "write":
            return (
                len(inputs) == 3
                and self.__is_valid_address(inputs[1])
                and self.__is_valid_hex(inputs[2])
            )

        elif inputs[0] == "read":
            return len(inputs) == 2 and self.__is_valid_address(inputs[1])

        elif inputs[0] == "fullwrite":
            return len(inputs) == 2 and self.__is_valid_hex(inputs[1])

        elif inputs[0] == "erase":
            return (
                len(inputs) == 3
                and self.__is_valid_address(inputs[1])
                and self.__is_valid_address(inputs[2])
            )
        elif inputs[0] == "erase_range":
            return (
                len(inputs) == 3
                and self.__is_valid_address(inputs[1])
                and self.__is_valid_address(inputs[2])
                and int(inputs[1]) < int(inputs[2])
            )

        elif len(inputs) == 1:
            return True

        return False

    def __is_valid_address(self, value: str) -> bool:
        return value.isdigit() and 0 <= int(value) <= 99

    def __is_valid_hex(self, value: str) -> bool:
        if len(value) != 10 or value[:2] != "0x":
            return False
        return all(char in "0123456789ABCDEF" for char in value[2:])

    def run(self) -> None:
        self.logger.print("User IP:192.XX.XX.XX be connected")
        print("Hello ! Welcome to the Aut ut hul shell !")

        self.is_run = True
        while self.is_run:
            try:
                user_input = input()
                user_input_list = user_input.split(" ")
                if not self.is_valid_command(user_input_list):
                    print("INVALID COMMAND")
                    self.logger.print(f"INVALID COMMAND - {user_input}")
                    continue
                self.select_commands(user_input_list)

            except Exception as e:
                self.logger.print(e)

        self.logger.print("User IP:192.XX.XX.XX be disconnected")
        print("See you !")

    def select_commands(self, inputs: list[str]) -> None:
        if len(inputs) < 1:
            return

        match inputs[0]:
            case "write":
                self.write(inputs[1], inputs[2])
            case "read":
                self.read(inputs[1])
            case "erase":
                self.erase(inputs[1], inputs[2])
            case "erase_range":
                self.erase(inputs[1], inputs[2])
            case "exit":
                self.exit()
            case "help":
                self.help()
            case "fullwrite":
                self.fullwrite(inputs[1])
            case "fullread":
                self.fullread()
            case _:
                print("INVALID COMMAND")

    def write(self, address: str, data: str) -> None:
        self.logger.print(f"write {address} {data}")
        subprocess.run(
            [sys.executable, f"{self.ssd_dir}/virtual_ssd.py", "W", address, data]
        )

    def read(self, address: str) -> None:
        self.logger.print(f"read {address}")
        subprocess.run([sys.executable, f"{self.ssd_dir}/virtual_ssd.py", "R", address])
        try:
            with open(f"{self.ssd_dir}/result.txt", "r") as file:
                file_contents = file.read().strip()
                print(file_contents)
        except FileNotFoundError:
            print("파일이 존재하지 않습니다.")

    def erase(self, address: str, size: str) -> None:
        self.logger.print(f"erase {address} {size}")
        isize = int(size)
        while isize > 10:
            subprocess.run(
                [sys.executable, f"{self.ssd_dir}/virtual_ssd.py", "E", address, "10"]
            )
            isize -= 10
        subprocess.run(
            [
                sys.executable,
                f"{self.ssd_dir}/virtual_ssd.py",
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
                    self.select_commands(line.strip().split())

            return output.getvalue()

    def read_test_result(self, file_path: str) -> str:
        """주어진 경로의 파일을 읽어 내용 반환"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def compare_test_result(self, result_file: str, output: str) -> bool:
        return output == self.read_test_result(result_file)

    def run_test_list(self, test_list_file: str) -> None:
        if not self.__is_valid_test_list_file(test_list_file):
            self.logger.print(f"invalid test list: {test_list_file}")
            exit(1)

        self.logger.print(f"run test list {test_list_file}")
        test_list_file_path = f"{self.test_script_dir}/{test_list_file}"
        with open(test_list_file_path, "r", encoding="utf-8") as file:
            for line in file:
                test_file, result_file = line.rstrip().split(" ")
                test_file_path, result_file_path = (
                    f"{self.test_script_dir}/{test_file}",
                    f"{self.test_script_dir}/{result_file}",
                )
                print(f"{test_file} --- Run...", end="")

                output = self.run_test(test_file_path)
                if self.compare_test_result(result_file_path, output):
                    print("Pass")
                else:
                    print("Fail")
                    exit(1)

    def __is_valid_test_list_file(self, test_list_file: str) -> bool:
        test_list_file_path = f"{self.test_script_dir}/{test_list_file}"
        if not os.path.exists(test_list_file_path):
            print(f"file {test_list_file} was not found.")
            return False

        with open(test_list_file_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                if not self.__is_valid_test_list_line(line, line_num, test_list_file):
                    return False
        return True

    def __is_valid_test_list_line(
        self, line: str, line_num: int, test_list_file: str
    ) -> bool:
        if not re.match(r"^\S+\.txt \S+\.txt$", line.strip()):
            print(f"{test_list_file}:{line_num}: line does not match '*.txt *.txt'.")
            return False

        test_file, result_file = line.split()
        test_file_path = f"{self.test_script_dir}/{test_file}"
        result_file_path = f"{self.test_script_dir}/{result_file}"

        if not os.path.exists(test_file_path):
            print(f"{test_list_file}:{line_num}: file {test_file} does not exist.")
            return False
        if not self.__is_valid_test_file(test_file):
            return False

        if not os.path.exists(result_file_path):
            print(f"{test_list_file}:{line_num}: file {result_file} does not exist.")
            return False
        return True

    def __is_valid_test_file(self, test_file: str) -> bool:
        test_file_path = f"{self.test_script_dir}/{test_file}"

        with open(test_file_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                if not self.is_valid_command(line.strip().split()):
                    print(
                        f"{test_file}:{line_num}: `{line.strip()}` is invalid command"
                    )
                    return False

        return True


if __name__ == "__main__":
    try:
        shell = Shell()
        args = sys.argv[1:]  # Get command-line arguments excluding the script name

        if len(args) == 0:
            shell.run()
        elif len(args) == 1:
            shell.run_test_list(args[0])
        else:
            raise ValueError("This script accepts at most one argument.")
    except Exception as e:
        print(f"An error occurred: {e}")
