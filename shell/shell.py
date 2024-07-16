import subprocess
import sys


ALLOWED_INITIAL_COMMANDS = [
    "write",
    "read",
    "exit",
    "help",
    "fullwrite",
    "fullread",
]  # test 명령어 추가 필요


class Validate:
    def is_valid_data(self) -> None:
        pass

    def is_valid_LBA_addr(self) -> None:
        pass

    def command_string_parser(self) -> None:
        pass


class Shell:

    def __init__(self) -> None:
        self.is_run = False
        self.ssd_path: str = "../ssd"
        self.help_information = [
            "Available commands:",
            "  write <LBA> <value>  - Write value to the specified LBA",
            "  read <LBA>           - Read value from the specified LBA",
            "  fullwrite <value>    - Write value to all LBAs",
            "  fullread             - Read values from all LBAs",
            "  exit                 - Exit the shell",
            "  help                 - Show this help message",
        ]

    def is_valid_command(self, inputs: list) -> bool:
        if inputs[0] not in ALLOWED_INITIAL_COMMANDS:
            return False

        if len(inputs) == 1:
            return True
        # write
        if inputs[0] == "write":
            if not inputs[1].isdigit():
                return False

            if not 0 <= int(inputs[1]) <= 99:
                return False

            if len(inputs[2]) != 10:
                return False

            if inputs[2][:2] != "0x":
                return False

            for char in inputs[2][2:]:
                if not (("0" <= char <= "9") or ("A" <= char <= "F")):
                    return False

        elif inputs[0] == "read":
            if not inputs[1].isdigit():
                return False

            if not 0 <= int(inputs[1]) <= 99:
                return False

        elif inputs[0] == "fullwrite":

            if len(inputs[1]) != 10:
                return False

            if inputs[1][:2] != "0x":
                return False

            for char in inputs[1][2:]:
                if not (("0" <= char <= "9") or ("A" <= char <= "F")):
                    return False

        return True

    def run(self) -> None:
        self.is_run = True
        while self.is_run:
            inputs = input().split(" ")
            if not self.is_valid_command(inputs):
                print("INVALID COMMAND")
                continue
            self.is_run = self.select_commands(inputs)

    def select_commands(self, inputs) -> bool:
        if inputs[0] == "ssd" and inputs[1] == "W":
            self.write(int(inputs[2]), inputs[3])
        if inputs[0] == "ssd" and inputs[1] == "R":
            self.read(int(inputs[2]))

        elif inputs[0] == "exit":
            self.exit()

        elif inputs[0] == "help":
            self.help()

        elif inputs[0] == "fullwrite":
            self.fullwrite(inputs[1])

        elif inputs[0] == "fullread":
            self.fullread()

        else:
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
        for h_info in self.help_information:
            print(h_info)

    def fullwrite(self, data: str) -> None:
        for i in range(100):
            self.write(str(i), data)

    def fullread(self) -> None:
        for i in range(100):
            self.read(str(i))

    def run_testscript(self, testcase) -> None:
        if testcase == "testapp1":
            self.run_test("testscript/TestApp1.txt")
        elif testcase == "testapp2":
            self.run_test("testscript/TestApp2.txt")
        else:
            print("WRONG COMMAND")
            self.exit()

    def run_test(self, test_file):
        with open(test_file, "r", encoding="utf-8") as file:
            # 파일을 한 줄씩 읽기
            for line in file:
                self.select_commands(line.strip())


if __name__ == "__main__":
    shell = Shell()
    shell.run()
