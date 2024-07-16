import subprocess

from ssd.storage_device_interface import StorageDeviceInterface
from ssd.virtual_ssd import VirtualSSD


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
        self.ssd: StorageDeviceInterface = VirtualSSD()
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

    def write(self, address: int, data: str) -> None:
        subprocess.run(["python", "../ssd/virtual_ssd.py", "W", str(address), data])

    def read(self, address: int) -> None:
        subprocess.run(["python", "../ssd/virtual_ssd.py", "R", str(address)])
        with open("result.txt", "r") as file:
            file_contents = file.read()
        print(file_contents)

    def exit(self) -> None:
        self.is_run = False

    def help(self) -> None:
        for h_info in self.help_information:
            print(h_info)

    def fullwrite(self, data: str) -> None:
        for i in range(100):
            self.ssd.write(i, data)

    def fullread(self) -> None:
        for i in range(100):
            self.read(i)


if __name__ == "__main__":
    shell = Shell()
    shell.run()
