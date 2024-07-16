import contextlib
import io
import os
import subprocess
import sys
from helper import Helper

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_INITIAL_COMMANDS = [
    "write",
    "read",
    "exit",
    "help",
    "fullwrite",
    "fullread",
    "testapp1",
    "testapp2",
]


class Shell:

    def __init__(self) -> None:
        self.is_run = False
        self.ssd_path: str = "../ssd"
        self.test_script_path: str = "../testscript"
        self.helper: Helper = Helper()

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
        self.is_run = True
        while self.is_run:
            inputs = input().split(" ")
            if not self.is_valid_command(inputs):
                print("INVALID COMMAND")
                continue
            self.select_commands(inputs)

    def select_commands(self, inputs: list[str]) -> None:
        if len(inputs) < 1:
            return

        match inputs[0]:
            case "write":
                self.write(inputs[1], inputs[2])
            case "read":
                self.read(inputs[1])
            case "exit":
                self.exit()
            case "help":
                self.help()
            case "fullwrite":
                self.fullwrite(inputs[1])
            case "fullread":
                self.fullread()
            case _:
                self.run_testscript(inputs[0])

    def write(self, address: str, data: str) -> None:
        subprocess.run(
            [sys.executable, f"{self.ssd_path}/virtual_ssd.py", "W", address, data]
        )

    def read(self, address: str) -> None:
        subprocess.run(
            [sys.executable, f"{self.ssd_path}/virtual_ssd.py", "R", address]
        )
        try:
            with open(f"{self.ssd_path}/result.txt", "r") as file:
                file_contents = file.read()
                print(file_contents)
        except FileNotFoundError:
            print("파일이 존재하지 않습니다.")

    def exit(self) -> None:
        self.is_run = False

    def help(self) -> None:
        for h_info in self.helper.get_help_information():
            print(h_info)

    def fullwrite(self, data: str) -> None:
        for i in range(100):
            self.write(str(i), data)

    def fullread(self) -> None:
        for i in range(100):
            self.read(str(i))

    def run_testscript(self, testcase: str) -> None:
        if testcase == "testapp1":
            self.run_test(
                f"{self.test_script_path}/TestApp01.txt",
                f"{self.test_script_path}/TestAppResult01.txt",
            )
        elif testcase == "testapp2":
            self.run_test(
                f"{self.test_script_path}/TestApp02.txt",
                f"{self.test_script_path}/TestAppResult02.txt",
            )
        else:
            print("INVALID COMMAND")

    def run_test(self, test_file: str, result_file: str) -> bool:
        with open(test_file, "r", encoding="utf-8") as file:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                # 파일을 한 줄씩 읽기
                for line in file:
                    self.select_commands(line.strip().split())

            captured_output = output.getvalue()
            result_contents = self.read_test_result(result_file)

            if captured_output == result_contents:
                return True
            else:
                return False

    def read_test_result(self, file_path) -> str:
        """주어진 경로의 파일을 읽어 내용 반환"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


if __name__ == "__main__":
    shell = Shell()
    shell.run()
