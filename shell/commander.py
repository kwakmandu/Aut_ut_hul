import subprocess
import sys
from shell.helper import Helper
from logger.logger import Logger

ALLOWED_INITIAL_COMMANDS = [
    "write",
    "read",
    "erase",
    "erase_range",
    "flush",
    "exit",
    "help",
    "fullwrite",
    "fullread",
]


class CommandValidator:
    def is_valid_command(self, inputs: list[str]) -> bool:
        if len(inputs) == 0:
            return False

        if inputs[0] not in ALLOWED_INITIAL_COMMANDS:
            return False

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
                and 1 <= int(inputs[2]) <= 100
                and int(inputs[1]) + int(inputs[2]) <= 100
            )
        elif inputs[0] == "erase_range":
            return (
                len(inputs) == 3
                and self.__is_valid_address(inputs[1])
                and self.__is_valid_address(str(int(inputs[2]) - 1))
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


class CommandExecutor:
    def __init__(self, ssd_executable: str = "ssd.py") -> None:
        self.__ssd_path: str = "./"
        self.__ssd_executable: str = self.__ssd_path + "/" + ssd_executable
        self.__helper: Helper = Helper()
        self.__logger: Logger = Logger()

    def execute_command(self, inputs: list[str]) -> bool:
        if not inputs:
            return

        match inputs[0]:
            case "write":
                self.write(inputs[1], inputs[2])
            case "read":
                self.read(inputs[1])
            case "erase":
                self.erase(inputs[1], inputs[2])
            case "erase_range":
                self.erase(inputs[1], str(int(inputs[2]) - int(inputs[1])))
            case "flush":
                self.flush()
            case "exit":
                self.exit()
                return False
            case "help":
                self.help()
            case "fullwrite":
                self.fullwrite(inputs[1])
            case "fullread":
                self.fullread()
            case _:
                print("INVALID COMMAND")

        return True

    def write(self, address: str, data: str) -> None:
        self.__logger.print(f"write {address} {data}")
        subprocess.run([sys.executable, self.__ssd_executable, "W", address, data])

    def read(self, address: str) -> None:
        self.__logger.print(f"read {address}")
        subprocess.run([sys.executable, self.__ssd_executable, "R", address])
        try:
            with open(f"{self.__ssd_path}/result.txt", "r") as file:
                file_contents = file.read().strip()
                print(file_contents)
        except FileNotFoundError:
            print("파일이 존재하지 않습니다.")

    def erase(self, address: str, size: str) -> None:
        self.__logger.print(f"erase {address} {size}")
        isize = int(size)
        iaddress = int(address)
        while isize > 10:
            subprocess.run(
                [sys.executable, self.__ssd_executable, "E", str(iaddress), "10"]
            )
            iaddress += 10
            isize -= 10
        subprocess.run(
            [
                sys.executable,
                self.__ssd_executable,
                "E",
                str(iaddress),
                str(isize),
            ]
        )

    def flush(self) -> None:
        self.__logger.print(f"flush")
        subprocess.run([sys.executable, self.__ssd_executable, "F"])

    def exit(self) -> None:
        self.__logger.print(f"exit")

    def help(self) -> None:
        self.__logger.print(f"help")
        for h_info in self.__helper.get_help_information():
            print(h_info)

    def fullwrite(self, data: str) -> None:
        self.__logger.print(f"fullwrite {data}")
        for i in range(100):
            self.write(str(i), data)

    def fullread(self) -> None:
        self.__logger.print(f"fullread")
        for i in range(100):
            self.read(str(i))

    def set_ssd_executable(self, ssd_executable: str) -> None:
        self.__ssd_executable: str = self.__ssd_path + "/" + ssd_executable
