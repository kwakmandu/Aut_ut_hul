import io
import os

from logger.logger import Logger
import contextlib
from shell.commander import CommandExecutor, CommandValidator
import re


class ScriptTester:
    def __init__(self, ce: CommandExecutor, cv: CommandValidator) -> None:
        self.__command_executor = ce
        self.__command_validator = cv
        self.__logger: Logger = Logger()
        self.__test_script_dir: str = "./testscript"

    def run_test(self, test_file: str) -> str:
        self.__logger.print(f"run {test_file}")
        with open(test_file, "r", encoding="utf-8") as file:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                # 파일을 한 줄씩 읽기
                for line in file:
                    self.__command_executor.execute_command(line.strip().split())

            return output.getvalue()

    def read_test_result(self, file_path: str) -> str:
        """주어진 경로의 파일을 읽어 내용 반환"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def compare_test_result(self, result_file: str, output: str) -> bool:
        return output == self.read_test_result(result_file)

    def run_test_list(self, test_list_file: str) -> None:
        if not self.__is_valid_test_list_file(test_list_file):
            self.__logger.print(f"invalid test list: {test_list_file}")
            exit(1)

        self.__logger.print(f"run test list {test_list_file}")
        test_list_file_path = f"{self.__test_script_dir}/{test_list_file}"
        with open(test_list_file_path, "r", encoding="utf-8") as file:
            for line in file:
                test_file, result_file = line.rstrip().split(" ")
                test_file_path, result_file_path = (
                    f"{self.__test_script_dir}/{test_file}",
                    f"{self.__test_script_dir}/{result_file}",
                )
                print(f"{test_file} --- Run...", end="", flush=True)

                output = self.run_test(test_file_path)
                if self.compare_test_result(result_file_path, output):
                    print("Pass")
                else:
                    print("Fail")
                    exit(1)

    def __is_valid_test_list_file(self, test_list_file: str) -> bool:
        test_list_file_path = f"{self.__test_script_dir}/{test_list_file}"
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
        test_file_path = f"{self.__test_script_dir}/{test_file}"
        result_file_path = f"{self.__test_script_dir}/{result_file}"

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
        test_file_path = f"{self.__test_script_dir}/{test_file}"

        with open(test_file_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                if not self.__command_validator.is_valid_command(line.strip().split()):
                    print(
                        f"{test_file}:{line_num}: `{line.strip()}` is invalid command"
                    )
                    return False

        return True
